# pages/agronomo.py
# ===== PERFIL AGRÔNOMO - INTERVENÇÃO AGROALIMENTAR =====

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import base64
import time

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

# ========== FUNÇÕES PARA CALCULAR ÍNDICES ==========
def calcular_indices(respostas):
    """Calcula todos os índices baseado nas respostas do formulário"""
    
    indices = {}
    
    # 1. Índice de Resiliência Climática Agrícola
    resiliencia = 0
    
    # Disponibilidade de água
    if respostas.get('disponibilidade_agua') in ['Suficiente todo o ano', 'Apenas na época chuvosa']:
        resiliencia += 25
    elif respostas.get('disponibilidade_agua') == 'Insuficiente':
        resiliencia += 10
    else:
        resiliencia += 5
    
    # Eventos climáticos
    if respostas.get('exposicao_climatica') == 'Nenhum':
        resiliencia += 25
    elif respostas.get('exposicao_climatica') == 'Seca':
        resiliencia += 10
    elif respostas.get('exposicao_climatica') == 'Cheias':
        resiliencia += 10
    elif respostas.get('exposicao_climatica') == 'Ciclones':
        resiliencia += 10
    else:  # Múltiplos eventos
        resiliencia += 5
    
    # Estado do solo
    if respostas.get('estado_solo') in ['Solo fértil com conservação', 'Solo moderado com alguma conservação']:
        resiliencia += 25
    elif respostas.get('estado_solo') == 'Solo degradado':
        resiliencia += 10
    else:  # Erosão severa
        resiliencia += 5
    
    # Sistema de produção
    if respostas.get('sistema_producao') == 'Produção diversificada com variedades resilientes':
        resiliencia += 25
    elif respostas.get('sistema_producao') == 'Diversificada sem variedades resilientes':
        resiliencia += 15
    elif respostas.get('sistema_producao') == 'Monocultura':
        resiliencia += 10
    else:  # Produção muito reduzida
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

