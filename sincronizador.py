# sincronizador.py
import streamlit as st
import time
from database_local import (
    get_nao_sincronizados,
    marcar_como_sincronizado,
    contar_nao_sincronizados
)

def verificar_internet():
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def sincronizar_com_supabase(supabase_client, progress_bar=None, status_text=None):
    try:
        nao_sincronizados = get_nao_sincronizados()
        
        if not nao_sincronizados:
            return {
                'success': True,
                'message': '✅ Todos os dados já estão sincronizados!',
                'total': 0,
                'sincronizados': 0,
                'erros': 0
            }
        
        total = len(nao_sincronizados)
        sincronizados = 0
        erros = 0
        erros_lista = []
        
        for i, dados in enumerate(nao_sincronizados):
            try:
                if progress_bar:
                    progress_bar.progress((i + 1) / total)
                if status_text:
                    status_text.text(f"Sincronizando {i+1}/{total}: {dados.get('nome_completo', 'N/A')}")
                
                resultado = supabase_client.table('criancas').insert(dados).execute()
                
                if resultado.data:
                    marcar_como_sincronizado(dados.get('id_local'))
                    sincronizados += 1
                else:
                    erros += 1
                    erros_lista.append(f"{dados.get('nome_completo', 'N/A')}: Erro ao inserir")
                    
            except Exception as e:
                erros += 1
                erros_lista.append(f"{dados.get('nome_completo', 'N/A')}: {str(e)}")
        
        return {
            'success': True,
            'message': f'✅ Sincronização concluída! {sincronizados} registos sincronizados, {erros} erros.',
            'total': total,
            'sincronizados': sincronizados,
            'erros': erros,
            'erros_lista': erros_lista
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'❌ Erro na sincronização: {str(e)}',
            'total': 0,
            'sincronizados': 0,
            'erros': 0
        }

def mostrar_status_sincronizacao():
    nao_sincronizados = contar_nao_sincronizados()
    ultima = None  # Temporário - função será adicionada depois
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if nao_sincronizados > 0:
            st.warning(f"📤 {nao_sincronizados} registos para sincronizar")
        else:
            st.success("✅ Todos os dados sincronizados")
    
    with col2:
        if ultima:
            st.info(f"🕐 Última: {ultima['data'][:16]}")
        else:
            st.info("🕐 Nenhuma sincronização ainda")
    
    with col3:
        if verificar_internet():
            st.success("🌐 Online")
        else:
            st.error("📡 Offline")
    
    return nao_sincronizados