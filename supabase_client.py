from supabase import create_client

# ===== CHAVES DIRETAS (SEM SECRETS) =====
SUPABASE_URL = "https://llfcnigfidoiyhaitala.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxsZmNuaWdmaWRvaXloYWl0YWxhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM2NTY2OTYsImV4cCI6MjA5OTIzMjY5Nn0.-WtmiDwYPS9eQDRsQ-bmXGKzvy4p9x7i9bzYGCgX3VM"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    SUPABASE_AVAILABLE = True
    print("✅ Supabase conectado com sucesso!")
except Exception as e:
    SUPABASE_AVAILABLE = False
    print(f"❌ Erro ao conectar Supabase: {e}")

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