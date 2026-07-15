# database_local.py
import sqlite3
import json
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'nutrivision.db')
def get_ultima_sincronizacao():
    """Retorna a data da última sincronização"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT data_sincronizacao, registos_sincronizados, status 
        FROM sincronizacao 
        ORDER BY id DESC 
        LIMIT 1
        ''')
        row = cursor.fetchone()
        conn.close()
        if row:
            return {'data': row[0], 'registos': row[1], 'status': row[2]}
        return None
    except Exception as e:
        return None

def init_db():
    """Inicializa o banco de dados local"""
    # Criar pasta data se não existir
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabela de crianças
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS criancas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT,
        idade_meses INTEGER,
        data_nascimento TEXT,
        provincia TEXT,
        distrito TEXT,
        residencia TEXT,
        hospital TEXT,
        peso REAL,
        altura REAL,
        muac INTEGER,
        risco_anemia_nivel TEXT,
        risco_fome_nivel TEXT,
        risco_inseguranca_nivel TEXT,
        dados_completos TEXT,
        sincronizado INTEGER DEFAULT 0,
        data_registo TEXT,
        data_sincronizacao TEXT
    )
    ''')
    
    # Tabela de logs de sincronização
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sincronizacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_sincronizacao TEXT,
        registos_sincronizados INTEGER,
        status TEXT,
        detalhes TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def salvar_crianca_local(dados):
    """Salva os dados no SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO criancas (
            nome_completo, idade_meses, data_nascimento, provincia, distrito,
            residencia, hospital, peso, altura, muac,
            risco_anemia_nivel, risco_fome_nivel, risco_inseguranca_nivel,
            dados_completos, sincronizado, data_registo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dados.get('nome_completo', ''),
            dados.get('idade_meses', 0),
            dados.get('data_nascimento', ''),
            dados.get('provincia', ''),
            dados.get('distrito', ''),
            dados.get('residencia', ''),
            dados.get('hospital', ''),
            dados.get('peso', 0),
            dados.get('altura', 0),
            dados.get('muac', 0),
            dados.get('risco_anemia_nivel', ''),
            dados.get('risco_fome_nivel', ''),
            dados.get('risco_inseguranca_nivel', ''),
            json.dumps(dados),
            0,  # não sincronizado
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        conn.close()
        return True, "Salvo localmente"
    except Exception as e:
        return False, str(e)

def carregar_criancas_local():
    """Carrega todos os dados do SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM criancas ORDER BY id DESC')
        rows = cursor.fetchall()
        
        criancas = []
        for row in rows:
            try:
                dados = json.loads(row[13])  # dados_completos
                dados['id_local'] = row[0]
                dados['sincronizado'] = row[14]
                criancas.append(dados)
            except:
                continue
        
        conn.close()
        return True, criancas
    except Exception as e:
        return False, []

def get_nao_sincronizados():
    """Busca registos que não foram sincronizados"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM criancas WHERE sincronizado = 0 ORDER BY id
        ''')
        rows = cursor.fetchall()
        
        nao_sincronizados = []
        for row in rows:
            try:
                dados = json.loads(row[13])
                dados['id_local'] = row[0]
                nao_sincronizados.append(dados)
            except:
                continue
        
        conn.close()
        return nao_sincronizados
    except Exception as e:
        return []

def marcar_como_sincronizado(id_local):
    """Marca um registo como sincronizado"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE criancas 
        SET sincronizado = 1, data_sincronizacao = ? 
        WHERE id = ?
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id_local))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def registrar_log_sincronizacao(registos, status, detalhes=""):
    """Registra um log de sincronização"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO sincronizacao (data_sincronizacao, registos_sincronizados, status, detalhes)
        VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            registos,
            status,
            detalhes
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def get_ultima_sincronizacao():
    """Retorna a data da última sincronização"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT data_sincronizacao, registos_sincronizados, status 
        FROM sincronizacao 
        ORDER BY id DESC 
        LIMIT 1
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'data': row[0],
                'registos': row[1],
                'status': row[2]
            }
        return None
    except Exception as e:
        return None

def contar_nao_sincronizados():
    """Conta quantos registos não foram sincronizados"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM criancas WHERE sincronizado = 0')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    except Exception as e:
        return 0

def limpar_dados_sincronizados():
    """Remove dados antigos já sincronizados (opcional)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Remover registos sincronizados há mais de 30 dias
        cursor.execute('''
        DELETE FROM criancas 
        WHERE sincronizado = 1 
        AND data_sincronizacao < datetime('now', '-30 days')
        ''')
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False