# pages/admin.py
# ===== PERFIL ADMINISTRADOR =====

import streamlit as st
from config import USUARIOS
from utils.helpers import t

def renderizar_admin():
    st.title(t('configuracoes'))
    st.markdown("Configurações do Sistema")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👥 Usuários")
        for user, info in USUARIOS.items():
            st.write(f"- {info['icone']} {info['nome']} (usuário: `{user}`)")
    
    with col2:
        st.subheader("📊 Estatísticas")
        st.metric("Total de usuários", len(USUARIOS))
        st.metric("Triagens realizadas", len(st.session_state.get('criancas', [])))
        st.metric("Pacientes cadastrados", len(st.session_state.get('criancas', [])))