# teste_supabase.py
import streamlit as st

st.title("🔍 Teste de Conexão Supabase")

try:
    from supabase_client import SUPABASE_AVAILABLE, carregar_criancas_supabase
    
    st.write(f"**Supabase disponível:** {SUPABASE_AVAILABLE}")
    
    if SUPABASE_AVAILABLE:
        st.success("✅ Supabase instalado e disponível!")
        
        # Tentar carregar dados
        sucesso, dados = carregar_criancas_supabase()
        if sucesso:
            st.success(f"✅ {len(dados)} registos carregados!")
            if dados:
                st.dataframe(dados)
            else:
                st.info("📋 Nenhum registo encontrado")
        else:
            st.error(f"❌ Erro ao carregar dados: {dados}")
    else:
        st.error("❌ Supabase não disponível. Execute: pip install supabase")
        
except Exception as e:
    st.error(f"❌ Erro: {e}")
    st.info("""
    **Soluções:**
    1. Verifique se o ficheiro `.streamlit/secrets.toml` existe
    2. Instale o supabase: `pip install supabase`
    3. Verifique as credenciais no secrets.toml
    """)