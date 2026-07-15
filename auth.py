# auth.py
# ===== AUTENTICAÇÃO E SESSÃO =====

import streamlit as st
from config import USUARIOS

def inicializar_sessao():
    """Inicializa as variáveis de sessão"""
    if 'logado' not in st.session_state:
        st.session_state.logado = False
    if 'usuario' not in st.session_state:
        st.session_state.usuario = None
    if 'perfil' not in st.session_state:
        st.session_state.perfil = None
    if 'icone' not in st.session_state:
        st.session_state.icone = None
    if 'idioma' not in st.session_state:
        st.session_state.idioma = 'pt'

def fazer_login(user, senha):
    """Realiza o login do usuário"""
    if user in USUARIOS and USUARIOS[user]["senha"] == senha:
        st.session_state.logado = True
        st.session_state.usuario = USUARIOS[user]["nome"]
        st.session_state.perfil = user
        st.session_state.icone = USUARIOS[user]["icone"]
        return True
    return False

def fazer_logout():
    """Realiza o logout do usuário"""
    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.perfil = None
    st.session_state.icone = None
    st.rerun()

def verificar_autenticacao():
    """Verifica se o usuário está autenticado"""
    return st.session_state.logado