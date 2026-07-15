# supabase_config.py
# ===== CONFIGURAÇÃO DO SUPABASE =====

from supabase import create_client
import streamlit as st
from datetime import datetime

# ===== CHAVES DIRETAS =====
SUPABASE_URL = "https://llfcnigfidoiyhaitala.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxsZmNuaWdmaWRvaXloYWl0YWxhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM2NTY2OTYsImV4cCI6MjA5OTIzMjY5Nn0.-WtmiDwYPS9eQDRsQ-bmXGKzvy4p9x7i9bzYGCgX3VM"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    SUPABASE_AVAILABLE = True
    print("✅ Supabase conectado com sucesso!")
except Exception as e:
    SUPABASE_AVAILABLE = False
    print(f"❌ Erro ao conectar Supabase: {e}")

def get_supabase_client():
    return supabase if SUPABASE_AVAILABLE else None

def verificar_conexao():
    """Verifica se a conexão com o Supabase está ativa"""
    if SUPABASE_AVAILABLE:
        return True, "Conexão ativa"
    return False, "Sem conexão"

def salvar_crianca_supabase(dados):
    if not SUPABASE_AVAILABLE:
        return False, "Supabase nao disponivel"
    try:
        response = supabase.table("criancas").insert(dados).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

def carregar_criancas_supabase():
    if not SUPABASE_AVAILABLE:
        return False, []
    try:
        response = supabase.table("criancas").select("*").execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

def atualizar_crianca_supabase(id, dados):
    if not SUPABASE_AVAILABLE:
        return False, "Supabase nao disponivel"
    try:
        response = supabase.table("criancas").update(dados).eq("id", id).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

# ===== FUNÇÕES PARA DECISÕES CLÍNICAS =====

def criar_tabela_decisoes_clinicas():
    """Cria a tabela de decisões clínicas no Supabase se não existir"""
    try:
        if not SUPABASE_AVAILABLE:
            return False, "Supabase não disponível"
        
        try:
            resultado = supabase.table('decisoes_clinicas').select('*').limit(1).execute()
            return True, "Tabela já existe"
        except Exception as e:
            if "relation" in str(e) and "does not exist" in str(e):
                sql = """
                CREATE TABLE IF NOT EXISTS decisoes_clinicas (
                    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                    paciente TEXT NOT NULL,
                    data TIMESTAMP,
                    diagnostico TEXT,
                    prescricao TEXT,
                    seguimento TEXT,
                    observacoes TEXT,
                    hemoglobina FLOAT,
                    tipo_anemia TEXT,
                    densidade_parasitaria TEXT,
                    diarreia TEXT,
                    doenca_cronica TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                );
                """
                try:
                    resultado = supabase.rpc('exec_sql', {'sql': sql}).execute()
                    return True, "Tabela criada com sucesso!"
                except:
                    return False, "Não foi possível criar a tabela. Execute o SQL manualmente no Supabase."
            else:
                return False, f"Erro ao verificar tabela: {str(e)}"
    except Exception as e:
        return False, f"Erro ao criar tabela: {str(e)}"

def salvar_decisao_clinica_supabase(decisao):
    """Salva a decisão clínica no Supabase"""
    try:
        if not SUPABASE_AVAILABLE:
            return False, "Supabase não disponível"
        
        dados = {
            'paciente': decisao['paciente'],
            'data': decisao['data'],
            'diagnostico': decisao.get('diagnostico', ''),
            'prescricao': decisao.get('prescricao', ''),
            'seguimento': decisao.get('seguimento', ''),
            'observacoes': decisao.get('observacoes', ''),
            'hemoglobina': decisao.get('hemoglobina', None),
            'tipo_anemia': decisao.get('tipo_anemia', None),
            'densidade_parasitaria': decisao.get('densidade_parasitaria', None),
            'diarreia': decisao.get('diarreia', None),
            'doenca_cronica': decisao.get('doenca_cronica', None),
            'created_at': datetime.now().isoformat()
        }
        
        resultado = supabase.table('decisoes_clinicas').insert(dados).execute()
        return True, resultado.data
    except Exception as e:
        return False, str(e)

def carregar_decisoes_clinicas_supabase():
    """Carrega as decisões clínicas do Supabase"""
    try:
        if not SUPABASE_AVAILABLE:
            return False, []
        
        try:
            resultado = supabase.table('decisoes_clinicas')\
                .select('*')\
                .order('created_at', desc=True)\
                .execute()
            return True, resultado.data
        except Exception as e:
            if "relation" in str(e) and "does not exist" in str(e):
                return False, "Tabela ainda não foi criada"
            return False, str(e)
    except Exception as e:
        return False, str(e)