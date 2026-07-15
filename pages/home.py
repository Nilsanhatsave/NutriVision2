# pages/home.py
# ===== PÁGINA INICIAL =====

import streamlit as st
from utils.helpers import t

def renderizar_home():
    """Renderiza a página inicial"""
    
    st.markdown(f"""
    <h1 style='text-align:center;font-size:3rem;color:#1B5E20;'>
        🌿 NutriVision
    </h1>
    <h3 style='text-align:center;'>
        👋 {t('bem_vindo')}, {st.session_state.icone} {st.session_state.usuario}!
    </h3>
    <p style='text-align:center;font-size:1.2rem;color:#555;'>
        📋 {t('perfil_label')}: {st.session_state.perfil.capitalize()}
    </p>
    <hr>
    """, unsafe_allow_html=True)
    
    st.success(f"✅ {t('conectado_sucesso')}")
    st.info(f"📋 {t('use_menu')}")