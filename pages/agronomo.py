# pages/agronomo.py
# ===== PERFIL AGRÔNOMO - INTERVENÇÃO AGROALIMENTAR =====

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

# ========== FUNÇÕES PARA CALCULAR ÍNDICES ==========
def calcular_indices(respostas):
    """Calcula todos os índices baseado nas respostas do formulário"""
    
    indices = {}
    
    # 1. Índice de Resiliência Climática Agrícola
    resiliencia = 0
    
    if respostas.get('disponibilidade_agua') in ['Suficiente todo o ano', 'Apenas na época chuvosa']:
        resiliencia += 25
    elif respostas.get('disponibilidade_agua') == 'Insuficiente':
        resiliencia += 10
    else:
        resiliencia += 5
    
    if respostas.get('exposicao_climatica') == 'Nenhum':
        resiliencia += 25
    elif respostas.get('exposicao_climatica') in ['Seca', 'Cheias', 'Ciclones']:
        resiliencia += 10
    else:
        resiliencia += 5
    
    if respostas.get('estado_solo') in ['Solo fértil com conservação', 'Solo moderado com alguma conservação']:
        resiliencia += 25
    elif respostas.get('estado_solo') == 'Solo degradado':
        resiliencia += 10
    else:
        resiliencia += 5
    
    if respostas.get('sistema_producao') == 'Produção diversificada com variedades resilientes':
        resiliencia += 25
    elif respostas.get('sistema_producao') == 'Diversificada sem variedades resilientes':
        resiliencia += 15
    elif respostas.get('sistema_producao') == 'Monocultura':
        resiliencia += 10
    else:
        resiliencia += 5
    
    indices['Resiliência Climática'] = min(100, resiliencia)
    
    # 2. Índice de Vulnerabilidade à Seca
    vulnerabilidade_seca = 0
    
    if respostas.get('disponibilidade_agua') in ['Insuficiente', 'Sem fonte permanente de água']:
        vulnerabilidade_seca += 30
    elif respostas.get('disponibilidade_agua') == 'Apenas na época chuvosa':
        vulnerabilidade_seca += 20
    
    if respostas.get('exposicao_climatica') in ['Seca', 'Múltiplos eventos']:
        vulnerabilidade_seca += 30
    
    if respostas.get('estado_solo') in ['Solo degradado', 'Erosão severa sem conservação']:
        vulnerabilidade_seca += 20
    
    if respostas.get('sistema_producao') in ['Monocultura', 'Produção muito reduzida']:
        vulnerabilidade_seca += 20
    
    indices['Vulnerabilidade à Seca'] = min(100, vulnerabilidade_seca)
    
    # 3. Índice de Vulnerabilidade a Cheias
    vulnerabilidade_cheias = 0
    
    if respostas.get('exposicao_climatica') in ['Cheias', 'Múltiplos eventos']:
        vulnerabilidade_cheias += 35
    
    if respostas.get('estado_solo') in ['Solo degradado', 'Erosão severa sem conservação']:
        vulnerabilidade_cheias += 30
    
    if respostas.get('disponibilidade_agua') in ['Insuficiente', 'Sem fonte permanente de água']:
        vulnerabilidade_cheias += 20
    
    if respostas.get('sistema_producao') in ['Monocultura', 'Produção muito reduzida']:
        vulnerabilidade_cheias += 15
    
    indices['Vulnerabilidade a Cheias'] = min(100, vulnerabilidade_cheias)
    
    # 4. Índice de Degradação do Solo
    degradacao_solo = 0
    
    if respostas.get('estado_solo') == 'Erosão severa sem conservação':
        degradacao_solo += 40
    elif respostas.get('estado_solo') == 'Solo degradado':
        degradacao_solo += 30
    elif respostas.get('estado_solo') == 'Solo moderado com alguma conservação':
        degradacao_solo += 15
    
    if respostas.get('sistema_producao') in ['Monocultura', 'Produção muito reduzida']:
        degradacao_solo += 25
    
    if respostas.get('capacidade_adaptativa') == 'Nenhum recurso de adaptação':
        degradacao_solo += 20
    
    if respostas.get('impacto_producao') in ['Perdas >50% ou produção insuficiente', 'Perdas 25–50%']:
        degradacao_solo += 15
    
    indices['Degradação do Solo'] = min(100, degradacao_solo)
    
    # 5. Índice de Segurança Hídrica
    seguranca_hidrica = 0
    
    if respostas.get('disponibilidade_agua') == 'Suficiente todo o ano':
        seguranca_hidrica += 40
    elif respostas.get('disponibilidade_agua') == 'Apenas na época chuvosa':
        seguranca_hidrica += 25
    elif respostas.get('disponibilidade_agua') == 'Insuficiente':
        seguranca_hidrica += 15
    else:
        seguranca_hidrica += 5
    
    if respostas.get('capacidade_adaptativa') in ['Irrigação + assistência técnica + informação climática', 'Apenas um ou dois destes recursos']:
        seguranca_hidrica += 30
    
    if respostas.get('impacto_producao') in ['Produção suficiente sem perdas', 'Perdas <25%']:
        seguranca_hidrica += 30
    elif respostas.get('impacto_producao') == 'Perdas 25–50%':
        seguranca_hidrica += 15
    else:
        seguranca_hidrica += 5
    
    indices['Segurança Hídrica'] = min(100, seguranca_hidrica)
    
    # 6. Índice de Diversificação da Produção
    diversificacao = 0
    
    if respostas.get('sistema_producao') == 'Produção diversificada com variedades resilientes':
        diversificacao += 50
    elif respostas.get('sistema_producao') == 'Diversificada sem variedades resilientes':
        diversificacao += 35
    elif respostas.get('sistema_producao') == 'Monocultura':
        diversificacao += 15
    else:
        diversificacao += 5
    
    if respostas.get('estado_solo') in ['Solo fértil com conservação', 'Solo moderado com alguma conservação']:
        diversificacao += 25
    
    if respostas.get('capacidade_adaptativa') in ['Irrigação + assistência técnica + informação climática', 'Apenas um ou dois destes recursos']:
        diversificacao += 25
    
    indices['Diversificação da Produção'] = min(100, diversificacao)
    
    # 7. Índice de Adoção de Agricultura Inteligente (CSA)
    csa = 0
    
    if respostas.get('estado_solo') in ['Solo fértil com conservação', 'Solo moderado com alguma conservação']:
        csa += 30
    
    if respostas.get('sistema_producao') == 'Produção diversificada com variedades resilientes':
        csa += 30
    elif respostas.get('sistema_producao') == 'Diversificada sem variedades resilientes':
        csa += 15
    
    if respostas.get('capacidade_adaptativa') == 'Irrigação + assistência técnica + informação climática':
        csa += 25
    elif respostas.get('capacidade_adaptativa') == 'Apenas um ou dois destes recursos':
        csa += 15
    
    if respostas.get('impacto_producao') in ['Produção suficiente sem perdas', 'Perdas <25%']:
        csa += 15
    
    indices['Agricultura Inteligente (CSA)'] = min(100, csa)
    
    # 8. Índice de Capacidade Adaptativa da Família
    capacidade_adaptativa = 0
    
    if respostas.get('capacidade_adaptativa') == 'Irrigação + assistência técnica + informação climática':
        capacidade_adaptativa += 50
    elif respostas.get('capacidade_adaptativa') == 'Apenas um ou dois destes recursos':
        capacidade_adaptativa += 30
    else:
        capacidade_adaptativa += 10
    
    if respostas.get('sistema_producao') == 'Produção diversificada com variedades resilientes':
        capacidade_adaptativa += 25
    
    if respostas.get('estado_solo') in ['Solo fértil com conservação', 'Solo moderado com alguma conservação']:
        capacidade_adaptativa += 25
    
    indices['Capacidade Adaptativa'] = min(100, capacidade_adaptativa)
    
    # 9. Índice de Risco Agroalimentar
    risco_agro = 0
    
    if respostas.get('impacto_producao') == 'Perdas >50% ou produção insuficiente':
        risco_agro += 40
    elif respostas.get('impacto_producao') == 'Perdas 25–50%':
        risco_agro += 30
    elif respostas.get('impacto_producao') == 'Perdas <25%':
        risco_agro += 15
    
    if respostas.get('exposicao_climatica') in ['Seca', 'Cheias', 'Ciclones', 'Múltiplos eventos']:
        risco_agro += 25
    
    if respostas.get('disponibilidade_agua') in ['Insuficiente', 'Sem fonte permanente de água']:
        risco_agro += 20
    
    if respostas.get('sistema_producao') in ['Monocultura', 'Produção muito reduzida']:
        risco_agro += 15
    
    indices['Risco Agroalimentar'] = min(100, risco_agro)
    
    # 10. Índice Integrado One Health/Nexus
    one_health = 0
    
    if indices['Resiliência Climática'] >= 50:
        one_health += 15
    if indices['Segurança Hídrica'] >= 50:
        one_health += 15
    if indices['Diversificação da Produção'] >= 50:
        one_health += 15
    if indices['Capacidade Adaptativa'] >= 50:
        one_health += 15
    if indices['Agricultura Inteligente (CSA)'] >= 50:
        one_health += 15
    
    if respostas.get('capacidade_adaptativa') in ['Irrigação + assistência técnica + informação climática', 'Apenas um ou dois destes recursos']:
        one_health += 15
    
    if respostas.get('estado_solo') in ['Solo fértil com conservação', 'Solo moderado com alguma conservação']:
        one_health += 10
    
    indices['Índice Integrado One Health/Nexus'] = min(100, one_health)
    
    return indices

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
def render_agronomo():
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
    
    # ===== PLANOS DE INTERVENÇÃO AGRONÔMICA =====
    if 'planos_intervencao_agro' not in st.session_state:
        st.session_state.planos_intervencao_agro = []
    
    st.title(f"👨🏾🌾 {t('agronomo_titulo')}")
    st.markdown(f"""
    <p style='color: #555; margin-bottom: 2rem;'>
    {t('descricao_agronomo')}
    </p>
    """, unsafe_allow_html=True)
    
    # ===== ESTATÍSTICAS =====
    total = len(st.session_state.criancas)
    enc_agro = [e for e in st.session_state.encaminhamentos if 'Agrônomo' in e.get('especialidade', '')]
    pendentes = len([e for e in enc_agro if e.get('status') != 'Concluído'])
    atendidos = len([e for e in enc_agro if e.get('status') == 'Concluído'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(f"👶 {t('total_pacientes')}", total)
    with col2:
        st.metric(f"📨 {t('encaminhamentos')}", len(enc_agro))
    with col3:
        st.metric(f"⏳ {t('pendentes')}", pendentes)
    with col4:
        st.metric(f"✅ {t('atendidos')}", atendidos)
    
    st.markdown("---")
    
    # ============================================================
    # ===== ABAS =====
    # ============================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Avaliação",
        "📝 Plano de Intervenção",
        "📊 Índices",
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
            
            st.markdown(f"#### 🌾 {t('producao_familiar')}")
            st.markdown(f"**{t('producao_familiar')}:** {patient_data.get('producao_familiar', 'N/A')}")
            st.markdown(f"**{t('acesso_terra')}:** {patient_data.get('acesso_terra', 'N/A')}")
            st.markdown(f"**{t('fonte_agua')}:** {patient_data.get('fonte_agua', 'N/A')}")
            st.markdown(f"**{t('culturas_produzidas')}:** {patient_data.get('culturas_produzidas', 'N/A')}")
        
        st.divider()
        
        # ===== DIFICULDADES =====
        st.markdown(f"#### 🌾 {t('dificuldades_producao')}")
        dificuldades = patient_data.get('dificuldades_producao', 'N/A')
        if dificuldades and dificuldades != 'N/A':
            for d in dificuldades.split(','):
                st.markdown(f"- {d.strip()}")
        else:
            st.info(t('nenhuma_dificuldade'))
        
        st.divider()
        
        # ===== FORMULÁRIO DE AVALIAÇÃO AGROALIMENTAR =====
        st.markdown(f"### 🌾 {t('avaliacao_resiliencia')}")
        st.markdown(t('descricao_resiliencia'))
        
        if 'respostas_agro' not in st.session_state:
            st.session_state.respostas_agro = {}
        
        with st.form("form_avaliacao_agro"):
            st.markdown(f"#### 💧 1. {t('pergunta_disponibilidade_agua')}")
            disponibilidade_agua = st.selectbox(
                t('selecione_opcao'),
                ["Suficiente todo o ano", "Apenas na época chuvosa", "Insuficiente", "Sem fonte permanente de água"],
                key="disponibilidade_agua"
            )
            
            st.markdown(f"#### 🌪️ 2. {t('pergunta_exposicao_climatica')}")
            exposicao_climatica = st.selectbox(
                t('selecione_opcao'),
                ["Nenhum", "Seca", "Cheias", "Ciclones", "Múltiplos eventos"],
                key="exposicao_climatica"
            )
            
            st.markdown(f"#### 🌱 3. {t('pergunta_estado_solo')}")
            estado_solo = st.selectbox(
                t('selecione_opcao'),
                ["Solo fértil com conservação", "Solo moderado com alguma conservação", "Solo degradado", "Erosão severa sem conservação"],
                key="estado_solo"
            )
            
            st.markdown(f"#### 🌾 4. {t('pergunta_sistema_producao')}")
            sistema_producao = st.selectbox(
                t('selecione_opcao'),
                ["Produção diversificada com variedades resilientes", "Diversificada sem variedades resilientes", "Monocultura", "Produção muito reduzida"],
                key="sistema_producao"
            )
            
            st.markdown(f"#### 🧠 5. {t('pergunta_capacidade_adaptativa')}")
            capacidade_adaptativa = st.selectbox(
                t('selecione_opcao'),
                ["Irrigação + assistência técnica + informação climática", "Apenas um ou dois destes recursos", "Nenhum recurso de adaptação"],
                key="capacidade_adaptativa"
            )
            
            st.markdown(f"#### 🍽️ 6. {t('pergunta_impacto_producao')}")
            impacto_producao = st.selectbox(
                t('selecione_opcao'),
                ["Produção suficiente sem perdas", "Perdas <25%", "Perdas 25–50%", "Perdas >50% ou produção insuficiente"],
                key="impacto_producao"
            )
            
            st.markdown("---")
            st.caption(f"📊 {t('legenda_calcular_indices')}")
            
            if st.form_submit_button(f"📊 {t('calcular_indices')}", use_container_width=True):
                respostas = {
                    'disponibilidade_agua': disponibilidade_agua,
                    'exposicao_climatica': exposicao_climatica,
                    'estado_solo': estado_solo,
                    'sistema_producao': sistema_producao,
                    'capacidade_adaptativa': capacidade_adaptativa,
                    'impacto_producao': impacto_producao,
                    'fonte_agua': patient_data.get('fonte_agua', 'N/A')
                }
                
                st.session_state.respostas_agro = respostas
                indices = calcular_indices(respostas)
                st.session_state.indices_agro = indices
                
                st.success(f"✅ {t('indices_calculados')}")
                st.rerun()
    
    # ============================================================
    # ===== TAB 2: PLANO DE INTERVENÇÃO AGRONÔMICA =====
    # ============================================================
    with tab2:
        st.subheader(f"📝 {t('plano_intervencao_agronomica')}")
        
        if not st.session_state.criancas:
            st.info(t('nenhum_paciente'))
            return
        
        df = pd.DataFrame(st.session_state.criancas)
        selected_plano = st.selectbox(
            f"{t('selecionar_paciente')}:",
            df['nome_completo'].unique().tolist(),
            key="select_plano_agro"
        )
        
        patient_data_plano = df[df['nome_completo'] == selected_plano].iloc[0]
        
        st.markdown(f"#### 👶 {patient_data_plano['nome_completo']}")
        st.markdown(f"**{t('idade')}:** {patient_data_plano['idade_meses']} {t('meses')}")
        st.markdown(f"**📍 {t('provincia')}:** {patient_data_plano.get('provincia', 'N/A')}")
        st.markdown(f"**🌾 {t('producao_familiar')}:** {patient_data_plano.get('producao_familiar', 'N/A')}")
        
        st.divider()
        
        with st.form("plano_intervencao_agro_form"):
            st.markdown(f"### 🎯 {t('objetivos_intervencao_agro')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**📋 {t('objetivo_principal_agro')}**")
                objetivo_principal = st.text_area(
                    t('objetivo_principal_agro'),
                    placeholder=t('objetivo_principal_agro_placeholder'),
                    height=80,
                    key=f"obj_principal_agro_{selected_plano}"
                )
                
                st.markdown(f"**📊 {t('metas_especificas_agro')}**")
                metas = st.text_area(
                    t('metas_especificas_agro'),
                    placeholder=t('metas_agro_placeholder'),
                    height=80,
                    key=f"metas_agro_{selected_plano}"
                )
            
            with col2:
                st.markdown(f"**⏱️ {t('prazo_execucao_agro')}**")
                prazo = st.selectbox(
                    t('prazo_execucao_agro'),
                    ["1 mês", "2 meses", "3 meses", "6 meses", "1 ano"],
                    key=f"prazo_agro_{selected_plano}"
                )
                
                st.markdown(f"**📅 {t('data_inicio_agro')}**")
                data_inicio = st.date_input(
                    t('data_inicio_agro'),
                    value=datetime.now().date(),
                    key=f"data_inicio_agro_{selected_plano}"
                )
            
            st.markdown(f"### 🌾 {t('intervencoes_agronomicas')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**🌱 {t('praticas_agricolas_recomendadas')}**")
                praticas_agricolas = st.text_area(
                    t('praticas_agricolas_recomendadas'),
                    placeholder=t('praticas_agricolas_placeholder'),
                    height=100,
                    key=f"praticas_{selected_plano}"
                )
                
                st.markdown(f"**🌿 {t('culturas_recomendadas')}**")
                culturas = st.text_area(
                    t('culturas_recomendadas'),
                    placeholder=t('culturas_placeholder'),
                    height=60,
                    key=f"culturas_{selected_plano}"
                )
            
            with col2:
                st.markdown(f"**💧 {t('recomendacoes_agua')}**")
                recomendacoes_agua = st.text_area(
                    t('recomendacoes_agua'),
                    placeholder=t('recomendacoes_agua_placeholder'),
                    height=100,
                    key=f"recomendacoes_agua_{selected_plano}"
                )
                
                st.markdown(f"**🧑‍🌾 {t('formacao_tecnica')}**")
                formacao = st.text_area(
                    t('formacao_tecnica'),
                    placeholder=t('formacao_tecnica_placeholder'),
                    height=60,
                    key=f"formacao_{selected_plano}"
                )
            
            st.markdown(f"### 📊 {t('monitoramento_avaliacao_agro')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**📅 {t('frequencia_monitoramento_agro')}**")
                frequencia_monitoramento = st.selectbox(
                    t('frequencia_monitoramento_agro'),
                    ["Semanal", "Quinzenal", "Mensal", "Trimestral"],
                    key=f"freq_monitor_agro_{selected_plano}"
                )
            
            with col2:
                st.markdown(f"**📋 {t('indicadores_avaliacao_agro')}**")
                indicadores = st.text_area(
                    t('indicadores_avaliacao_agro'),
                    placeholder=t('indicadores_agro_placeholder'),
                    height=60,
                    key=f"indicadores_agro_{selected_plano}"
                )
            
            st.markdown(f"### 📝 {t('observacoes_finais_agro')}")
            observacoes_plano = st.text_area(
                t('observacoes_finais_agro'),
                placeholder=t('observacoes_agro_placeholder'),
                height=80,
                key=f"obs_plano_agro_{selected_plano}"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.form_submit_button(f"💾 {t('registar_plano_agro')}", use_container_width=True):
                    if objetivo_principal or praticas_agricolas:
                        novo_plano = {
                            'paciente': selected_plano,
                            'data': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'objetivo_principal': objetivo_principal,
                            'metas': metas,
                            'prazo': prazo,
                            'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                            'praticas_agricolas': praticas_agricolas,
                            'culturas': culturas,
                            'recomendacoes_agua': recomendacoes_agua,
                            'formacao': formacao,
                            'frequencia_monitoramento': frequencia_monitoramento,
                            'indicadores': indicadores,
                            'observacoes': observacoes_plano,
                            'status': 'Ativo'
                        }
                        st.session_state.planos_intervencao_agro.append(novo_plano)
                        st.success(f"✅ {t('plano_registado_agro')} {selected_plano}!")
                        st.balloons()
                    else:
                        st.warning(f"⚠️ {t('preencher_objetivo_praticas')}")
        
        # ===== LISTA DE PLANOS REGISTADOS =====
        st.divider()
        st.subheader(f"📋 {t('planos_registados_agro')}")
        
        planos_paciente = [p for p in st.session_state.planos_intervencao_agro if p['paciente'] == selected_plano]
        
        if planos_paciente:
            for i, plano in enumerate(planos_paciente):
                with st.expander(f"📋 {t('plano')} {i+1} - {plano['data']} - {plano.get('status', 'Ativo')}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**🎯 {t('objetivo_principal_agro')}:** {plano.get('objetivo_principal', 'N/A')}")
                        st.markdown(f"**📊 {t('metas_especificas_agro')}:** {plano.get('metas', 'N/A')}")
                        st.markdown(f"**⏱️ {t('prazo_execucao_agro')}:** {plano.get('prazo', 'N/A')}")
                        st.markdown(f"**📅 {t('data_inicio_agro')}:** {plano.get('data_inicio', 'N/A')}")
                    
                    with col2:
                        st.markdown(f"**🌱 {t('praticas_agricolas_recomendadas')}:** {plano.get('praticas_agricolas', 'N/A')}")
                        st.markdown(f"**🌿 {t('culturas_recomendadas')}:** {plano.get('culturas', 'N/A')}")
                        st.markdown(f"**💧 {t('recomendacoes_agua')}:** {plano.get('recomendacoes_agua', 'N/A')}")
                        st.markdown(f"**📅 {t('frequencia_monitoramento_agro')}:** {plano.get('frequencia_monitoramento', 'N/A')}")
                    
                    st.markdown(f"**📝 {t('observacoes')}:** {plano.get('observacoes', 'N/A')}")
                    
                    st.divider()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if plano.get('status') == 'Ativo':
                            if st.button(f"✅ {t('marcar_concluido')}", key=f"concluir_agro_{i}_{selected_plano}"):
                                st.session_state.planos_intervencao_agro[i]['status'] = 'Concluído'
                                st.rerun()
                    with col2:
                        if st.button(f"🗑️ {t('remover')}", key=f"remover_agro_{i}_{selected_plano}"):
                            st.session_state.planos_intervencao_agro.pop(i)
                            st.rerun()
        else:
            st.info(f"📋 {t('nenhum_plano_registado_agro')}")
    
    # ============================================================
    # ===== TAB 3: ÍNDICES =====
    # ============================================================
    with tab3:
        if 'indices_agro' in st.session_state and st.session_state.indices_agro:
            st.subheader(f"📊 {t('resultados_indices')}")
            
            indices = st.session_state.indices_agro
            
            col1, col2, col3 = st.columns(3)
            
            def card_style(valor, titulo, descricao, icone):
                if valor >= 60:
                    bg = "#c8e6c9"
                    border = "#2e7d32"
                    texto = "✅ Bom"
                elif valor >= 40:
                    bg = "#ffe0b2"
                    border = "#ef6c00"
                    texto = "⚠️ Médio"
                else:
                    bg = "#ffcdd2"
                    border = "#c62828"
                    texto = "🔴 Baixo"
                
                return f"""
                <div style="background: {bg}; padding: 15px; border-radius: 10px; margin: 8px 0; border-left: 5px solid {border};">
                    <h4>{icone} {titulo}</h4>
                    <h2 style="text-align: center;">{valor}%</h2>
                    <p style="font-size: 0.8rem; color: #555;">{descricao}</p>
                    <p style="font-size: 0.8rem; font-weight: bold; color: {border};">{texto}</p>
                </div>
                """
            
            with col1:
                st.markdown(card_style(indices['Resiliência Climática'], "Resiliência Climática", "Capacidade de recuperação", "🔄"), unsafe_allow_html=True)
                st.markdown(card_style(indices['Segurança Hídrica'], "Segurança Hídrica", "Disponibilidade de água", "💧"), unsafe_allow_html=True)
                st.markdown(card_style(indices['Agricultura Inteligente (CSA)'], "Agricultura Inteligente", "Práticas sustentáveis", "🌱"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(card_style(indices['Diversificação da Produção'], "Diversificação", "Número de culturas", "🌾"), unsafe_allow_html=True)
                st.markdown(card_style(indices['Capacidade Adaptativa'], "Capacidade Adaptativa", "Adaptação às mudanças", "🧠"), unsafe_allow_html=True)
                st.markdown(card_style(indices['Índice Integrado One Health/Nexus'], "One Health/Nexus", "Integração saúde-agricultura", "🔄"), unsafe_allow_html=True)
            
            with col3:
                vul_seca = indices['Vulnerabilidade à Seca']
                bg = "#c8e6c9" if vul_seca <= 40 else "#ffe0b2" if vul_seca <= 60 else "#ffcdd2"
                border = "#2e7d32" if vul_seca <= 40 else "#ef6c00" if vul_seca <= 60 else "#c62828"
                st.markdown(f"""
                <div style="background: {bg}; padding: 15px; border-radius: 10px; margin: 8px 0; border-left: 5px solid {border};">
                    <h4>☀️ Vulnerabilidade à Seca</h4>
                    <h2 style="text-align: center;">{vul_seca}%</h2>
                    <p style="font-size: 0.8rem; color: #555;">Quanto menor, melhor</p>
                </div>
                """, unsafe_allow_html=True)
                
                vul_cheias = indices['Vulnerabilidade a Cheias']
                bg = "#c8e6c9" if vul_cheias <= 40 else "#ffe0b2" if vul_cheias <= 60 else "#ffcdd2"
                border = "#2e7d32" if vul_cheias <= 40 else "#ef6c00" if vul_cheias <= 60 else "#c62828"
                st.markdown(f"""
                <div style="background: {bg}; padding: 15px; border-radius: 10px; margin: 8px 0; border-left: 5px solid {border};">
                    <h4>🌊 Vulnerabilidade a Cheias</h4>
                    <h2 style="text-align: center;">{vul_cheias}%</h2>
                    <p style="font-size: 0.8rem; color: #555;">Quanto menor, melhor</p>
                </div>
                """, unsafe_allow_html=True)
                
                degradacao = indices['Degradação do Solo']
                bg = "#c8e6c9" if degradacao <= 40 else "#ffe0b2" if degradacao <= 60 else "#ffcdd2"
                border = "#2e7d32" if degradacao <= 40 else "#ef6c00" if degradacao <= 60 else "#c62828"
                st.markdown(f"""
                <div style="background: {bg}; padding: 15px; border-radius: 10px; margin: 8px 0; border-left: 5px solid {border};">
                    <h4>🏜️ Degradação do Solo</h4>
                    <h2 style="text-align: center;">{degradacao}%</h2>
                    <p style="font-size: 0.8rem; color: #555;">Quanto menor, melhor</p>
                </div>
                """, unsafe_allow_html=True)
                
                risco = indices['Risco Agroalimentar']
                bg = "#c8e6c9" if risco <= 40 else "#ffe0b2" if risco <= 60 else "#ffcdd2"
                border = "#2e7d32" if risco <= 40 else "#ef6c00" if risco <= 60 else "#c62828"
                st.markdown(f"""
                <div style="background: {bg}; padding: 15px; border-radius: 10px; margin: 8px 0; border-left: 5px solid {border};">
                    <h4>⚠️ Risco Agroalimentar</h4>
                    <h2 style="text-align: center;">{risco}%</h2>
                    <p style="font-size: 0.8rem; color: #555;">Quanto menor, melhor</p>
                </div>
                """, unsafe_allow_html=True)
            
            # ===== RECOMENDAÇÕES =====
            st.divider()
            st.markdown(f"### 💡 {t('recomendacoes')}")
            
            indices = st.session_state.indices_agro
            recomendacoes = []
            
            if indices['Resiliência Climática'] < 50:
                recomendacoes.append("🔴 **Baixa Resiliência Climática:** Implementar sistemas de irrigação e diversificar culturas para reduzir riscos.")
            
            if indices['Segurança Hídrica'] < 50:
                recomendacoes.append("🟠 **Insegurança Hídrica:** Investir em captação de água da chuva e sistemas de irrigação eficientes.")
            
            if indices['Diversificação da Produção'] < 50:
                recomendacoes.append("🟠 **Baixa Diversificação:** Aumentar o número de culturas para melhorar a segurança alimentar.")
            
            if indices['Vulnerabilidade à Seca'] > 60:
                recomendacoes.append("🔴 **Alta Vulnerabilidade à Seca:** Plantar variedades resistentes à seca e implementar sistemas de armazenamento de água.")
            
            if indices['Vulnerabilidade a Cheias'] > 60:
                recomendacoes.append("🔴 **Alta Vulnerabilidade a Cheias:** Melhorar a drenagem e plantar em áreas menos sujeitas a inundações.")
            
            if indices['Degradação do Solo'] > 60:
                recomendacoes.append("🔴 **Degradação do Solo:** Implementar práticas de conservação como rotação de culturas e adubação orgânica.")
            
            if indices['Agricultura Inteligente (CSA)'] < 50:
                recomendacoes.append("🟠 **Baixa Adoção de CSA:** Adotar práticas de agricultura sustentável e usar previsões meteorológicas.")
            
            if indices['Capacidade Adaptativa'] < 50:
                recomendacoes.append("🟠 **Baixa Capacidade Adaptativa:** Buscar assistência técnica e formar-se em práticas agrícolas resilientes.")
            
            if indices['Risco Agroalimentar'] > 60:
                recomendacoes.append("🔴 **Alto Risco Agroalimentar:** Diversificar fontes de renda e melhorar o armazenamento pós-colheita.")
            
            if indices['Índice Integrado One Health/Nexus'] < 50:
                recomendacoes.append("🟠 **Baixa Integração One Health:** Promover sinergias entre saúde, agricultura e ambiente.")
            
            if not recomendacoes:
                recomendacoes.append("✅ **Boa resiliência agroalimentar!** A família apresenta boas práticas de adaptação climática.")
            
            for rec in recomendacoes:
                st.info(rec)
        else:
            st.info("📋 Nenhum índice calculado. Preencha a avaliação agroalimentar na aba 'Avaliação'.")
    
    # ============================================================
    # ===== TAB 4: DASHBOARD =====
    # ============================================================
    with tab4:
        st.subheader(t('dashboard'))
        
        if not st.session_state.criancas:
            st.info(t('nenhum_paciente'))
            return
        
        df = pd.DataFrame(st.session_state.criancas)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👶 Total", len(df))
        with col2:
            producao = len(df[df['producao_familiar'] != 'Não produz'])
            st.metric("🌾 Produção Familiar", producao)
        with col3:
            terra = len(df[df['acesso_terra'] != 'Não tem terra'])
            st.metric("🏠 Acesso à Terra", terra)
        with col4:
            agua = len(df[df['fonte_agua'] != 'Nenhuma'])
            st.metric("💧 Fonte de Água", agua)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'producao_familiar' in df.columns:
                fig1 = px.pie(df, names='producao_familiar', title=t('producao_familiar'))
                fig1.update_layout(showlegend=True)
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            if 'acesso_terra' in df.columns:
                fig2 = px.pie(df, names='acesso_terra', title=t('acesso_terra'))
                fig2.update_layout(showlegend=True)
                st.plotly_chart(fig2, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            if 'fonte_agua' in df.columns:
                fig3 = px.pie(df, names='fonte_agua', title=t('fonte_agua'))
                fig3.update_layout(showlegend=True)
                st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            if 'culturas_produzidas' in df.columns:
                culturas_counts = df['culturas_produzidas'].value_counts().head(5)
                if not culturas_counts.empty:
                    fig4 = px.bar(x=culturas_counts.values, y=culturas_counts.index,
                                orientation='h', title=t('culturas_produzidas'))
                    st.plotly_chart(fig4, use_container_width=True)
        
        st.divider()
        
        # ===== RECOMENDAÇÕES AGROALIMENTARES =====
        st.subheader(f"💡 {t('recomendacoes_agroalimentares')}")
        
        total_producao = len(df[df['producao_familiar'] != 'Não produz'])
        total_terra = len(df[df['acesso_terra'] != 'Não tem terra'])
        total_agua = len(df[df['fonte_agua'] != 'Nenhuma'])
        
        if total_producao < total * 0.5:
            st.warning(f"🔴 **{total - total_producao} famílias não produzem alimentos** - Incentivar produção familiar para segurança alimentar.")
        
        if total_terra < total * 0.5:
            st.warning(f"🔴 **{total - total_terra} famílias não têm acesso à terra** - Avaliar programas de acesso à terra.")
        
        if total_agua < total * 0.5:
            st.warning(f"🔴 **{total - total_agua} famílias não têm fonte de água** - Implementar sistemas de captação de água.")
        
        if 'dificuldades_producao' in df.columns:
            dificuldades_counts = df['dificuldades_producao'].value_counts()
            if not dificuldades_counts.empty:
                top_dificuldade = dificuldades_counts.index[0]
                st.info(f"🟠 **Principal dificuldade:** {top_dificuldade} - {dificuldades_counts.iloc[0]} famílias")
        
        if total_producao >= total * 0.7 and total_terra >= total * 0.7 and total_agua >= total * 0.7:
            st.success("✅ Boa resiliência agroalimentar! As famílias têm boas condições de produção.")
    
    # ============================================================
    # ===== TAB 5: ENCAMINHAMENTOS =====
    # ============================================================
    with tab5:
        st.subheader(f"📨 {t('encaminhamentos_recebidos')}")
        
        enc_agro = [e for e in st.session_state.encaminhamentos if 'Agrônomo' in e.get('especialidade', '')]
        
        if not enc_agro:
            st.info(f"📋 {t('nenhum_encaminhamento_agronomo')}")
        else:
            pendentes = [e for e in enc_agro if e.get('status') != 'Concluído']
            atendidos = [e for e in enc_agro if e.get('status') == 'Concluído']
            
            # ===== ESTATÍSTICAS =====
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"📨 {t('total')}", len(enc_agro))
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
                            st.markdown(f"**📊 {t('dados_agroalimentares')}**")
                            if 'dados_clinicos' in enc and enc['dados_clinicos']:
                                dados = enc['dados_clinicos']
                                st.markdown(f"- DDS: {dados.get('dds', 0)}/9")
                                st.markdown(f"- MUAC: {dados.get('muac', 0)} mm")
                                st.markdown(f"- {t('producao_familiar')}: {dados.get('producao_familiar', 'N/A')}")
                                st.markdown(f"- {t('acesso_terra')}: {dados.get('acesso_terra', 'N/A')}")
                                st.markdown(f"- {t('dificuldades_producao')}: {dados.get('dificuldades_producao', 'N/A')}")
                        
                        if enc.get('status') == 'Pendente':
                            st.divider()
                            if st.button(f"✅ {t('marcar_atendido')} - {enc.get('paciente', '')}"):
                                for e in st.session_state.encaminhamentos:
                                    if e.get('paciente') == enc.get('paciente') and e.get('data') == enc.get('data'):
                                        e['status'] = 'Concluído'
                                        st.rerun()
            else:
                st.success(f"✅ {t('todos_atendidos_agro')}")
            
            # ===== LISTA DE ATENDIDOS =====
            if atendidos:
                st.divider()
                st.markdown(f"### ✅ {t('lista_atendidos_agro')} ({len(atendidos)})")
                
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
                            st.markdown(f"**📊 {t('dados_agroalimentares')}**")
                            if 'dados_clinicos' in enc and enc['dados_clinicos']:
                                dados = enc['dados_clinicos']
                                st.markdown(f"- DDS: {dados.get('dds', 0)}/9")
                                st.markdown(f"- MUAC: {dados.get('muac', 0)} mm")
                                st.markdown(f"- {t('producao_familiar')}: {dados.get('producao_familiar', 'N/A')}")
                                st.markdown(f"- {t('acesso_terra')}: {dados.get('acesso_terra', 'N/A')}")

if __name__ == "__main__":
    render_agronomo()