# pages/nutricionista.py
# ===== PERFIL NUTRICIONISTA - AVALIAÇÃO NUTRICIONAL =====

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import base64
import time
import sys
import os

# Adicionar o diretório pai ao path para importar funções
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import t, SUPABASE_AVAILABLE

# ========== CONEXÃO SUPABASE ==========
try:
    from supabase import create_client
    SUPABASE_URL = "https://llfcnigfidoiyhaitala.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxsZmNuaWdmaWRvaXloYWl0YWxhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM2NTY2OTYsImV4cCI6MjA5OTIzMjY5Nn0.-WtmiDwYPS9eQDRsQ-bmXGKzvy4p9x7i9bzYGCgX3VM"
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

# ========== FUNÇÃO PARA OBTER DADOS CLÍNICOS ==========
def obter_dados_clinicos(row):
    """Extrai os dados clínicos de forma segura"""
    if 'dados_clinicos' in row and row['dados_clinicos']:
        if isinstance(row['dados_clinicos'], dict):
            return row['dados_clinicos']
        elif isinstance(row['dados_clinicos'], str):
            try:
                return json.loads(row['dados_clinicos'])
            except:
                return {}
    return {}

# ========== FUNÇÃO PRINCIPAL ==========
def render_nutricionista():
    # ===== CARREGAR DADOS =====
    if 'criancas' not in st.session_state or not st.session_state.criancas:
        if SUPABASE_AVAILABLE:
            sucesso, dados = carregar_criancas_supabase()
            if sucesso and dados:
                st.session_state.criancas = dados
                st.success(f"✅ {len(dados)} {t('pacientes')} {t('carregados')}!")
            else:
                st.session_state.criancas = []
                if dados:
                    st.info(f"ℹ️ {dados}")
        else:
            st.session_state.criancas = []
            st.warning(t('supabase_indisponivel'))
    
    # ===== ENCAMINHAMENTOS =====
    if 'encaminhamentos' not in st.session_state:
        st.session_state.encaminhamentos = []
    
    # ===== PLANOS DE INTERVENÇÃO =====
    if 'planos_intervencao' not in st.session_state:
        st.session_state.planos_intervencao = []
    
    st.title(f"🍎 {t('nutricionista_titulo')}")
    st.markdown(f"""
    <p style='color: #555; margin-bottom: 2rem;'>
    {t('descricao_nutricionista')}
    </p>
    """, unsafe_allow_html=True)
    
    # ===== ESTATÍSTICAS =====
    total = len(st.session_state.criancas)
    enc_nutri = [e for e in st.session_state.encaminhamentos if 'Nutricionista' in e.get('especialidade', '')]
    pendentes = len([e for e in enc_nutri if e.get('status') != 'Concluído'])
    atendidos = len([e for e in enc_nutri if e.get('status') == 'Concluído'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(f"👶 {t('total_pacientes')}", total)
    with col2:
        st.metric(f"📨 {t('encaminhamentos')}", len(enc_nutri))
    with col3:
        st.metric(f"⏳ {t('pendentes')}", pendentes)
    with col4:
        st.metric(f"✅ {t('atendidos')}", atendidos)
    
    st.markdown("---")
    
    # ============================================================
    # ===== ABAS =====
    # ============================================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Avaliação",
        "📝 Plano de Intervenção",
        "📊 Dashboard",
        "📨 Encaminhamentos"
    ])
    
    # ============================================================
    # ===== TAB 1: AVALIAÇÃO =====
    # ============================================================
    with tab1:
        st.subheader(f"👤 {t('selecionar_paciente')}")
        
        if not st.session_state.criancas:
            st.info(t('nenhum_paciente'))
            return
        
        df = pd.DataFrame(st.session_state.criancas)
        selected = st.selectbox(
            f"{t('selecionar_paciente')}:",
            df['nome_completo'].unique().tolist()
        )
        
        patient_data = df[df['nome_completo'] == selected].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 📊 {t('dados_paciente')}")
            st.markdown(f"**👶 {t('nome')}:** {patient_data['nome_completo']}")
            st.markdown(f"**📏 {t('idade')}:** {patient_data['idade_meses']} {t('meses')}")
            st.markdown(f"**⚖️ {t('peso')}:** {patient_data['peso']} kg")
            st.markdown(f"**📐 {t('altura')}:** {patient_data['altura']} cm")
            st.markdown(f"**📏 {t('muac')}:** {patient_data['muac']} mm")
            st.markdown(f"**📊 DDS:** {patient_data.get('dds_calculado', 0)}/9")
            st.markdown(f"**📍 {t('provincia')}:** {patient_data.get('provincia', 'N/A')}")
            st.markdown(f"**📍 {t('distrito')}:** {patient_data.get('distrito', 'N/A')}")
        
        with col2:
            st.markdown(f"#### 🩺 {t('risco')}")
            risco = patient_data.get('risco_anemia_nivel', 'N/A')
            cor = "🔴" if risco == "ALTO" else "🟡" if risco == "MÉDIO" else "🟢"
            st.metric(f"{t('risco_anemia')}", f"{cor} {risco}")
            st.metric(f"{t('risco_fome')}", patient_data.get('risco_fome_nivel', 'N/A'))
            st.metric(f"{t('risco_inseguranca')}", patient_data.get('risco_inseguranca_nivel', 'N/A'))
        
        st.divider()
        
        # ===== AVALIAÇÃO NUTRICIONAL =====
        st.markdown(f"### 🥗 {t('avaliacao_nutricional')}")
        
        with st.form("avaliacao_nutricional_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**📊 {t('diversidade_alimentar_dds')}**")
                dds_atual = patient_data.get('dds_calculado', 0)
                dds_novo = st.slider(
                    t('dds_slider'),
                    0, 9, int(dds_atual) if dds_atual else 5,
                    key=f"dds_{selected}"
                )
                
                st.markdown(f"**🍽️ {t('frequencia_refeicoes')}**")
                refeicoes = st.selectbox(
                    t('refeicoes_por_dia'),
                    ["1", "2", "3", "4", "5+"],
                    key=f"refeicoes_{selected}"
                )
            
            with col2:
                st.markdown(f"**🥩 {t('consumo_proteina')}**")
                consumo_proteina = st.selectbox(
                    t('fonte_proteina'),
                    ["Carnes", "Ovos", "Feijão", "Amendoim", "Peixe", "Mista"],
                    key=f"proteina_{selected}"
                )
                
                st.markdown(f"**🍊 {t('consumo_vitamina_c')}**")
                consumo_vit_c = st.selectbox(
                    t('fonte_vitamina_c'),
                    ["Laranja", "Limão", "Manga", "Goiaba", "Tomate", "Misto"],
                    key=f"vitamina_c_{selected}"
                )
            
            st.markdown(f"**🥬 {t('observacoes_nutricionais')}**")
            observacoes_nutri = st.text_area(
                t('observacoes'),
                placeholder=t('observacoes_placeholder'),
                height=80,
                key=f"obs_nutri_{selected}"
            )
            
            if st.form_submit_button(f"💾 {t('salvar_avaliacao')}", use_container_width=True):
                st.success(f"✅ {t('avaliacao_salva')} {selected}!")
    
    # ============================================================
    # ===== TAB 2: PLANO DE INTERVENÇÃO =====
    # ============================================================
    with tab2:
        st.subheader(f"📝 {t('plano_intervencao')}")
        
        if not st.session_state.criancas:
            st.info(t('nenhum_paciente'))
            return
        
        df = pd.DataFrame(st.session_state.criancas)
        selected_plano = st.selectbox(
            f"{t('selecionar_paciente')}:",
            df['nome_completo'].unique().tolist(),
            key="select_plano"
        )
        
        patient_data_plano = df[df['nome_completo'] == selected_plano].iloc[0]
        
        st.markdown(f"#### 👶 {patient_data_plano['nome_completo']}")
        st.markdown(f"**{t('idade')}:** {patient_data_plano['idade_meses']} {t('meses')}")
        st.markdown(f"**DDS:** {patient_data_plano.get('dds_calculado', 0)}/9")
        
        st.divider()
        
        with st.form("plano_intervencao_form"):
            st.markdown(f"### 🎯 {t('objetivos_intervencao')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**📋 {t('objetivo_principal')}**")
                objetivo_principal = st.text_area(
                    t('objetivo_principal'),
                    placeholder=t('objetivo_principal_placeholder'),
                    height=80,
                    key=f"obj_principal_{selected_plano}"
                )
                
                st.markdown(f"**📊 {t('metas_especificas')}**")
                metas = st.text_area(
                    t('metas_especificas'),
                    placeholder=t('metas_placeholder'),
                    height=80,
                    key=f"metas_{selected_plano}"
                )
            
            with col2:
                st.markdown(f"**⏱️ {t('prazo_execucao')}**")
                prazo = st.selectbox(
                    t('prazo_execucao'),
                    ["1 semana", "2 semanas", "1 mês", "2 meses", "3 meses"],
                    key=f"prazo_{selected_plano}"
                )
                
                st.markdown(f"**📅 {t('data_inicio')}**")
                data_inicio = st.date_input(
                    t('data_inicio'),
                    value=datetime.now().date(),
                    key=f"data_inicio_{selected_plano}"
                )
            
            st.markdown(f"### 🍽️ {t('intervencoes_nutricionais')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**🥗 {t('recomendacoes_dieteticas')}**")
                recomendacoes = st.text_area(
                    t('recomendacoes_dieteticas'),
                    placeholder=t('recomendacoes_placeholder'),
                    height=100,
                    key=f"recomendacoes_{selected_plano}"
                )
                
                st.markdown(f"**💊 {t('suplementacao_recomendada')}**")
                suplementacao = st.text_area(
                    t('suplementacao_recomendada'),
                    placeholder=t('suplementacao_placeholder'),
                    height=60,
                    key=f"suplementacao_{selected_plano}"
                )
            
            with col2:
                st.markdown(f"**📋 {t('atividades_educativas')}**")
                atividades = st.text_area(
                    t('atividades_educativas'),
                    placeholder=t('atividades_placeholder'),
                    height=100,
                    key=f"atividades_{selected_plano}"
                )
                
                st.markdown(f"**👨‍👩‍👧‍👦 {t('envolvimento_familiar')}**")
                envolvimento = st.text_area(
                    t('envolvimento_familiar'),
                    placeholder=t('envolvimento_placeholder'),
                    height=60,
                    key=f"envolvimento_{selected_plano}"
                )
            
            st.markdown(f"### 📊 {t('monitoramento_avaliacao')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**📅 {t('frequencia_monitoramento')}**")
                frequencia_monitoramento = st.selectbox(
                    t('frequencia_monitoramento'),
                    ["Semanal", "Quinzenal", "Mensal", "Trimestral"],
                    key=f"freq_monitor_{selected_plano}"
                )
            
            with col2:
                st.markdown(f"**📋 {t('indicadores_avaliacao')}**")
                indicadores = st.text_area(
                    t('indicadores_avaliacao'),
                    placeholder=t('indicadores_placeholder'),
                    height=60,
                    key=f"indicadores_{selected_plano}"
                )
            
            st.markdown(f"### 📝 {t('observacoes_finais')}")
            observacoes_plano = st.text_area(
                t('observacoes_finais'),
                placeholder=t('observacoes_plano_placeholder'),
                height=80,
                key=f"obs_plano_{selected_plano}"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.form_submit_button(f"💾 {t('registar_plano')}", use_container_width=True):
                    if objetivo_principal or recomendacoes:
                        novo_plano = {
                            'paciente': selected_plano,
                            'data': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'objetivo_principal': objetivo_principal,
                            'metas': metas,
                            'prazo': prazo,
                            'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                            'recomendacoes_dieteticas': recomendacoes,
                            'suplementacao': suplementacao,
                            'atividades_educativas': atividades,
                            'envolvimento_familiar': envolvimento,
                            'frequencia_monitoramento': frequencia_monitoramento,
                            'indicadores_avaliacao': indicadores,
                            'observacoes': observacoes_plano,
                            'status': 'Ativo'
                        }
                        st.session_state.planos_intervencao.append(novo_plano)
                        st.success(f"✅ {t('plano_registado')} {selected_plano}!")
                        st.balloons()
                    else:
                        st.warning(f"⚠️ {t('preencher_objetivo_recomendacoes')}")
        
        # ===== LISTA DE PLANOS REGISTADOS =====
        st.divider()
        st.subheader(f"📋 {t('planos_registados')}")
        
        planos_paciente = [p for p in st.session_state.planos_intervencao if p['paciente'] == selected_plano]
        
        if planos_paciente:
            for i, plano in enumerate(planos_paciente):
                with st.expander(f"📋 {t('plano')} {i+1} - {plano['data']} - {plano.get('status', 'Ativo')}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**🎯 {t('objetivo_principal')}:** {plano.get('objetivo_principal', 'N/A')}")
                        st.markdown(f"**📊 {t('metas_especificas')}:** {plano.get('metas', 'N/A')}")
                        st.markdown(f"**⏱️ {t('prazo_execucao')}:** {plano.get('prazo', 'N/A')}")
                        st.markdown(f"**📅 {t('data_inicio')}:** {plano.get('data_inicio', 'N/A')}")
                    
                    with col2:
                        st.markdown(f"**🥗 {t('recomendacoes_dieteticas')}:** {plano.get('recomendacoes_dieteticas', 'N/A')}")
                        st.markdown(f"**💊 {t('suplementacao_recomendada')}:** {plano.get('suplementacao', 'N/A')}")
                        st.markdown(f"**📋 {t('atividades_educativas')}:** {plano.get('atividades_educativas', 'N/A')}")
                        st.markdown(f"**📅 {t('frequencia_monitoramento')}:** {plano.get('frequencia_monitoramento', 'N/A')}")
                    
                    st.markdown(f"**📝 {t('observacoes')}:** {plano.get('observacoes', 'N/A')}")
                    
                    st.divider()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if plano.get('status') == 'Ativo':
                            if st.button(f"✅ {t('marcar_concluido')}", key=f"concluir_{i}_{selected_plano}"):
                                st.session_state.planos_intervencao[i]['status'] = 'Concluído'
                                st.rerun()
                    with col2:
                        if st.button(f"🗑️ {t('remover')}", key=f"remover_{i}_{selected_plano}"):
                            st.session_state.planos_intervencao.pop(i)
                            st.rerun()
        else:
            st.info(f"📋 {t('nenhum_plano_registado')}")
    
    # ============================================================
    # ===== TAB 3: DASHBOARD =====
    # ============================================================
    with tab3:
        st.subheader(t('dashboard'))
        
        if not st.session_state.criancas:
            st.info(t('nenhum_paciente'))
            return
        
        df = pd.DataFrame(st.session_state.criancas)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👶 Total", len(df))
        with col2:
            alto_anemia = len(df[df['risco_anemia_nivel'] == 'ALTO'])
            st.metric("🩸 Anemia ALTA", alto_anemia)
        with col3:
            alto_fome = len(df[df['risco_fome_nivel'] == 'ALTO'])
            st.metric("🍽️ Fome Oculta ALTA", alto_fome)
        with col4:
            alto_inseg = len(df[df['risco_inseguranca_nivel'] == 'ALTO'])
            st.metric("🏠 Insegurança ALTA", alto_inseg)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'risco_anemia_nivel' in df.columns:
                fig1 = px.pie(df, names='risco_anemia_nivel', 
                             title=t('distribuicao_risco'),
                             color='risco_anemia_nivel',
                             color_discrete_map={'ALTO': '#c62828', 'MÉDIO': '#ef6c00', 'BAIXO': '#2e7d32'})
                fig1.update_layout(showlegend=True)
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            if 'risco_fome_nivel' in df.columns:
                fig2 = px.pie(df, names='risco_fome_nivel', 
                             title=t('distribuicao_fome'),
                             color='risco_fome_nivel',
                             color_discrete_map={'ALTO': '#c62828', 'MÉDIO': '#ef6c00', 'BAIXO': '#2e7d32'})
                fig2.update_layout(showlegend=True)
                st.plotly_chart(fig2, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            if 'risco_inseguranca_nivel' in df.columns:
                fig3 = px.pie(df, names='risco_inseguranca_nivel', 
                             title=t('distribuicao_inseguranca'),
                             color='risco_inseguranca_nivel',
                             color_discrete_map={'ALTO': '#c62828', 'MÉDIO': '#ef6c00', 'BAIXO': '#2e7d32'})
                fig3.update_layout(showlegend=True)
                st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            if 'dds_calculado' in df.columns:
                fig4 = px.histogram(df, x='dds_calculado', 
                                   title=t('distribuicao_dds'),
                                   nbins=10,
                                   color='risco_anemia_nivel',
                                   color_discrete_map={'ALTO': '#c62828', 'MÉDIO': '#ef6c00', 'BAIXO': '#2e7d32'})
                st.plotly_chart(fig4, use_container_width=True)
        
        st.divider()
        
        # ===== RECOMENDAÇÕES =====
        st.subheader(f"💡 {t('recomendacoes_nutricionais')}")
        
        total_alto = len(df[df['risco_anemia_nivel'] == 'ALTO'])
        total_medio = len(df[df['risco_anemia_nivel'] == 'MÉDIO'])
        total_fome_alto = len(df[df['risco_fome_nivel'] == 'ALTO'])
        total_inseg_alto = len(df[df['risco_inseguranca_nivel'] == 'ALTO'])
        
        if total_alto > 0:
            st.warning(f"🔴 **{total_alto} {t('pacientes_anemia_alta')}** - {t('recomendacao_anemia_alta')}")
        
        if total_medio > 0:
            st.info(f"🟠 **{total_medio} {t('pacientes_anemia_media')}** - {t('recomendacao_anemia_media')}")
        
        if total_fome_alto > 0:
            st.warning(f"🔴 **{total_fome_alto} {t('pacientes_fome_alta')}** - {t('recomendacao_fome_alta')}")
        
        if total_inseg_alto > 0:
            st.warning(f"🔴 **{total_inseg_alto} {t('pacientes_inseguranca_alta')}** - {t('recomendacao_inseguranca_alta')}")
        
        if total_alto == 0 and total_medio == 0 and total_fome_alto == 0 and total_inseg_alto == 0:
            st.success(f"✅ {t('todos_baixo_risco')}")
    
    # ============================================================
    # ===== TAB 4: ENCAMINHAMENTOS =====
    # ============================================================
    with tab4:
        st.subheader(f"📨 {t('encaminhamentos_recebidos')}")
        
        enc_nutri = [e for e in st.session_state.encaminhamentos if 'Nutricionista' in e.get('especialidade', '')]
        
        if not enc_nutri:
            st.info(f"📋 {t('nenhum_encaminhamento_nutricionista')}")
        else:
            pendentes = [e for e in enc_nutri if e.get('status') != 'Concluído']
            atendidos = [e for e in enc_nutri if e.get('status') == 'Concluído']
            
            # ===== ESTATÍSTICAS =====
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"📨 {t('total')}", len(enc_nutri))
            with col2:
                st.metric(f"⏳ {t('pendentes')}", len(pendentes))
            with col3:
                st.metric(f"✅ {t('atendidos')}", len(atendidos))
            
            st.divider()
            
            # ===== LISTA DE PENDENTES =====
            if pendentes:
                st.markdown(f"### ⏳ {t('lista_pendentes')} ({len(pendentes)})")
                
                for enc in pendentes:
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
                            st.markdown(f"**📋 {t('dados_encaminhamento')}**")
                            st.markdown(f"**{t('especialidade')}:** {enc.get('especialidade', 'N/A')}")
                            st.markdown(f"**{t('urgencia')}:** {enc.get('urgencia', 'Normal')}")
                            st.markdown(f"**{t('motivo')}:** {enc.get('motivo', 'N/A')}")
                            st.markdown(f"**{t('status')}:** {enc.get('status', 'Pendente')}")
                            st.markdown(f"**{t('medico_responsavel')}:** {enc.get('medico_responsavel', 'N/A')}")
                        
                        with col2:
                            st.markdown(f"**📊 {t('dados_clinicos')}**")
                            if 'dados_clinicos' in enc and enc['dados_clinicos']:
                                dados = enc['dados_clinicos']
                                st.markdown(f"- Hemoglobina: {dados.get('hemoglobina', 'N/A')} g/dL")
                                st.markdown(f"- {t('tipo_anemia')}: {dados.get('tipo_anemia', 'N/A')}")
                                st.markdown(f"- DDS: {dados.get('dds', 0)}/9")
                                st.markdown(f"- MUAC: {dados.get('muac', 0)} mm")
                        
                        st.divider()
                        if st.button(f"✅ {t('marcar_atendido')} - {enc.get('paciente', '')}"):
                            for e in st.session_state.encaminhamentos:
                                if e.get('paciente') == enc.get('paciente') and e.get('data') == enc.get('data'):
                                    e['status'] = 'Concluído'
                                    st.rerun()
            else:
                st.success(f"✅ {t('todos_atendidos')}")
            
            # ===== LISTA DE ATENDIDOS =====
            if atendidos:
                st.divider()
                st.markdown(f"### ✅ {t('lista_atendidos')} ({len(atendidos)})")
                
                for enc in atendidos:
                    with st.expander(f"✅ 👶 {enc.get('paciente', 'N/A')} - {enc.get('data', 'N/A')}", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**📋 {t('dados_encaminhamento')}**")
                            st.markdown(f"**{t('especialidade')}:** {enc.get('especialidade', 'N/A')}")
                            st.markdown(f"**{t('urgencia')}:** {enc.get('urgencia', 'Normal')}")
                            st.markdown(f"**{t('motivo')}:** {enc.get('motivo', 'N/A')}")
                            st.markdown(f"**{t('status')}:** {enc.get('status', 'Concluído')}")
                            st.markdown(f"**{t('medico_responsavel')}:** {enc.get('medico_responsavel', 'N/A')}")
                        
                        with col2:
                            st.markdown(f"**📊 {t('dados_clinicos')}**")
                            if 'dados_clinicos' in enc and enc['dados_clinicos']:
                                dados = enc['dados_clinicos']
                                st.markdown(f"- Hemoglobina: {dados.get('hemoglobina', 'N/A')} g/dL")
                                st.markdown(f"- {t('tipo_anemia')}: {dados.get('tipo_anemia', 'N/A')}")
                                st.markdown(f"- DDS: {dados.get('dds', 0)}/9")
                                st.markdown(f"- MUAC: {dados.get('muac', 0)} mm")

if __name__ == "__main__":
    render_nutricionista()