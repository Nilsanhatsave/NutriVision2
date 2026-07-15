# teste.py
import streamlit as st

st.title("🔍 Teste Supabase")

try:
    from supabase_client import SUPABASE_AVAILABLE, get_supabase_client, carregar_criancas_supabase
    
    st.write(f"**SUPABASE_AVAILABLE:** {SUPABASE_AVAILABLE}")
    
    if SUPABASE_AVAILABLE:
        st.success("✅ Supabase instalado")
        
        # Testar cliente
        client = get_supabase_client()
        if client:
            st.success("✅ Cliente criado")
        else:
            st.error("❌ Cliente NÃO criado")
        
        # Testar carregar dados
        sucesso, dados = carregar_criancas_supabase()
        if sucesso:
            st.success(f"✅ {len(dados)} registos carregados")
            if dados:
                st.dataframe(dados)
        else:
            st.error(f"❌ Erro: {dados}")
    else:
        st.error("❌ Supabase não instalado. Execute: pip install supabase")
        
except Exception as e:
    st.error(f"❌ Erro: {e}")