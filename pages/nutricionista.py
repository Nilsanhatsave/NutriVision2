# pages/nutricionista.py
# ===== PERFIL NUTRICIONISTA =====

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ========== CONEXÃO DIRETA COM SUPABASE ==========
from supabase import create_client

# ===== CHAVES DIRETAS =====
SUPABASE_URL = "https://llfcnigfidoiyhaitala.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxsZmNuaWdmaWRvaXloYWl0YWxhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM2NTY2OTYsImV4cCI6MjA5OTIzMjY5Nn0.-WtmiDwYPS9eQDRsQ-bmXGKzvy4p9x7i9bzYGCgX3VM"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    SUPABASE_AVAILABLE = True
    print("✅ Supabase conectado!")
except Exception as e:
    SUPABASE_AVAILABLE = False
    print(f"❌ Erro: {e}")

def carregar_criancas_supabase():
    """Carrega todas as crianças do Supabase"""
    if not SUPABASE_AVAILABLE:
        return False, []
    try:
        resultado = supabase.table('criancas').select('*').order('created_at', desc=True).execute()
        return True, resultado.data
    except Exception as e:
        return False, str(e)

def render_nutricionista():
    # ===== CARREGAR DADOS DO SUPABASE =====
    if 'criancas' not in st.session_state or not st.session_state.criancas:
        if SUPABASE_AVAILABLE:
            sucesso, dados = carregar_criancas_supabase()
            if sucesso and dados:
                st.session_state.criancas = dados
                st.success(f"✅ {len(dados)} pacientes carregados do Supabase!")
            else:
                st.session_state.criancas = []
                if dados:
                    st.info(f"ℹ️ {dados}")
        else:
            st.session_state.criancas = []
            st.warning("⚠️ Supabase não disponível")
    
    # ===== ENCAMINHAMENTOS =====
    if 'encaminhamentos' not in st.session_state:
        st.session_state.encaminhamentos = []
    
    st.title("🍎 Nutricionista - Avaliação Nutricional")
    st.markdown("""
    <p style='color: #555; margin-bottom: 2rem;'>
    Gestão de pacientes, encaminhamentos e análise nutricional.
    </p>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # ===== PARTE 1: LISTA DE PACIENTES + MÉTRICAS =====
    # ============================================================
    
    if not st.session_state.criancas:
        st.info("📋 Nenhum paciente registado no sistema.")
        return
    
    df = pd.DataFrame(st.session_state.criancas)
    
    # ===== FILTRAR ENCAMINHAMENTOS PARA NUTRICIONISTA =====
    encaminhamentos_nutri = [
        e for e in st.session_state.encaminhamentos 
        if 'Nutricionista' in e.get('especialidade', '')
    ]
    
    # ===== MÉTRICAS =====
    total_pacientes = len(st.session_state.criancas)
    total_encaminhados = len(encaminhamentos_nutri)
    atendidos = len([e for e in encaminhamentos_nutri if e.get('status') == 'Concluído'])
    pendentes = total_encaminhados - atendidos
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👶 Total Pacientes", total_pacientes)
    with col2:
        st.metric("📨 Encaminhados", total_encaminhados)
    with col3:
        st.metric("✅ Atendidos", atendidos)
    with col4:
        st.metric("⏳ Pendentes", pendentes)
    
    st.markdown("---")
    
    # ===== LISTA DE PACIENTES =====
    st.subheader("📋 Lista de Pacientes")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        risco_filter = st.multiselect(
            "Filtrar por Risco de Anemia",
            ["ALTO", "MÉDIO", "BAIXO"],
            default=["ALTO", "MÉDIO", "BAIXO"]
        )
    with col2:
        if 'provincia' in df.columns:
            provincia_filter = st.multiselect(
                "Filtrar por Província",
                df['provincia'].unique().tolist() if not df.empty else [],
                default=df['provincia'].unique().tolist() if not df.empty else []
            )
    
    # Aplicar filtros
    df_filtered = df.copy()
    if 'risco_anemia_nivel' in df.columns and risco_filter:
        df_filtered = df_filtered[df_filtered['risco_anemia_nivel'].isin(risco_filter)]
    if 'provincia' in df.columns and provincia_filter:
        df_filtered = df_filtered[df_filtered['provincia'].isin(provincia_filter)]
    
    if df_filtered.empty:
        st.info("Nenhum paciente encontrado com os filtros selecionados.")
    else:
        # Tabela
        cols_to_show = ['nome_completo', 'idade_meses', 'peso', 'altura', 'muac', 
                        'dds_calculado', 'risco_anemia_nivel', 'risco_fome_nivel', 
                        'risco_inseguranca_nivel', 'provincia']
        cols_available = [c for c in cols_to_show if c in df_filtered.columns]
        
        st.dataframe(
            df_filtered[cols_available],
            use_container_width=True,
            hide_index=True,
            column_config={
                "nome_completo": "Nome",
                "idade_meses": "Idade (meses)",
                "peso": "Peso (kg)",
                "altura": "Altura (cm)",
                "muac": "MUAC (mm)",
                "dds_calculado": "DDS",
                "risco_anemia_nivel": "Risco Anemia",
                "risco_fome_nivel": "Fome Oculta",
                "risco_inseguranca_nivel": "Insegurança Alimentar",
                "provincia": "Província"
            }
        )
    
    # ============================================================
    # ===== PARTE 2: ESTATÍSTICAS E ANÁLISES =====
    # ============================================================
    
    st.markdown("---")
    st.subheader("📊 Estatísticas e Análises Nutricionais")
    
    # ===== ESTATÍSTICAS RÁPIDAS =====
    col1, col2, col3 = st.columns(3)
    with col1:
        alto_anemia = len(df[df['risco_anemia_nivel'] == 'ALTO'])
        st.metric("🩸 Anemia ALTA", alto_anemia, delta=f"{alto_anemia/total_pacientes*100:.1f}%" if total_pacientes > 0 else "0%")
    with col2:
        alto_fome = len(df[df['risco_fome_nivel'] == 'ALTO'])
        st.metric("🍽️ Fome Oculta ALTA", alto_fome, delta=f"{alto_fome/total_pacientes*100:.1f}%" if total_pacientes > 0 else "0%")
    with col3:
        alto_inseg = len(df[df['risco_inseguranca_nivel'] == 'ALTO'])
        st.metric("🏠 Insegurança ALTA", alto_inseg, delta=f"{alto_inseg/total_pacientes*100:.1f}%" if total_pacientes > 0 else "0%")
    
    st.markdown("---")
    
    # ===== GRÁFICOS =====
    col1, col2 = st.columns(2)
    
    with col1:
        if 'risco_anemia_nivel' in df.columns:
            fig1 = px.pie(df, names='risco_anemia_nivel', 
                         title='Risco de Anemia',
                         color='risco_anemia_nivel',
                         color_discrete_map={'ALTO': '#c62828', 'MÉDIO': '#ef6c00', 'BAIXO': '#2e7d32'})
            fig1.update_layout(showlegend=True)
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        if 'risco_fome_nivel' in df.columns:
            fig2 = px.pie(df, names='risco_fome_nivel', 
                         title='Fome Oculta',
                         color='risco_fome_nivel',
                         color_discrete_map={'ALTO': '#c62828', 'MÉDIO': '#ef6c00', 'BAIXO': '#2e7d32'})
            fig2.update_layout(showlegend=True)
            st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        if 'risco_inseguranca_nivel' in df.columns:
            fig3 = px.pie(df, names='risco_inseguranca_nivel', 
                         title='Insegurança Alimentar',
                         color='risco_inseguranca_nivel',
                         color_discrete_map={'ALTO': '#c62828', 'MÉDIO': '#ef6c00', 'BAIXO': '#2e7d32'})
            fig3.update_layout(showlegend=True)
            st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        if 'dds_calculado' in df.columns:
            fig4 = px.histogram(df, x='dds_calculado', 
                               title='Diversidade Alimentar (DDS)',
                               nbins=10,
                               color='risco_anemia_nivel',
                               color_discrete_map={'ALTO': '#c62828', 'MÉDIO': '#ef6c00', 'BAIXO': '#2e7d32'})
            st.plotly_chart(fig4, use_container_width=True)
    
    # ===== RECOMENDAÇÕES =====
    st.markdown("---")
    st.subheader("💡 Recomendações Nutricionais")
    
    total_alto = len(df[df['risco_anemia_nivel'] == 'ALTO'])
    total_medio = len(df[df['risco_anemia_nivel'] == 'MÉDIO'])
    total_fome_alto = len(df[df['risco_fome_nivel'] == 'ALTO'])
    total_inseg_alto = len(df[df['risco_inseguranca_nivel'] == 'ALTO'])
    
    if total_alto > 0:
        st.warning(f"🔴 **{total_alto} pacientes com ALTO risco de anemia** - Priorizar suplementação de ferro e alimentação rica em ferro.")
    
    if total_medio > 0:
        st.info(f"🟠 **{total_medio} pacientes com MÉDIO risco de anemia** - Reforçar orientação nutricional e monitoramento.")
    
    if total_fome_alto > 0:
        st.warning(f"🔴 **{total_fome_alto} pacientes com ALTA fome oculta** - Diversificar alimentação com frutas, legumes e vegetais.")
    
    if total_inseg_alto > 0:
        st.warning(f"🔴 **{total_inseg_alto} pacientes com ALTA insegurança alimentar** - Avaliar programas de complementação alimentar.")
    
    if total_alto == 0 and total_medio == 0 and total_fome_alto == 0 and total_inseg_alto == 0:
        st.success("✅ Todos os pacientes estão com BAIXO risco. Manter acompanhamento preventivo.")
    
    # ============================================================
    # ===== ENCAMINHAMENTOS (opcional - se quiser manter) =====
    # ============================================================
    
    st.markdown("---")
    st.subheader("📨 Encaminhamentos Recebidos")
    
    if encaminhamentos_nutri:
        for enc in encaminhamentos_nutri:
            urgencia = enc.get('urgencia', 'Normal')
            if urgencia == "Muito Urgente":
                cor = "🔴"
            elif urgencia == "Urgente":
                cor = "🟠"
            else:
                cor = "🟢"
            
            with st.expander(f"{cor} 👶 {enc.get('paciente', 'N/A')} - {enc.get('data', 'N/A')}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📋 Dados do Encaminhamento**")
                    st.markdown(f"**Especialidade:** {enc.get('especialidade', 'N/A')}")
                    st.markdown(f"**Urgência:** {enc.get('urgencia', 'Normal')}")
                    st.markdown(f"**Motivo:** {enc.get('motivo', 'N/A')}")
                    st.markdown(f"**Status:** {enc.get('status', 'Pendente')}")
                    st.markdown(f"**Médico:** {enc.get('medico_responsavel', 'N/A')}")
                
                with col2:
                    st.markdown("**📊 Dados Clínicos**")
                    if 'dados_clinicos' in enc and enc['dados_clinicos']:
                        dados = enc['dados_clinicos']
                        st.markdown(f"- Hemoglobina: {dados.get('hemoglobina', 'N/A')} g/dL")
                        st.markdown(f"- Tipo Anemia: {dados.get('tipo_anemia', 'N/A')}")
                        st.markdown(f"- DDS: {dados.get('dds', 0)}/9")
                        st.markdown(f"- MUAC: {dados.get('muac', 0)} mm")
                
                # Marcar como visto
                if enc.get('status') == 'Pendente':
                    if st.button(f"✅ Marcar como Visto - {enc['paciente']}"):
                        for e in st.session_state.encaminhamentos:
                            if e['paciente'] == enc['paciente'] and e['data'] == enc['data']:
                                e['status'] = 'Em análise'
                                st.rerun()
    else:
        st.info("📋 Nenhum encaminhamento recebido ainda.")

if __name__ == "__main__":
    render_nutricionista()