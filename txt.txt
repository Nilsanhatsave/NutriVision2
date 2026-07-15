# supabase_client.py
# ===== CLIENTE SUPABASE =====

import streamlit as st
from datetime import datetime

try:
    from supabase import create_client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️ Supabase nao instalado. Execute: pip install supabase")

def get_supabase_client():
    """Inicializa o cliente Supabase"""
    if not SUPABASE_AVAILABLE:
        return None
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except:
        return None

def salvar_crianca_supabase(dados):
    """Salva os dados da crianca no Supabase"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
            return False, "Supabase nao configurado"
        
        dados_para_salvar = {}
        for k, v in dados.items():
            if v is not None and v != "" and v != "None" and v != "N/A":
                dados_para_salvar[k] = v
        
        resultado = supabase.table('criancas').insert(dados_para_salvar).execute()
        return True, resultado
    except Exception as e:
        return False, str(e)

def carregar_criancas_supabase():
    """Carrega todas as criancas do Supabase"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
            return False, []
        
        resultado = supabase.table('criancas').select('*').order('created_at', desc=True).execute()
        return True, resultado.data
    except Exception as e:
        return False, str(e)

def atualizar_crianca_supabase(id_crianca, dados):
    """Atualiza os dados da crianca no Supabase"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
            return False, "Supabase nao configurado"
        
        dados_para_salvar = {}
        for k, v in dados.items():
            if v is not None and v != "" and v != "None" and v != "N/A":
                dados_para_salvar[k] = v
        
        resultado = supabase.table('criancas').update(dados_para_salvar).eq('id', id_crianca).execute()
        return True, resultado
    except Exception as e:
        return False, str(e)

def salvar_decisao_clinica_supabase(decisao):
    """Salva a decisao clinica no Supabase"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
            return False, "Supabase nao configurado"
        
        dados = {
            'paciente': decisao.get('paciente', ''),
            'data': decisao.get('data', datetime.now().strftime('%Y-%m-%d %H:%M')),
            'diagnostico': decisao.get('diagnostico', ''),
            'prescricao': decisao.get('prescricao', ''),
            'seguimento': decisao.get('seguimento', ''),
            'observacoes': decisao.get('observacoes', ''),
            'hemoglobina': decisao.get('hemoglobina', None),
            'tipo_anemia': decisao.get('tipo_anemia', None),
            'created_at': datetime.now().isoformat()
        }
        
        resultado = supabase.table('decisoes_clinicas').insert(dados).execute()
        return True, resultado
    except Exception as e:
        return False, str(e)

def carregar_decisoes_clinicas_supabase():
    """Carrega as decisoes clinicas do Supabase"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
            return False, []
        
        resultado = supabase.table('decisoes_clinicas').select('*').order('created_at', desc=True).execute()
        return True, resultado.data
    except Exception as e:
        return False, str(e)

def criar_tabelas_supabase():
    """Cria as tabelas necessarias no Supabase"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
            return False, "Supabase nao configurado"
        
        # Verificar se a tabela criancas existe
        try:
            supabase.table('criancas').select('*').limit(1).execute()
        except:
            pass
        
        # Verificar se a tabela decisoes_clinicas existe
        try:
            supabase.table('decisoes_clinicas').select('*').limit(1).execute()
        except:
            pass
        
        return True, "Tabelas verificadas"
    except Exception as e:
        return False, str(e)