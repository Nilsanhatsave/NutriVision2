# utils/helpers.py
# ===== FUNÇÕES AUXILIARES =====

import streamlit as st
from datetime import datetime
from traducoes import TRADUCOES

def t(texto):
    """Função para traduzir textos"""
    idioma = st.session_state.get('idioma', 'pt')
    return TRADUCOES[idioma].get(texto, texto)

# def criar_sidebar():
#     """Cria a sidebar com navegação"""
#     from auth import fazer_logout
#     
#     with st.sidebar:
#         # ... todo o código da sidebar
#         pass
#     return None