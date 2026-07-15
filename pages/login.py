# pages/login.py
# ===== TELA DE LOGIN =====

import streamlit as st
from auth import fazer_login
from utils.helpers import t
from config import USUARIOS

def renderizar_login():
    """Renderiza a tela de login"""
    
    # ===== TRADUTOR PT/EN NO TOPO =====
    idioma_atual = st.session_state.idioma
    
    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: flex-start;
        gap: 10px;
        padding: 8px 20px;
        background: white;
        border-radius: 30px;
        border: 2px solid #2E7D32;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        width: fit-content;
        margin-bottom: 15px;
    ">
        <a href="?lang=pt" style="
            text-decoration: none;
            background: {'#2E7D32' if idioma_atual == 'pt' else 'transparent'};
            color: {'white' if idioma_atual == 'pt' else '#1B5E20'};
            font-size: 20px;
            font-weight: 700;
            padding: 5px 15px;
            border-radius: 20px;
            transition: all 0.3s ease;
        ">🇵🇹 PT</a>
        <span style="color: #ccc; font-size: 20px;">|</span>
        <a href="?lang=en" style="
            text-decoration: none;
            background: {'#2E7D32' if idioma_atual == 'en' else 'transparent'};
            color: {'white' if idioma_atual == 'en' else '#1B5E20'};
            font-size: 20px;
            font-weight: 700;
            padding: 5px 15px;
            border-radius: 20px;
            transition: all 0.3s ease;
        ">🇬🇧 EN</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar mudança de idioma
    query_params = st.query_params
    if 'lang' in query_params:
        novo_idioma = query_params['lang']
        if novo_idioma in ['pt', 'en'] and novo_idioma != idioma_atual:
            st.session_state.idioma = novo_idioma
            st.rerun()
    
    # ===== CONTEÚDO =====
    st.markdown(f'<h1 class="main-title">{t("titulo")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-title">{t("subtitulo")}</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            
            st.markdown(f"### 🔐 {t('login')}")
            
            username = st.text_input(f"👤 {t('usuario')}", placeholder=f"Digite seu {t('usuario').lower()}", key="login_user")
            password = st.text_input(f"🔑 {t('senha')}", type="password", placeholder=f"Digite sua {t('senha').lower()}", key="login_pass")
            
            if st.button(f"🚀 {t('entrar')}", use_container_width=True, type="primary"):
                if username and password:
                    if fazer_login(username, password):
                        st.success(f"✅ {t('login_sucesso')}")
                        st.rerun()
                    else:
                        st.error(f"❌ {t('login_erro')}")
                else:
                    st.warning(f"⚠️ {t('preencha_campos')}")
            
            st.markdown("---")
            
            st.markdown(f"### 📋 {t('credenciais')}")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown(f"**{t('perfil')}**")
                for perfil in USUARIOS.keys():
                    st.write(f"{USUARIOS[perfil]['icone']} {USUARIOS[perfil]['nome']}")
            
            with col_b:
                st.markdown(f"**{t('usuario_senha')}**")
                for perfil in USUARIOS.keys():
                    st.code(f"{perfil} / 123")
            
            st.markdown('</div>', unsafe_allow_html=True)