# ========== FUNÇÃO PRINCIPAL ==========
def render_agronomo():
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
    
    st.title("👨🏾🌾 Agrônomo - Intervenção Agroalimentar")
    st.markdown("""
    <p style='color: #555; margin-bottom: 2rem;'>
    Avaliação agroalimentar, resiliência climática e recomendações para famílias encaminhadas pelo médico.
    </p>
    """, unsafe_allow_html=True)
    
    # ===== ESTATÍSTICAS =====
    total = len(st.session_state.criancas)
    enc_agro = [e for e in st.session_state.encaminhamentos if 'Agrônomo' in e.get('especialidade', '')]
    pendentes = len([e for e in enc_agro if e.get('status') != 'Concluído'])
    atendidos = len([e for e in enc_agro if e.get('status') == 'Concluído'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👶 Total Pacientes", total)
    with col2:
        st.metric("📨 Encaminhamentos", len(enc_agro))
    with col3:
        st.metric("⏳ Pendentes", pendentes)
    with col4:
        st.metric("✅ Atendidos", atendidos)
    
    st.markdown("---")
    
    # ============================================================
    # ===== SELEÇÃO DE PACIENTE =====
    # ============================================================
    st.subheader("👤 Selecionar Paciente")
    
    if not st.session_state.criancas:
        st.info("📋 Nenhum paciente registado no sistema.")
        return
    
    df = pd.DataFrame(st.session_state.criancas)
    selected = st.selectbox(
        "Selecione um paciente:",
        df['nome_completo'].unique().tolist()
    )
    
    patient_data = df[df['nome_completo'] == selected].iloc[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Dados do Paciente")
        st.markdown(f"**👶 Nome:** {patient_data['nome_completo']}")
        st.markdown(f"**📏 Idade:** {patient_data['idade_meses']} meses")
        st.markdown(f"**⚖️ Peso:** {patient_data['peso']} kg")
        st.markdown(f"**📐 Altura:** {patient_data['altura']} cm")
        st.markdown(f"**📏 MUAC:** {patient_data['muac']} mm")
        st.markdown(f"**📊 DDS:** {patient_data.get('dds_calculado', 0)}/9")
        st.markdown(f"**📍 Província:** {patient_data.get('provincia', 'N/A')}")
        st.markdown(f"**📍 Distrito:** {patient_data.get('distrito', 'N/A')}")
    
    with col2:
        st.markdown("#### 🩺 Risco")
        risco = patient_data.get('risco_anemia_nivel', 'N/A')
        cor = "🔴" if risco == "ALTO" else "🟡" if risco == "MÉDIO" else "🟢"
        st.metric("Risco de Anemia", f"{cor} {risco}")
        st.metric("Fome Oculta", patient_data.get('risco_fome_nivel', 'N/A'))
        st.metric("Insegurança Alimentar", patient_data.get('risco_inseguranca_nivel', 'N/A'))
        
        st.markdown("#### 🌾 Produção Agrícola")
        st.markdown(f"**Produção:** {patient_data.get('producao_familiar', 'N/A')}")
        st.markdown(f"**Terra:** {patient_data.get('acesso_terra', 'N/A')}")
        st.markdown(f"**Água:** {patient_data.get('fonte_agua', 'N/A')}")
        st.markdown(f"**Culturas:** {patient_data.get('culturas_produzidas', 'N/A')}")
    
    # ============================================================
    # ===== DIFICULDADES =====
    # ============================================================
    st.divider()
    st.markdown("#### 🌾 Dificuldades na Produção")
    dificuldades = patient_data.get('dificuldades_producao', 'N/A')
    if dificuldades and dificuldades != 'N/A':
        for d in dificuldades.split(','):
            st.markdown(f"- {d.strip()}")
    else:
        st.info("Nenhuma dificuldade registada")
    
    # ============================================================
    # ===== FORMULÁRIO DE AVALIAÇÃO AGROALIMENTAR COMPLETO =====
    # ============================================================
    st.divider()
    st.markdown("### 🌾 Avaliação de Resiliência Agroalimentar")
    st.markdown("Preencha o formulário para avaliar a resiliência climática e produtiva da família.")
    
    # Inicializar respostas no session state
    if 'respostas_agro' not in st.session_state:
        st.session_state.respostas_agro = {}
    
    with st.form("form_avaliacao_agro"):
        # ===== 1. DISPONIBILIDADE DE ÁGUA =====
        st.markdown("#### 💧 1. Qual é a disponibilidade de água para a produção agrícola?")
        disponibilidade_agua = st.selectbox(
            "Selecione a opção:",
            ["Suficiente todo o ano", "Apenas na época chuvosa", "Insuficiente", "Sem fonte permanente de água"],
            key="disponibilidade_agua"
        )
        
        # ===== 2. EXPOSIÇÃO A EVENTOS CLIMÁTICOS =====
        st.markdown("#### 🌪️ 2. Como classifica a exposição da exploração agrícola a eventos climáticos nos últimos 5 anos?")
        exposicao_climatica = st.selectbox(
            "Selecione a opção:",
            ["Nenhum", "Seca", "Cheias", "Ciclones", "Múltiplos eventos"],
            key="exposicao_climatica"
        )
        
        # ===== 3. ESTADO DO SOLO E PRÁTICAS DE CONSERVAÇÃO =====
        st.markdown("#### 🌱 3. Qual é o estado atual do solo e as práticas de conservação?")
        estado_solo = st.selectbox(
            "Selecione a opção:",
            ["Solo fértil com conservação", "Solo moderado com alguma conservação", "Solo degradado", "Erosão severa sem conservação"],
            key="estado_solo"
        )
        
        # ===== 4. SISTEMA DE PRODUÇÃO AGRÍCOLA =====
        st.markdown("#### 🌾 4. Como caracteriza o sistema de produção agrícola?")
        sistema_producao = st.selectbox(
            "Selecione a opção:",
            ["Produção diversificada com variedades resilientes", "Diversificada sem variedades resilientes", "Monocultura", "Produção muito reduzida"],
            key="sistema_producao"
        )
        
        # ===== 5. CAPACIDADE ADAPTATIVA =====
        st.markdown("#### 🧠 5. Qual é o nível de capacidade adaptativa da família agrícola?")
        capacidade_adaptativa = st.selectbox(
            "Selecione a opção:",
            ["Irrigação + assistência técnica + informação climática", "Apenas um ou dois destes recursos", "Nenhum recurso de adaptação"],
            key="capacidade_adaptativa"
        )
        
        # ===== 6. IMPACTO NA SEGURANÇA ALIMENTAR =====
        st.markdown("#### 🍽️ 6. Qual foi o impacto da produção agrícola na segurança alimentar da família nos últimos 12 meses?")
        impacto_producao = st.selectbox(
            "Selecione a opção:",
            ["Produção suficiente sem perdas", "Perdas <25%", "Perdas 25–50%", "Perdas >50% ou produção insuficiente"],
            key="impacto_producao"
        )
        
        st.markdown("---")
        st.caption("📊 Após preencher todas as perguntas, clique em 'Calcular Índices' para obter os resultados.")
        
        if st.form_submit_button("📊 Calcular Índices", use_container_width=True):
            # Recolher respostas
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
            
            st.success("✅ Índices calculados com sucesso!")
            st.rerun()
    
    # ============================================================
    # ===== EXIBIR ÍNDICES =====
    # ============================================================
    if 'indices_agro' in st.session_state and st.session_state.indices_agro:
        st.divider()
        st.markdown("### 📊 Resultados dos Índices")
        
        indices = st.session_state.indices_agro
        
        # Criar um layout de cards para os índices
        col1, col2, col3 = st.columns(3)
        
        # Índices com cores baseadas no valor
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
        
        # Distribuir índices nas colunas
        with col1:
            st.markdown(card_style(indices['Resiliência Climática'], "Resiliência Climática", "Capacidade de recuperação", "🔄"), unsafe_allow_html=True)
            st.markdown(card_style(indices['Segurança Hídrica'], "Segurança Hídrica", "Disponibilidade de água", "💧"), unsafe_allow_html=True)
            st.markdown(card_style(indices['Agricultura Inteligente (CSA)'], "Agricultura Inteligente", "Práticas sustentáveis", "🌱"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(card_style(indices['Diversificação da Produção'], "Diversificação", "Número de culturas", "🌾"), unsafe_allow_html=True)
            st.markdown(card_style(indices['Capacidade Adaptativa'], "Capacidade Adaptativa", "Adaptação às mudanças", "🧠"), unsafe_allow_html=True)
            st.markdown(card_style(indices['Índice Integrado One Health/Nexus'], "One Health/Nexus", "Integração saúde-agricultura", "🔄"), unsafe_allow_html=True)
        
        with col3:
            # Índices onde menor é melhor
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
    
    # ============================================================
    # ===== RECOMENDAÇÕES AUTO-GERADAS =====
    # ============================================================
    if 'indices_agro' in st.session_state and st.session_state.indices_agro:
        st.divider()
        st.markdown("### 💡 Recomendações Personalizadas")
        
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
        
        # ===== REGISTAR INTERVENÇÃO =====
        st.divider()
        st.markdown("#### 📝 Registar Intervenção")
        
        with st.form("form_intervencao"):
            recomendacoes_tecnicas = st.text_area(
                "🌾 Recomendações Técnicas",
                placeholder="Ex: Implementar horta familiar com culturas ricas em ferro...",
                height=80
            )
            
            culturas_recomendadas = st.multiselect(
                "🌱 Culturas Recomendadas",
                ["Feijão", "Amendoim", "Soja", "Espinafre", "Couve", "Alface", 
                 "Batata Doce", "Mandioca", "Milho", "Manga", "Abacate", "Banana",
                 "Cenoura", "Abóbora", "Tomate", "Pimentão", "Cebola", "Alho"]
            )
            
            praticas = st.multiselect(
                "🔄 Práticas Agrícolas Recomendadas",
                ["Rotação de culturas", "Adubação orgânica", "Conservação do solo", 
                 "Irrigação por gotejamento", "Captação de água da chuva", 
                 "Compostagem", "Policultivo", "Agrofloresta", "Plantio direto"]
            )
            
            observacoes_intervencao = st.text_area(
                "📋 Observações",
                height=60
            )
            
            if st.form_submit_button("💾 Registar Intervenção", use_container_width=True):
                if recomendacoes_tecnicas:
                    st.success("✅ Intervenção registada com sucesso!")
                    st.balloons()
                else:
                    st.warning("⚠️ Preencha as recomendações técnicas.")
    
    # ============================================================
    # ===== ENCAMINHAMENTOS RECEBIDOS =====
    # ============================================================
    st.divider()
    st.subheader("📨 Encaminhamentos Recebidos")
    
    enc_agro = [e for e in st.session_state.encaminhamentos if 'Agrônomo' in e.get('especialidade', '')]
    
    if not enc_agro:
        st.info("📋 Nenhum encaminhamento para agrônomo recebido ainda.")
    else:
        pendentes = [e for e in enc_agro if e.get('status') != 'Concluído']
        atendidos = [e for e in enc_agro if e.get('status') == 'Concluído']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📨 Total", len(enc_agro))
        with col2:
            st.metric("⏳ Pendentes", len(pendentes))
        with col3:
            st.metric("✅ Atendidos", len(atendidos))
        
        st.divider()
        
        for enc in enc_agro:
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
                    st.markdown("**📊 Dados Agroalimentares**")
                    if 'dados_clinicos' in enc and enc['dados_clinicos']:
                        dados = enc['dados_clinicos']
                        st.markdown(f"- DDS: {dados.get('dds', 0)}/9")
                        st.markdown(f"- MUAC: {dados.get('muac', 0)} mm")
                        st.markdown(f"- Produção: {dados.get('producao_familiar', 'N/A')}")
                        st.markdown(f"- Terra: {dados.get('acesso_terra', 'N/A')}")
                        st.markdown(f"- Dificuldades: {dados.get('dificuldades_producao', 'N/A')}")
                
                if enc.get('status') == 'Pendente':
                    st.divider()
                    if st.button(f"✅ Marcar como Atendido - {enc.get('paciente', '')}"):
                        for e in st.session_state.encaminhamentos:
                            if e.get('paciente') == enc.get('paciente') and e.get('data') == enc.get('data'):
                                e['status'] = 'Concluído'
                                st.rerun()
    
    # ============================================================
    # ===== ANÁLISE AGROALIMENTAR =====
    # ============================================================
    st.divider()
    st.subheader("📊 Análise Agroalimentar")
    
    if st.session_state.criancas:
        df_pacientes = pd.DataFrame(st.session_state.criancas)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.bar(df_pacientes, x='nome_completo', y='dds_calculado', 
                         title='Diversidade Alimentar (DDS) por Paciente',
                         labels={'dds_calculado': 'DDS', 'nome_completo': 'Paciente'},
                         color='dds_calculado',
                         color_continuous_scale='RdYlGn')
            fig1.add_hline(y=4, line_dash="dash", line_color="red")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.pie(df_pacientes, names='risco_anemia_nivel', 
                         title='Distribuição - Risco de Anemia',
                         color='risco_anemia_nivel',
                         color_discrete_map={'ALTO': '#c62828', 'MÉDIO': '#ef6c00', 'BAIXO': '#2e7d32'})
            st.plotly_chart(fig2, use_container_width=True)
        
        st.subheader("🌾 Produção Agrícola")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'producao_familiar' in df_pacientes.columns:
                producao_counts = df_pacientes['producao_familiar'].value_counts()
                if not producao_counts.empty:
                    fig3 = px.pie(values=producao_counts.values, names=producao_counts.index,
                                 title='Distribuição - Produção Agrícola')
                    st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            if 'acesso_terra' in df_pacientes.columns:
                terra_counts = df_pacientes['acesso_terra'].value_counts()
                if not terra_counts.empty:
                    fig4 = px.pie(values=terra_counts.values, names=terra_counts.index,
                                 title='Distribuição - Acesso à Terra')
                    st.plotly_chart(fig4, use_container_width=True)
        
        st.subheader("🌱 Culturas Produzidas")
        if 'culturas_produzidas' in df_pacientes.columns:
            culturas_counts = df_pacientes['culturas_produzidas'].value_counts().head(10)
            if not culturas_counts.empty:
                fig5 = px.bar(x=culturas_counts.values, y=culturas_counts.index, 
                             orientation='h',
                             title='Principais Culturas Produzidas',
                             labels={'x': 'Nº de Famílias', 'y': 'Cultura'})
                st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("📋 Nenhum dado disponível para análise")

if __name__ == "__main__":
    render_agronomo()