# utils/helpers.py
# ===== FUNÇÕES AUXILIARES =====

import streamlit as st
from datetime import datetime
from traducoes import TRADUCOES

def t(texto):
    """Função para traduzir textos"""
    idioma = st.session_state.get('idioma', 'pt')
    return TRADUCOES[idioma].get(texto, texto)

def criar_sidebar():
    """Cria a sidebar com navegação e botão de logout"""
    from auth import fazer_logout
    
    with st.sidebar:
        st.markdown(f"### {t('titulo')}")
        st.markdown(f"**👤 {st.session_state.usuario}**")
        st.markdown(f"📋 {st.session_state.perfil.capitalize()}")
        st.markdown("---")
        
        st.markdown("### Menu")
        
        # ===== MENU POR PERFIL =====
        if st.session_state.perfil == "enfermeiro":
            menu = ["Início", "Dashboard", "Triagem"]
        elif st.session_state.perfil == "medico":
            menu = ["Início", "Dashboard", "Consultas"]
        elif st.session_state.perfil == "nutricionista":
            menu = ["Início", "Dashboard", "Avaliações"]
        elif st.session_state.perfil == "agronomo":
            menu = ["Início", "Dashboard", "Produção"]
        elif st.session_state.perfil == "admin":
            menu = ["Início", "Dashboard", "Configurações"]
        else:
            menu = ["Início", "Dashboard"]
        
        pagina = st.radio("Navegação", menu, index=0)
        
        st.markdown("---")
        st.markdown(f"### {t('informacoes')}")
        st.caption(f"{t('versao')}: 1.0.0")
        st.caption(f"{t('data')}: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        st.markdown("---")
        
        # ===== BOTÃO DE LOGOUT =====
        if st.button("🚪 Sair", use_container_width=True):
            fazer_logout()
        
        return pagina