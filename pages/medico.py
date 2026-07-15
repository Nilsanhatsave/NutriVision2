import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import uuid
import base64
import time
import qrcode
from io import BytesIO
import os
import tempfile

# ========== IMPORT SUPABASE ==========
try:
    from supabase import create_client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️ Supabase não instalado. Execute: pip install supabase")

# ========== FUNÇÕES SUPABASE ==========
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

def criar_tabela_decisoes_clinicas():
    """Cria a tabela de decisões clínicas no Supabase se não existir"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
            return False, "Supabase não configurado"
        
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

def carregar_pacientes_supabase():
    """Carrega todas as crianças do Supabase para o médico"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
            return False, []
        
        resultado = supabase.table('criancas').select('*').order('created_at', desc=True).execute()
        return True, resultado.data
    except Exception as e:
        return False, str(e)

def atualizar_dados_clinicos_supabase(paciente_id, dados):
    """Atualiza os dados clínicos no Supabase"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
            return False, "Supabase não configurado"
        
        resultado = supabase.table('criancas').update(dados).eq('id', paciente_id).execute()
        return True, resultado
    except Exception as e:
        return False, str(e)

def salvar_decisao_clinica_supabase(decisao):
    """Salva a decisão clínica no Supabase com tratamento de erros"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
            return False, "Supabase não configurado"
        
        try:
            test = supabase.table('decisoes_clinicas').select('*').limit(1).execute()
        except Exception as e:
            if "relation" in str(e) and "does not exist" in str(e):
                sucesso, msg = criar_tabela_decisoes_clinicas()
                if not sucesso:
                    return False, f"Tabela não existe e não foi possível criar: {msg}"
            else:
                return False, f"Erro ao verificar tabela: {str(e)}"
        
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
        return True, resultado
    except Exception as e:
        return False, str(e)

def carregar_decisoes_clinicas_supabase():
    """Carrega as decisões clínicas do Supabase"""
    try:
        supabase = get_supabase_client()
        if supabase is None:
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

def recarregar_pacientes():
    """Recarrega os pacientes do Supabase"""
    if SUPABASE_AVAILABLE:
        sucesso, dados = carregar_pacientes_supabase()
        if sucesso and dados:
            pacientes = []
            for item in dados:
                paciente = {
                    'id': item.get('id'),
                    'nome': item.get('nome_completo', 'N/A'),
                    'idade_meses': item.get('idade_meses', 0),
                    'peso_kg': item.get('peso', 0),
                    'altura_cm': item.get('altura', 0),
                    'muac_mm': item.get('muac', 0),
                    'hemoglobina': item.get('hemoglobina', None),
                    'tipo_anemia': item.get('tipo_anemia', None),
                    'densidade_parasitaria': item.get('densidade_parasitaria', None),
                    'diarreia': item.get('diarreia', None),
                    'doenca_cronica': item.get('doenca_cronica', None),
                    'doenca_cronica_especificar': item.get('doenca_cronica_especificar', None),
                    'anemia_risco': item.get('risco_anemia_nivel', 'N/A'),
                    'anemia_prob': item.get('risco_anemia_score', 0),
                    'diversidade_alimentar': item.get('dds_calculado', 0),
                    'data_registo': item.get('data_registo', 'N/A'),
                    'provincia': item.get('provincia', 'N/A'),
                    'distrito': item.get('distrito', 'N/A'),
                    'residencia': item.get('residencia', 'N/A'),
                    'hospital': item.get('hospital', 'N/A'),
                    'sexo': item.get('sexo', 'N/A')
                }
                pacientes.append(paciente)
            st.session_state.patients = pacientes
            return True
    return False

# ========== FUNÇÃO PARA CONVERTER DADOS CLÍNICOS ==========
def obter_dados_clinicos(row):
    """Extrai os dados clínicos de forma segura"""
    if 'dados_clinicos' in row and row['dados_clinicos']:
        if isinstance(row['dados_clinicos'], dict):
            return row['dados_clinicos']
        elif isinstance(row['dados_clinicos'], str):
            try:
                return json.loads(row['dados_clinicos'])
            except:
                return {}
    return {}

# ========== FUNÇÃO GERAR RELATÓRIO PDF COM QR CODE ==========
def gerar_relatorio_pdf_com_qr(patient_data, record, medico_nome, assinatura):
    """Gera um relatório em PDF com QR Code para validação"""
    try:
        from fpdf import FPDF
        from datetime import datetime
        import qrcode
        from io import BytesIO
        import json
        import os
        import tempfile
        
        # ===== DADOS PARA O QR CODE =====
        codigo_prescricao = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4())[:8]
        
        # ===== GARANTIR QUE OS VALORES EXISTAM =====
        paciente = patient_data.get('nome', 'N/A') or 'N/A'
        prescricao_texto = record.get('prescricao', 'N/A') or 'N/A'
        diagnostico_texto = record.get('diagnostico', 'N/A') or 'N/A'
        seguimento_texto = record.get('seguimento', '30 dias') or '30 dias'
        data_emissao = datetime.now().strftime('%Y-%m-%d %H:%M')
        validade = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        dados_qr = {
            'codigo': codigo_prescricao,
            'paciente': paciente,
            'data': data_emissao,
            'medico': medico_nome,
            'prescricao': prescricao_texto,
            'diagnostico': diagnostico_texto,
            'seguimento': seguimento_texto,
            'validade': validade
        }
        
        # ===== GERAR QR CODE =====
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=5,
            border=2,
        )
        qr.add_data(json.dumps(dados_qr))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr_data = buffered.getvalue()
        
        # ===== SALVAR QR CODE EM DIRETÓRIO TEMPORÁRIO =====
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            tmp_file.write(qr_data)
            qr_path = tmp_file.name
        
        # ===== CRIAR PDF =====
        pdf = FPDF()
        pdf.add_page()
        
        # ===== CABEÇALHO COM LOGO =====
        pdf.set_font("Arial", "B", 24)
        pdf.set_text_color(46, 125, 50)
        pdf.cell(0, 15, "NutriVision", ln=True, align='C')
        
        # ===== SELO DIGITAL =====
        pdf.set_y(10)
        pdf.set_x(170)
        pdf.set_font("Arial", "B", 10)
        pdf.set_text_color(0, 100, 0)
        pdf.cell(30, 10, "[SELO]", ln=False, align='C')
        pdf.set_y(17)
        pdf.set_x(165)
        pdf.set_font("Arial", "I", 6)
        pdf.cell(40, 5, "DIGITAL", ln=False, align='C')
        pdf.set_y(22)
        pdf.set_x(162)
        pdf.set_font("Arial", "I", 5)
        pdf.cell(46, 5, f"{datetime.now().strftime('%d/%m/%Y')}", ln=False, align='C')
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "RELATORIO CLINICO", ln=True, align='C')
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 8, f"Data de emissao: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
        pdf.line(10, 55, 200, 55)
        pdf.ln(5)
        
        # ===== DADOS DO PACIENTE =====
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(230, 240, 230)
        pdf.cell(0, 10, "DADOS DO PACIENTE", ln=True, fill=True)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Arial", "", 11)
        
        pdf.cell(60, 7, "Nome:", ln=0)
        pdf.cell(0, 7, f"{paciente}", ln=True)
        
        idade = patient_data.get('idade_meses', 0) or 0
        pdf.cell(60, 7, "Idade:", ln=0)
        pdf.cell(0, 7, f"{idade} meses", ln=True)
        
        sexo = patient_data.get('sexo', 'N/A') or 'N/A'
        pdf.cell(60, 7, "Sexo:", ln=0)
        pdf.cell(0, 7, f"{sexo}", ln=True)
        
        provincia = patient_data.get('provincia', 'N/A') or 'N/A'
        pdf.cell(60, 7, "Provincia:", ln=0)
        pdf.cell(0, 7, f"{provincia}", ln=True)
        
        hospital = patient_data.get('hospital', 'N/A') or 'N/A'
        pdf.cell(60, 7, "Hospital:", ln=0)
        pdf.cell(0, 7, f"{hospital}", ln=True)
        
        data_registo = patient_data.get('data_registo', 'N/A') or 'N/A'
        pdf.cell(60, 7, "Data de Registo:", ln=0)
        pdf.cell(0, 7, f"{data_registo}", ln=True)
        pdf.ln(3)
        
        # ===== DADOS CLÍNICOS =====
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(230, 240, 230)
        pdf.cell(0, 10, "DADOS CLINICOS", ln=True, fill=True)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Arial", "", 11)
        
        peso = patient_data.get('peso_kg', 0) or 0
        pdf.cell(60, 7, "Peso:", ln=0)
        pdf.cell(0, 7, f"{peso} kg", ln=True)
        
        altura = patient_data.get('altura_cm', 0) or 0
        pdf.cell(60, 7, "Altura:", ln=0)
        pdf.cell(0, 7, f"{altura} cm", ln=True)
        
        muac = patient_data.get('muac_mm', 0) or 0
        pdf.cell(60, 7, "MUAC:", ln=0)
        pdf.cell(0, 7, f"{muac} mm", ln=True)
        
        hemoglobina = patient_data.get('hemoglobina', 'N/A')
        if hemoglobina is None or hemoglobina == '':
            hemoglobina = 'N/A'
        pdf.cell(60, 7, "Hemoglobina:", ln=0)
        pdf.cell(0, 7, f"{hemoglobina} g/dL", ln=True)
        
        tipo_anemia = patient_data.get('tipo_anemia', 'N/A') or 'N/A'
        pdf.cell(60, 7, "Tipo de Anemia:", ln=0)
        pdf.cell(0, 7, f"{tipo_anemia}", ln=True)
        
        risco = patient_data.get('anemia_risco', 'N/A') or 'N/A'
        prob = patient_data.get('anemia_prob', 0)
        if prob is None:
            prob = 0
        pdf.cell(60, 7, "Risco de Anemia:", ln=0)
        pdf.cell(0, 7, f"{risco} ({prob:.1f}%)", ln=True)
        
        dds = patient_data.get('diversidade_alimentar', 0) or 0
        pdf.cell(60, 7, "DDS (Diversidade Alimentar):", ln=0)
        pdf.cell(0, 7, f"{dds}/9", ln=True)
        pdf.ln(3)
        
        # ===== DECISÃO CLÍNICA =====
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(230, 240, 230)
        pdf.cell(0, 10, "DECISAO CLINICA", ln=True, fill=True)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Arial", "", 11)
        
        pdf.cell(60, 7, "Data da Decisao:", ln=0)
        pdf.cell(0, 7, f"{data_emissao}", ln=True)
        
        pdf.cell(60, 7, "Diagnostico:", ln=0)
        pdf.cell(0, 7, "", ln=True)
        pdf.set_x(60)
        pdf.multi_cell(0, 7, f"{diagnostico_texto}")
        pdf.ln(2)
        
        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(0, 100, 0)
        pdf.cell(60, 7, "PRESCRICAO MEDICA:", ln=0)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 7, "", ln=True)
        pdf.set_x(60)
        pdf.multi_cell(0, 7, f"{prescricao_texto}")
        pdf.ln(2)
        
        pdf.set_text_color(0, 0, 0)
        pdf.cell(60, 7, "Plano de Seguimento:", ln=0)
        pdf.cell(0, 7, f"{seguimento_texto}", ln=True)
        
        pdf.ln(5)
        
        # ===== QR CODE =====
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(230, 240, 230)
        pdf.cell(0, 10, "VALIDACAO DO RELATORIO", ln=True, fill=True)
        pdf.set_fill_color(255, 255, 255)
        
        # Inserir QR Code
        try:
            if os.path.exists(qr_path):
                pdf.image(qr_path, x=10, y=pdf.get_y() + 5, w=50, h=50)
            else:
                pdf.cell(0, 7, "QR Code nao disponivel", ln=True)
        except Exception as e:
            pdf.cell(0, 7, f"QR Code: {str(e)[:30]}", ln=True)
        
        # Texto explicativo do QR Code (SEM EMOJIS)
        pdf.set_y(pdf.get_y() + 5)
        pdf.set_x(70)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, "ESCANEIE O QR CODE", ln=True)  # <-- SEM EMOJI
        pdf.set_x(70)
        pdf.set_font("Arial", "", 9)
        pdf.cell(0, 5, "Para validar a autenticidade do relatorio", ln=True)
        pdf.set_x(70)
        pdf.cell(0, 5, f"Codigo: {codigo_prescricao}", ln=True)
        pdf.set_x(70)
        pdf.cell(0, 5, f"Validade: {validade}", ln=True)
        
        pdf.ln(15)
        
        # ===== ASSINATURA COM SELO =====
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(230, 240, 230)
        pdf.cell(0, 10, "ASSINATURA DO MEDICO", ln=True, fill=True)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Arial", "", 11)
        
        pdf.ln(10)
        
        pdf.cell(80, 10, "_________________________", ln=0)
        pdf.cell(30, 10, "", ln=0)
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 100, 0)
        pdf.cell(20, 10, "[SELO]", ln=0, align='C')
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        pdf.cell(30, 10, "", ln=0)
        pdf.cell(80, 10, "_________________________", ln=True)
        
        medico_nome = medico_nome or '_________________________'
        pdf.cell(80, 7, medico_nome, ln=0)
        pdf.cell(30, 7, "", ln=0)
        pdf.set_font("Arial", "I", 8)
        pdf.set_text_color(0, 100, 0)
        pdf.cell(20, 7, "DIGITAL", ln=0, align='C')
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        pdf.cell(30, 7, "", ln=0)
        pdf.cell(80, 7, "Assinatura Eletronica", ln=True)
        
        pdf.cell(0, 7, f"Assinado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
        
        # ===== RODAPÉ =====
        pdf.set_y(270)
        pdf.set_font("Arial", "I", 7)
        pdf.set_text_color(0, 100, 0)
        pdf.cell(30, 7, "[SELO]", ln=0, align='L')
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "I", 6)
        pdf.cell(0, 7, "Documento validado digitalmente", ln=True, align='C')
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 7, "NutriVision - Plataforma de Detecao Precoce", ln=True, align='C')
        pdf.cell(0, 7, f"Relatorio Clinico - {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
        
        pdf_output = pdf.output(dest='S').encode('latin1')
        
        # Limpar arquivo temporário
        try:
            if os.path.exists(qr_path):
                os.remove(qr_path)
        except:
            pass
        
        return pdf_output
    
    except ImportError as e:
        st.error(f"❌ Biblioteca nao instalada: {e}. Execute: pip install qrcode[pil] fpdf")
        return None
    except Exception as e:
        st.error(f"❌ Erro ao gerar PDF: {e}")
        return None

# ========== FUNÇÃO PRINCIPAL ==========
def render_medico():
    st.title("👨🏾⚕️ Médico - Avaliação Clínica")
    
    # ===== INICIALIZAR SESSION STATE =====
    if 'medical_records' not in st.session_state:
        st.session_state.medical_records = []
    
    if 'encaminhamentos' not in st.session_state:
        st.session_state.encaminhamentos = []
    
    if 'modo_edicao' not in st.session_state:
        st.session_state.modo_edicao = False
    
    if 'paciente_em_edicao' not in st.session_state:
        st.session_state.paciente_em_edicao = None
    
    if 'paciente_selecionado' not in st.session_state:
        st.session_state.paciente_selecionado = None
    
    if 'erro_supabase' not in st.session_state:
        st.session_state.erro_supabase = None
    
    if 'limpar_campos' not in st.session_state:
        st.session_state.limpar_campos = False
    
    if 'gerar_relatorio_apos_encaminhar' not in st.session_state:
        st.session_state.gerar_relatorio_apos_encaminhar = False
    
    if 'paciente_relatorio' not in st.session_state:
        st.session_state.paciente_relatorio = None
    
    # ===== GERAR RELATÓRIO APÓS ENCAMINHAMENTO =====
    if st.session_state.get('gerar_relatorio_apos_encaminhar', False):
        paciente_nome = st.session_state.get('paciente_relatorio', '')
        
        if paciente_nome:
            patient_data = next((p for p in st.session_state.patients if p['nome'] == paciente_nome), None)
            
            ultima_decisao = None
            for r in reversed(st.session_state.medical_records):
                if r.get('paciente') == paciente_nome:
                    ultima_decisao = r
                    break
            
            if patient_data and ultima_decisao:
                st.success(f"✅ {paciente_nome} encaminhado com sucesso!")
                
                with st.expander("📄 Gerar Relatório Clínico", expanded=True):
                    st.markdown(f"### 📄 Relatório - {paciente_nome}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Dados do Paciente**")
                        st.markdown(f"- Nome: {patient_data.get('nome', 'N/A')}")
                        st.markdown(f"- Idade: {patient_data.get('idade_meses', 0)} meses")
                        st.markdown(f"- Sexo: {patient_data.get('sexo', 'N/A')}")
                        st.markdown(f"- Província: {patient_data.get('provincia', 'N/A')}")
                        st.markdown(f"- Hospital: {patient_data.get('hospital', 'N/A')}")
                    
                    with col2:
                        st.markdown("**Última Decisão Clínica**")
                        st.markdown(f"- Data: {ultima_decisao.get('data', 'N/A')}")
                        st.markdown(f"- Diagnóstico: {ultima_decisao.get('diagnostico', 'N/A')}")
                        st.markdown(f"- Prescrição: {ultima_decisao.get('prescricao', 'N/A')}")
                        st.markdown(f"- Seguimento: {ultima_decisao.get('seguimento', 'N/A')}")
                    
                    st.divider()
                    
                    st.markdown("#### 📄 Gerar PDF do Relatório")
                    
                    medico_nome = st.text_input(
                        "Nome do Médico Responsável:",
                        placeholder="Dr. Nome Completo",
                        key=f"medico_nome_relatorio_final_{paciente_nome}"
                    )
                    
                    st.markdown("**✍️ Assinatura Eletrónica**")
                    assinatura = st.text_input(
                        "Digite a sua assinatura (nome completo):",
                        placeholder="Digite o seu nome para assinar eletronicamente",
                        key=f"assinatura_final_{paciente_nome}"
                    )
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button("📄 Gerar PDF do Relatório", use_container_width=True, key=f"btn_pdf_final_{paciente_nome}"):
                            if not medico_nome:
                                st.warning("⚠️ Insira o nome do médico responsável")
                            elif not assinatura:
                                st.warning("⚠️ Digite a sua assinatura eletrónica")
                            else:
                                with st.spinner("Gerando relatório com QR Code..."):
                                    pdf_data = gerar_relatorio_pdf_com_qr(
                                        patient_data, 
                                        ultima_decisao, 
                                        medico_nome, 
                                        assinatura
                                    )
                                    if pdf_data:
                                        b64 = base64.b64encode(pdf_data).decode()
                                        href = f'''
                                        <a href="data:application/pdf;base64,{b64}" 
                                           download="relatorio_{patient_data.get('nome', 'paciente')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                                           style="display: inline-block; 
                                                  background: linear-gradient(135deg, #2E7D32, #4CAF50);
                                                  color: white;
                                                  padding: 12px 24px;
                                                  border-radius: 12px;
                                                  text-decoration: none;
                                                  font-weight: bold;
                                                  text-align: center;
                                                  width: 100%;
                                                  box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
                                                  transition: all 0.3s ease;">
                                            📥 Baixar PDF com QR Code
                                        </a>
                                        '''
                                        st.markdown(href, unsafe_allow_html=True)
                                        st.success("✅ Relatório PDF com QR Code gerado com sucesso!")
                                        st.info("📱 O QR Code pode ser escaneado para validar a autenticidade do relatório.")
                                    else:
                                        st.error("❌ Erro ao gerar o PDF")
                    
                    st.divider()
                    
                    if st.button("✅ Continuar para Lista de Pacientes", use_container_width=True, key="btn_continuar_lista"):
                        st.session_state.gerar_relatorio_apos_encaminhar = False
                        st.session_state.paciente_relatorio = None
                        st.rerun()
                
                st.stop()
    
    # ===== VERIFICAR E CRIAR TABELA =====
    if SUPABASE_AVAILABLE and 'tabela_verificada' not in st.session_state:
        with st.spinner("Verificando conexão com Supabase..."):
            sucesso, msg = criar_tabela_decisoes_clinicas()
            if sucesso:
                st.session_state.tabela_verificada = True
            else:
                st.session_state.erro_supabase = msg
    
    # ===== CARREGAR DECISÕES CLÍNICAS =====
    if SUPABASE_AVAILABLE and not st.session_state.medical_records:
        sucesso, dados = carregar_decisoes_clinicas_supabase()
        if sucesso and dados:
            st.session_state.medical_records = dados
    
    # ===== CARREGAR PACIENTES DO SUPABASE =====
    if SUPABASE_AVAILABLE:
        sucesso, dados = carregar_pacientes_supabase()
        if sucesso and dados:
            pacientes = []
            for item in dados:
                paciente = {
                    'id': item.get('id'),
                    'nome': item.get('nome_completo', 'N/A'),
                    'idade_meses': item.get('idade_meses', 0),
                    'peso_kg': item.get('peso', 0),
                    'altura_cm': item.get('altura', 0),
                    'muac_mm': item.get('muac', 0),
                    'hemoglobina': item.get('hemoglobina', None),
                    'tipo_anemia': item.get('tipo_anemia', None),
                    'densidade_parasitaria': item.get('densidade_parasitaria', None),
                    'diarreia': item.get('diarreia', None),
                    'doenca_cronica': item.get('doenca_cronica', None),
                    'doenca_cronica_especificar': item.get('doenca_cronica_especificar', None),
                    'anemia_risco': item.get('risco_anemia_nivel', 'N/A'),
                    'anemia_prob': item.get('risco_anemia_score', 0),
                    'diversidade_alimentar': item.get('dds_calculado', 0),
                    'data_registo': item.get('data_registo', 'N/A'),
                    'provincia': item.get('provincia', 'N/A'),
                    'distrito': item.get('distrito', 'N/A'),
                    'residencia': item.get('residencia', 'N/A'),
                    'hospital': item.get('hospital', 'N/A'),
                    'sexo': item.get('sexo', 'N/A')
                }
                pacientes.append(paciente)
            st.session_state.patients = pacientes
        else:
            if 'patients' not in st.session_state:
                st.session_state.patients = []
    
    # ===== MOSTRAR ERRO DO SUPABASE =====
    if st.session_state.erro_supabase:
        with st.expander("⚠️ Erro de conexão com Supabase", expanded=True):
            st.error(f"**Erro:** {st.session_state.erro_supabase}")
            st.info("💡 As decisões clínicas serão salvas localmente enquanto o problema não for resolvido.")
            if st.button("🔄 Tentar novamente", key="btn_tentar_novamente"):
                st.session_state.erro_supabase = None
                st.session_state.tabela_verificada = False
                st.rerun()
    
    # ===== VERIFICAR SE HÁ PACIENTES =====
    if 'patients' not in st.session_state or not st.session_state.patients:
        st.warning("⚠️ Nenhum paciente registado no sistema.")
        st.info("""
        📋 **Fluxo de Trabalho:**
        1. 👩🏾⚕️ Enfermeiro realiza a triagem e regista o paciente
        2. 📨 Pacientes com alto risco são encaminhados para o médico
        3. 👨🏾⚕️ Médico avalia, regista dados e faz o seguimento
        """)
        
        if st.button("🔄 Recarregar Pacientes", use_container_width=True):
            st.rerun()
        return
    
    patients = st.session_state.patients
    
    # ===== GARANTIR QUE O MODO DE EDIÇÃO SEJA MANTIDO =====
    if st.session_state.get('modo_edicao') and st.session_state.get('paciente_em_edicao'):
        paciente_em_edicao = st.session_state.paciente_em_edicao
        if paciente_em_edicao not in [p['nome'] for p in patients]:
            st.session_state.modo_edicao = False
            st.session_state.paciente_em_edicao = None
    
    # ===== ABAS =====
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Avaliação", 
        "📊 Dashboard", 
        "📜 Histórico", 
        "📨 Encaminhamentos"
    ])
    
    # ============================================================
    # ===== TAB 1: AVALIAÇÃO DO PACIENTE =====
    # ============================================================
    with tab1:
        st.subheader("👤 Gestão de Pacientes")
        
        # ===== IDENTIFICAR CASOS PENDENTES =====
        pacientes_pendentes = []
        pacientes_analisados = []
        
        for p in patients:
            if p.get('hemoglobina') is None or p.get('hemoglobina') == 0:
                pacientes_pendentes.append(p)
            else:
                pacientes_analisados.append(p)
        
        # ===== ESTATÍSTICAS =====
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👶 Total Pacientes", len(patients))
        with col2:
            st.metric("⏳ Pendentes", len(pacientes_pendentes), 
                     delta=f"{len(pacientes_pendentes)} aguardam" if pacientes_pendentes else "0")
        with col3:
            st.metric("✅ Analisados", len(pacientes_analisados))
        with col4:
            alto_risco_pendentes = len([p for p in pacientes_pendentes if p.get('anemia_risco') == 'ALTO'])
            st.metric("🔴 Alto Risco Pendente", alto_risco_pendentes)
        
        st.divider()
        
        # ===== LISTA DE CASOS PENDENTES =====
        if pacientes_pendentes:
            st.warning(f"⚠️ **{len(pacientes_pendentes)} casos aguardam avaliação médica**")
            
            df_pendentes = pd.DataFrame(pacientes_pendentes)
            st.dataframe(
                df_pendentes[['nome', 'idade_meses', 'anemia_risco', 'anemia_prob', 'data_registo']],
                use_container_width=True,
                column_config={
                    'nome': 'Paciente',
                    'idade_meses': 'Idade (meses)',
                    'anemia_risco': 'Risco',
                    'anemia_prob': 'Probabilidade (%)',
                    'data_registo': 'Data Registo'
                }
            )
            
            if st.button("📋 Avaliar Próximo Caso Pendente", use_container_width=True):
                primeiro_pendente = pacientes_pendentes[0]['nome']
                st.session_state.paciente_selecionado = primeiro_pendente
                st.session_state.paciente_em_edicao = primeiro_pendente
                st.session_state.modo_edicao = True
                st.rerun()
        else:
            st.success("✅ Todos os pacientes foram avaliados!")
        
        st.divider()
        
        # ===== SELEÇÃO DE PACIENTE =====
        st.subheader("👤 Selecionar Paciente para Avaliação")
        
        lista_pacientes = [p['nome'] for p in patients]
        
        paciente_inicial = st.session_state.get('paciente_selecionado')
        if paciente_inicial not in lista_pacientes:
            paciente_inicial = lista_pacientes[0] if lista_pacientes else None
        
        col1, col2 = st.columns([3, 1])
        with col1:
            selected = st.selectbox(
                "Selecionar Paciente", 
                lista_pacientes,
                index=lista_pacientes.index(paciente_inicial) if paciente_inicial in lista_pacientes else 0,
                key="paciente_selecionado_select"
            )
            st.session_state.paciente_selecionado = selected
        with col2:
            if st.button("🔄 Atualizar", use_container_width=True):
                st.rerun()
        
        patient_data = next((p for p in patients if p['nome'] == selected), None)
        
        if patient_data:
            st.divider()
            
            # ===== VERIFICAR SE JÁ FOI AVALIADO =====
            is_pendente = patient_data.get('hemoglobina') is None or patient_data.get('hemoglobina') == 0
            
            # Buscar todas as decisões deste paciente
            decisoes_paciente = []
            if st.session_state.medical_records:
                for r in st.session_state.medical_records:
                    if r.get('paciente') == selected:
                        decisoes_paciente.append(r)
            
            ultimo_record = decisoes_paciente[-1] if decisoes_paciente else None
            tem_decisao = len(decisoes_paciente) > 0
            
            # ===== VERIFICAR SE ESTÁ EM MODO DE EDIÇÃO =====
            is_editando = st.session_state.modo_edicao and st.session_state.paciente_em_edicao == selected
            
            # ===== SE FOR CASO PENDENTE, ATIVAR EDIÇÃO AUTOMATICAMENTE =====
            if is_pendente and not is_editando:
                st.session_state.modo_edicao = True
                st.session_state.paciente_em_edicao = selected
                is_editando = True
                st.rerun()
            
            # ===== MODO VISUALIZAÇÃO =====
            if not is_pendente and tem_decisao and not is_editando:
                st.success("✅ **Este caso já foi avaliado**")
                st.info(f"🔒 {len(decisoes_paciente)} decisão(ões) registrada(s). Clique em 'Editar' para adicionar nova decisão.")
                
                st.markdown(f"### 👶 {selected}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📊 Dados do Paciente")
                    st.markdown(f"**📅 Data de Registo:** {patient_data.get('data_registo', 'N/A')}")
                    st.markdown(f"**📍 Província:** {patient_data.get('provincia', 'N/A')}")
                    st.markdown(f"**📍 Distrito:** {patient_data.get('distrito', 'N/A')}")
                    st.markdown(f"**📍 Residência:** {patient_data.get('residencia', 'N/A')}")
                    st.markdown(f"**🏥 Hospital:** {patient_data.get('hospital', 'N/A')}")
                    st.markdown(f"**📏 Idade:** {patient_data['idade_meses']} meses")
                    st.markdown(f"**⚖️ Peso:** {patient_data['peso_kg']} kg")
                    st.markdown(f"**📐 Altura:** {patient_data['altura_cm']} cm")
                    st.markdown(f"**📏 MUAC:** {patient_data['muac_mm']} mm")
                
                with col2:
                    st.markdown("#### 🩺 Avaliação de Risco")
                    
                    hemoglobina = patient_data.get('hemoglobina')
                    if hemoglobina and hemoglobina > 0:
                        st.markdown(f"**🩸 Hemoglobina:** {hemoglobina} g/dL")
                        if hemoglobina < 11:
                            st.error("🔴 Hemoglobina baixa - anemia confirmada")
                        elif hemoglobina < 12:
                            st.warning("🟠 Hemoglobina limítrofe")
                        else:
                            st.success("🟢 Hemoglobina normal")
                    else:
                        st.warning("⚠️ Hemoglobina não registada")
                    
                    st.markdown(f"**📋 Tipo de Anemia:** {patient_data.get('tipo_anemia', 'N/A')}")
                    st.markdown(f"**🦟 Densidade Parasitária:** {patient_data.get('densidade_parasitaria', 'N/A')}")
                    st.markdown(f"**💧 Diarreia:** {patient_data.get('diarreia', 'N/A')}")
                    st.markdown(f"**🏥 Doença Crónica:** {patient_data.get('doenca_cronica', 'N/A')}")
                    st.markdown(f"**⚠️ Risco de Anemia:** {patient_data.get('anemia_risco', 'N/A')}")
                    st.markdown(f"**📊 DDS:** {patient_data.get('diversidade_alimentar', 0)}/9")
                    
                    if ultimo_record:
                        st.markdown("#### 📝 Última Decisão Clínica")
                        st.markdown(f"**Diagnóstico:** {ultimo_record.get('diagnostico', 'N/A')}")
                        st.markdown(f"**Prescrição:** {ultimo_record.get('prescricao', 'N/A')}")
                        st.markdown(f"**Seguimento:** {ultimo_record.get('seguimento', 'N/A')}")
                        st.markdown(f"**Data:** {ultimo_record.get('data', 'N/A')}")
                
                if st.button("✏️ Adicionar Nova Decisão", use_container_width=True, key="btn_editar_caso"):
                    st.session_state.modo_edicao = True
                    st.session_state.paciente_em_edicao = selected
                    st.rerun()
                
                # ===== GERAR RELATÓRIO =====
                st.divider()
                st.markdown("### 📄 Gerar Relatório")
                with st.expander("📊 Gerar Relatório PDF", expanded=False):
                    st.markdown("#### 📄 Relatório Clínico")
                    
                    if len(decisoes_paciente) > 1:
                        decisao_selecionada = st.selectbox(
                            "Selecionar decisão para o relatório:",
                            [f"{d.get('data', 'N/A')} - {d.get('diagnostico', 'N/A')[:30]}..." for d in decisoes_paciente],
                            key=f"select_decisao_relatorio_{selected}"
                        )
                        idx_selecionado = [f"{d.get('data', 'N/A')} - {d.get('diagnostico', 'N/A')[:30]}..." for d in decisoes_paciente].index(decisao_selecionada)
                        record_relatorio = decisoes_paciente[idx_selecionado]
                    else:
                        record_relatorio = ultimo_record
                    
                    medico_nome = st.text_input(
                        "Nome do Médico Responsável:",
                        placeholder="Dr. Nome Completo",
                        key=f"medico_nome_relatorio_{selected}"
                    )
                    
                    st.markdown("**✍️ Assinatura Eletrónica**")
                    assinatura = st.text_input(
                        "Digite a sua assinatura (nome completo):",
                        placeholder="Digite o seu nome para assinar eletronicamente",
                        key=f"assinatura_eletronica_{selected}"
                    )
                    
                    if st.button("📄 Gerar PDF com QR Code", use_container_width=True, key=f"btn_gerar_pdf_view_{selected}"):
                        if not medico_nome:
                            st.warning("⚠️ Por favor, insira o nome do médico responsável")
                        elif not assinatura:
                            st.warning("⚠️ Por favor, digite a sua assinatura eletrónica")
                        elif not record_relatorio:
                            st.warning("⚠️ Nenhuma decisão clínica disponível para este paciente")
                        else:
                            with st.spinner("Gerando relatório com QR Code..."):
                                pdf_data = gerar_relatorio_pdf_com_qr(
                                    patient_data, 
                                    record_relatorio, 
                                    medico_nome, 
                                    assinatura
                                )
                                if pdf_data:
                                    b64 = base64.b64encode(pdf_data).decode()
                                    href = f'''
                                    <a href="data:application/pdf;base64,{b64}" 
                                       download="relatorio_{patient_data.get('nome', 'paciente')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                                       style="display: inline-block; 
                                              background: linear-gradient(135deg, #2E7D32, #4CAF50);
                                              color: white;
                                              padding: 12px 24px;
                                              border-radius: 12px;
                                              text-decoration: none;
                                              font-weight: bold;
                                              text-align: center;
                                              width: 100%;
                                              box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
                                              transition: all 0.3s ease;">
                                        📥 Baixar PDF com QR Code
                                    </a>
                                    '''
                                    st.markdown(href, unsafe_allow_html=True)
                                    st.success("✅ Relatório PDF com QR Code gerado com sucesso!")
                                    st.info("📱 O QR Code pode ser escaneado para validar a autenticidade do relatório.")
                                else:
                                    st.error("❌ Erro ao gerar o PDF")
            
            # ===== MODO EDIÇÃO =====
            else:
                if is_editando:
                    st.info(f"✏️ **Editando: {selected}**")
                    st.info("💡 Preencha os campos abaixo e escolha uma ação:")
                    if st.button("🔒 Cancelar e Voltar", use_container_width=True, key=f"btn_cancelar_edicao_{selected}"):
                        st.session_state.modo_edicao = False
                        st.session_state.paciente_em_edicao = None
                        st.rerun()
                
                is_pendente_label = "⏳ **Este caso aguarda avaliação médica**" if is_pendente else f"📝 **Editando: {selected}**"
                st.warning(is_pendente_label)
                
                if decisoes_paciente:
                    with st.expander(f"📜 Histórico de Decisões ({len(decisoes_paciente)})", expanded=False):
                        for i, dec in enumerate(decisoes_paciente):
                            st.markdown(f"**{i+1}.** {dec.get('data', 'N/A')}")
                            st.markdown(f"   - Diagnóstico: {dec.get('diagnostico', 'N/A')}")
                            st.markdown(f"   - Prescrição: {dec.get('prescricao', 'N/A')}")
                            st.markdown(f"   - Seguimento: {dec.get('seguimento', 'N/A')}")
                            st.divider()
                
                st.markdown(f"### 👶 {selected}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📊 Dados do Paciente")
                    st.markdown(f"**📅 Data de Registo:** {patient_data.get('data_registo', 'N/A')}")
                    st.markdown(f"**📍 Província:** {patient_data.get('provincia', 'N/A')}")
                    st.markdown(f"**📍 Distrito:** {patient_data.get('distrito', 'N/A')}")
                    st.markdown(f"**📍 Residência:** {patient_data.get('residencia', 'N/A')}")
                    st.markdown(f"**🏥 Hospital:** {patient_data.get('hospital', 'N/A')}")
                    st.markdown(f"**📏 Idade:** {patient_data['idade_meses']} meses")
                    st.markdown(f"**⚖️ Peso:** {patient_data['peso_kg']} kg")
                    st.markdown(f"**📐 Altura:** {patient_data['altura_cm']} cm")
                    st.markdown(f"**📏 MUAC:** {patient_data['muac_mm']} mm")
                
                with col2:
                    st.markdown("#### 🩺 Avaliação de Risco")
                    
                    hemoglobina = patient_data.get('hemoglobina')
                    if hemoglobina and hemoglobina > 0:
                        st.markdown(f"**🩸 Hemoglobina:** {hemoglobina} g/dL")
                        if hemoglobina < 11:
                            st.error("🔴 Hemoglobina baixa - anemia confirmada")
                        elif hemoglobina < 12:
                            st.warning("🟠 Hemoglobina limítrofe")
                        else:
                            st.success("🟢 Hemoglobina normal")
                    else:
                        st.warning("⚠️ Hemoglobina não registada")
                    
                    st.markdown(f"**📋 Tipo de Anemia:** {patient_data.get('tipo_anemia', 'N/A')}")
                    st.markdown(f"**🦟 Densidade Parasitária:** {patient_data.get('densidade_parasitaria', 'N/A')}")
                    st.markdown(f"**💧 Diarreia:** {patient_data.get('diarreia', 'N/A')}")
                    st.markdown(f"**🏥 Doença Crónica:** {patient_data.get('doenca_cronica', 'N/A')}")
                    st.markdown(f"**⚠️ Risco de Anemia:** {patient_data.get('anemia_risco', 'N/A')}")
                    st.markdown(f"**📊 DDS:** {patient_data.get('diversidade_alimentar', 0)}/9")
                
                st.divider()
                
                # ===== ATUALIZAR DADOS CLÍNICOS =====
                st.markdown("### 🩺 Atualizar Dados Clínicos (opcional)")
                st.caption("Atualize os dados clínicos se necessário. Deixe em branco para manter os valores atuais.")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🩸 Hemoglobina**")
                    valor_atual_hb = patient_data.get('hemoglobina', 12.0)
                    if valor_atual_hb is None or valor_atual_hb == 0:
                        valor_atual_hb = 12.0
                    novo_valor_hb = st.number_input(
                        "Hemoglobina (g/dL):",
                        min_value=0.0,
                        max_value=20.0,
                        value=float(valor_atual_hb),
                        step=0.1,
                        key=f"hb_input_{selected}"
                    )
                
                with col2:
                    st.markdown("**📋 Tipo de Anemia**")
                    tipo_atual = patient_data.get('tipo_anemia', 'Selecionar...')
                    if tipo_atual is None or tipo_atual == "":
                        tipo_atual = "Selecionar..."
                    tipo_options = [
                        "Selecionar...",
                        "Anemia Ferropriva",
                        "Anemia da Doença Crónica",
                        "Anemia Hemolítica",
                        "Anemia Megaloblástica",
                        "Anemia Falciforme",
                        "Talassemia",
                        "Anemia Mista",
                        "Não Anemia",
                        "Em investigação"
                    ]
                    tipo_anemia_select = st.selectbox(
                        "Selecione o tipo:",
                        tipo_options,
                        index=tipo_options.index(tipo_atual) if tipo_atual in tipo_options else 0,
                        key=f"tipo_anemia_select_{selected}"
                    )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🦟 Densidade Parasitária**")
                    densidade_atual = patient_data.get('densidade_parasitaria', 'Selecionar...')
                    if densidade_atual is None or densidade_atual == "":
                        densidade_atual = "Selecionar..."
                    densidade_options = [
                        "Selecionar...",
                        "Negativa",
                        "Positiva - Baixa (< 1000)",
                        "Positiva - Média (1000-5000)",
                        "Positiva - Alta (> 5000)",
                        "Em análise"
                    ]
                    densidade_select = st.selectbox(
                        "Selecione o resultado:",
                        densidade_options,
                        index=densidade_options.index(densidade_atual) if densidade_atual in densidade_options else 0,
                        key=f"densidade_select_{selected}"
                    )
                
                with col2:
                    st.markdown("**💧 Diarreia**")
                    diarreia_atual = patient_data.get('diarreia', 'Selecionar...')
                    if diarreia_atual is None or diarreia_atual == "":
                        diarreia_atual = "Selecionar..."
                    diarreia_options = [
                        "Selecionar...",
                        "Não",
                        "Sim, 1-3 dias",
                        "Sim, 4-7 dias",
                        "Sim, mais de 7 dias",
                        "Em observação"
                    ]
                    diarreia_select = st.selectbox(
                        "Diarreia (últimas 2 semanas):",
                        diarreia_options,
                        index=diarreia_options.index(diarreia_atual) if diarreia_atual in diarreia_options else 0,
                        key=f"diarreia_select_{selected}"
                    )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🏥 Doença Crónica**")
                    doenca_atual = patient_data.get('doenca_cronica', 'Selecionar...')
                    if doenca_atual is None or doenca_atual == "":
                        doenca_atual = "Selecionar..."
                    doenca_options = [
                        "Selecionar...",
                        "Não",
                        "Sim - HIV/SIDA",
                        "Sim - Tuberculose",
                        "Sim - Doença Cardíaca",
                        "Sim - Doença Renal",
                        "Sim - Diabetes",
                        "Sim - Asma",
                        "Sim - Desnutrição Crónica",
                        "Sim - Outra"
                    ]
                    doenca_cronica_select = st.selectbox(
                        "Doença Crónica conhecida:",
                        doenca_options,
                        index=doenca_options.index(doenca_atual) if doenca_atual in doenca_options else 0,
                        key=f"doenca_cronica_select_{selected}"
                    )
                
                with col2:
                    st.markdown("**📋 Especificar Doença**")
                    doenca_especificar = st.text_input(
                        "Especifique a doença crónica (se aplicável):",
                        value=patient_data.get('doenca_cronica_especificar', ''),
                        placeholder="Ex: HIV em TARV, Cardiopatia congénita...",
                        key=f"doenca_especificar_input_{selected}"
                    )
                
                st.divider()
                
                # ===== SALVAR DADOS CLÍNICOS =====
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("💾 Atualizar Dados Clínicos", use_container_width=True, key=f"btn_salvar_dados_{selected}"):
                        if patient_data:
                            dados_atualizar = {}
                            alteracoes = False
                            
                            if novo_valor_hb != patient_data.get('hemoglobina', 0):
                                dados_atualizar['hemoglobina'] = novo_valor_hb
                                patient_data['hemoglobina'] = novo_valor_hb
                                alteracoes = True
                            
                            if tipo_anemia_select != "Selecionar..." and tipo_anemia_select != patient_data.get('tipo_anemia'):
                                dados_atualizar['tipo_anemia'] = tipo_anemia_select
                                patient_data['tipo_anemia'] = tipo_anemia_select
                                alteracoes = True
                            
                            if densidade_select != "Selecionar..." and densidade_select != patient_data.get('densidade_parasitaria'):
                                dados_atualizar['densidade_parasitaria'] = densidade_select
                                patient_data['densidade_parasitaria'] = densidade_select
                                alteracoes = True
                            
                            if diarreia_select != "Selecionar..." and diarreia_select != patient_data.get('diarreia'):
                                dados_atualizar['diarreia'] = diarreia_select
                                patient_data['diarreia'] = diarreia_select
                                alteracoes = True
                            
                            if doenca_cronica_select != "Selecionar..." and doenca_cronica_select != patient_data.get('doenca_cronica'):
                                dados_atualizar['doenca_cronica'] = doenca_cronica_select
                                patient_data['doenca_cronica'] = doenca_cronica_select
                                alteracoes = True
                                if doenca_especificar:
                                    dados_atualizar['doenca_cronica_especificar'] = doenca_especificar
                                    patient_data['doenca_cronica_especificar'] = doenca_especificar
                            
                            if alteracoes and dados_atualizar:
                                if SUPABASE_AVAILABLE and patient_data.get('id'):
                                    sucesso, resultado = atualizar_dados_clinicos_supabase(
                                        patient_data['id'], 
                                        dados_atualizar
                                    )
                                    if sucesso:
                                        st.success(f"✅ Dados clínicos de {selected} atualizados com sucesso!")
                                        recarregar_pacientes()
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Erro ao atualizar: {resultado}")
                                else:
                                    st.success(f"✅ Dados clínicos de {selected} atualizados localmente!")
                                    st.rerun()
                            elif not alteracoes:
                                st.warning("⚠️ Nenhum dado foi alterado")
                        else:
                            st.error("❌ Selecione um paciente válido")
                
                st.divider()
                
                # ===== NOVA DECISÃO CLÍNICA =====
                st.markdown("### 📝 Nova Decisão Clínica")
                st.caption("Preencha os campos abaixo para registrar uma nova decisão clínica para este paciente.")
                
                # Se a flag limpar_campos estiver ativa, limpa os campos
                if st.session_state.limpar_campos:
                    prescricao_valor = ""
                    diagnostico_valor = ""
                    observacoes_valor = ""
                    st.session_state.limpar_campos = False
                else:
                    prescricao_valor = prescricao if 'prescricao' in locals() else ""
                    diagnostico_valor = diagnostico if 'diagnostico' in locals() else ""
                    observacoes_valor = observacoes if 'observacoes' in locals() else ""
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 💊 Prescrição")
                    prescricao = st.text_area(
                        "Prescrição Médica:",
                        placeholder="Ex: Sulfato Ferroso 3mg/kg/dia, Ácido Fólico 0.4mg/dia...",
                        height=120,
                        key=f"prescricao_{selected}",
                        value=prescricao_valor
                    )
                
                with col2:
                    st.markdown("#### 📋 Diagnóstico")
                    diagnostico = st.text_area(
                        "Diagnóstico:",
                        placeholder="Ex: Anemia ferropriva moderada...",
                        height=120,
                        key=f"diagnostico_{selected}",
                        value=diagnostico_valor
                    )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 📅 Plano de Seguimento")
                    seguimento = st.selectbox(
                        "Próximo retorno:",
                        ["7 dias", "15 dias", "30 dias", "60 dias", "90 dias"],
                        key=f"seguimento_{selected}"
                    )
                with col2:
                    st.markdown("#### 📋 Observações")
                    observacoes = st.text_area(
                        "Observações adicionais:",
                        placeholder="Notas sobre o caso...",
                        height=80,
                        key=f"observacoes_{selected}",
                        value=observacoes_valor
                    )
                
                st.divider()
                
                # ============================================================
                # ===== BOTÃO 1: SALVAR DECISÃO =====
                # ============================================================
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("💾 Salvar Decisão", use_container_width=True, key=f"btn_salvar_decisao_{selected}"):
                        if prescricao or diagnostico:
                            nova_decisao = {
                                'paciente': selected,
                                'data': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                'diagnostico': diagnostico,
                                'prescricao': prescricao,
                                'seguimento': seguimento,
                                'observacoes': observacoes,
                                'hemoglobina': patient_data.get('hemoglobina', None),
                                'tipo_anemia': patient_data.get('tipo_anemia', None),
                                'densidade_parasitaria': patient_data.get('densidade_parasitaria', None),
                                'diarreia': patient_data.get('diarreia', None),
                                'doenca_cronica': patient_data.get('doenca_cronica', None)
                            }
                            
                            st.session_state.medical_records.append(nova_decisao)
                            
                            if SUPABASE_AVAILABLE:
                                sucesso_supabase, resultado = salvar_decisao_clinica_supabase(nova_decisao)
                                if sucesso_supabase:
                                    st.success(f"✅ Decisão de {selected} registada no Supabase!")
                                else:
                                    st.warning(f"⚠️ Decisão salva localmente. Erro: {resultado}")
                            else:
                                st.success(f"✅ Decisão de {selected} registada localmente!")
                            
                            # ===== GARANTIR QUE O MODO DE EDIÇÃO CONTINUA ATIVO =====
                            st.session_state.modo_edicao = True
                            st.session_state.paciente_em_edicao = selected
                            
                            st.rerun()
                        else:
                            st.warning("⚠️ Preencha diagnóstico ou prescrição")
                
                st.divider()
                
                # ============================================================
                # ===== BOTÃO 2: NOVA DECISÃO (LIMPA CAMPOS) =====
                # ============================================================
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🧹 Nova Decisão", use_container_width=True, key=f"btn_nova_decisao_{selected}"):
                        st.session_state.limpar_campos = True
                        st.rerun()
                    st.caption("Clique para limpar os campos e adicionar uma nova decisão")
                
                st.divider()
                
                # ============================================================
                # ===== BOTÃO 3: ENCAMINHAR =====
                # ============================================================
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown("### 📨 Encaminhamento Integrado")
                    st.markdown("""
                    <div style="background-color: #e8f5e9; padding: 10px; border-radius: 10px; border-left: 5px solid #2e7d32; margin-bottom: 10px; font-size: 0.85rem;">
                        <p style="font-weight: bold; color: #1b5e20;">🌿 Encaminhamento Integrado</p>
                        <p>O paciente será encaminhado simultaneamente para <strong>Nutricionista</strong> e <strong>Agrônomo</strong>.</p>
                        <p style="font-size: 0.8rem; color: #555;">💡 As decisões já salvas serão mantidas no histórico.</p>
                        <p style="font-size: 0.8rem; color: #555;">📄 Após encaminhar, poderá gerar o relatório com QR Code.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    urgencia_enc = st.selectbox(
                        "Nível de Urgência:",
                        ["Normal", "Urgente", "Muito Urgente"],
                        key=f"urgencia_enc_{selected}"
                    )
                    
                    if st.button("📨 Encaminhar", use_container_width=True, key=f"btn_encaminhar_{selected}"):
                        if selected and patient_data:
                            enc_existente = False
                            for e in st.session_state.encaminhamentos:
                                if e['paciente'] == selected and e.get('especialidade') in ['Nutricionista', 'Agrônomo'] and e.get('status') == 'Pendente':
                                    enc_existente = True
                                    break
                            
                            if enc_existente:
                                st.warning(f"⚠️ {selected} já possui encaminhamento ativo!")
                            else:
                                if prescricao or diagnostico:
                                    nova_decisao = {
                                        'paciente': selected,
                                        'data': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                        'diagnostico': diagnostico,
                                        'prescricao': prescricao,
                                        'seguimento': seguimento,
                                        'observacoes': observacoes,
                                        'hemoglobina': patient_data.get('hemoglobina', None),
                                        'tipo_anemia': patient_data.get('tipo_anemia', None),
                                        'densidade_parasitaria': patient_data.get('densidade_parasitaria', None),
                                        'diarreia': patient_data.get('diarreia', None),
                                        'doenca_cronica': patient_data.get('doenca_cronica', None)
                                    }
                                    
                                    st.session_state.medical_records.append(nova_decisao)
                                    
                                    if SUPABASE_AVAILABLE:
                                        sucesso_supabase, resultado = salvar_decisao_clinica_supabase(nova_decisao)
                                
                                # Criar encaminhamentos
                                dados_nutricionista = {
                                    'hemoglobina': patient_data.get('hemoglobina', None),
                                    'tipo_anemia': patient_data.get('tipo_anemia', None),
                                    'densidade_parasitaria': patient_data.get('densidade_parasitaria', None),
                                    'diarreia': patient_data.get('diarreia', None),
                                    'doenca_cronica': patient_data.get('doenca_cronica', None),
                                    'anemia_risco': patient_data.get('anemia_risco', 'N/A'),
                                    'dds': patient_data.get('diversidade_alimentar', 0),
                                    'muac': patient_data.get('muac_mm', 0),
                                    'idade_meses': patient_data.get('idade_meses', 0),
                                    'peso': patient_data.get('peso_kg', 0),
                                    'altura': patient_data.get('altura_cm', 0),
                                    'provincia': patient_data.get('provincia', 'N/A'),
                                    'distrito': patient_data.get('distrito', 'N/A'),
                                    'residencia': patient_data.get('residencia', 'N/A'),
                                    'hospital': patient_data.get('hospital', 'N/A')
                                }
                                
                                dados_agronomo = {
                                    'dds': patient_data.get('diversidade_alimentar', 0),
                                    'muac': patient_data.get('muac_mm', 0),
                                    'anemia_risco': patient_data.get('anemia_risco', 'N/A'),
                                    'provincia': patient_data.get('provincia', 'N/A'),
                                    'distrito': patient_data.get('distrito', 'N/A'),
                                    'residencia': patient_data.get('residencia', 'N/A'),
                                    'hospital': patient_data.get('hospital', 'N/A'),
                                    'producao_agricola': patient_data.get('producao_agricola', 'N/A'),
                                    'tipo_produtos': patient_data.get('tipo_produtos', 'N/A'),
                                    'acesso_terra': patient_data.get('acesso_terra', 'N/A'),
                                    'dificuldades_producao': patient_data.get('dificuldades_producao', 'N/A'),
                                    'idade_meses': patient_data.get('idade_meses', 0)
                                }
                                
                                encaminhamento_nutri = {
                                    'paciente': selected,
                                    'especialidade': 'Nutricionista',
                                    'urgencia': urgencia_enc,
                                    'motivo': "Encaminhamento integrado - Avaliação nutricional necessária",
                                    'data': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                    'status': 'Pendente',
                                    'medico_responsavel': st.session_state.get('username', 'Médico'),
                                    'dados_clinicos': dados_nutricionista
                                }
                                
                                encaminhamento_agro = {
                                    'paciente': selected,
                                    'especialidade': 'Agrônomo',
                                    'urgencia': urgencia_enc,
                                    'motivo': "Encaminhamento integrado - Intervenção agroalimentar necessária",
                                    'data': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                    'status': 'Pendente',
                                    'medico_responsavel': st.session_state.get('username', 'Médico'),
                                    'dados_clinicos': dados_agronomo
                                }
                                
                                st.session_state.encaminhamentos.append(encaminhamento_nutri)
                                st.session_state.encaminhamentos.append(encaminhamento_agro)
                                
                                st.success(f"✅ {selected} encaminhado para Nutricionista e Agrônomo!")
                                
                                if urgencia_enc == "Muito Urgente":
                                    st.error("🔴 ALTA URGÊNCIA!")
                                elif urgencia_enc == "Urgente":
                                    st.warning("🟠 URGENTE!")
                                
                                # Fechar modo de edição
                                st.session_state.modo_edicao = False
                                st.session_state.paciente_em_edicao = None
                                
                                st.session_state.gerar_relatorio_apos_encaminhar = True
                                st.session_state.paciente_relatorio = selected
                                
                                time.sleep(1.5)
                                st.rerun()
                        else:
                            st.warning("⚠️ Selecione um paciente válido")
                
                st.divider()
                
                # ============================================================
                # ===== BOTÃO 4: FECHAR CASO =====
                # ============================================================
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🔒 Fechar Caso", use_container_width=True, key=f"btn_fechar_caso_{selected}"):
                        st.session_state.modo_edicao = False
                        st.session_state.paciente_em_edicao = None
                        st.info(f"ℹ️ Caso de {selected} fechado.")
                        time.sleep(1)
                        st.rerun()
                
                st.divider()
                
                # ============================================================
                # ===== GERAR RELATÓRIO (CORRIGIDO) =====
                # ============================================================
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown("### 📄 Gerar Relatório")
                    
                    with st.expander("📊 Gerar Relatório PDF", expanded=False):
                        st.markdown("#### 📄 Relatório Clínico")
                        
                        medico_nome = st.text_input(
                            "Nome do Médico Responsável:",
                            placeholder="Dr. Nome Completo",
                            key=f"medico_nome_relatorio_edit_{selected}"
                        )
                        
                        st.markdown("**✍️ Assinatura Eletrónica**")
                        assinatura = st.text_input(
                            "Digite a sua assinatura (nome completo):",
                            placeholder="Digite o seu nome para assinar eletronicamente",
                            key=f"assinatura_eletronica_edit_{selected}"
                        )
                        
                        st.markdown("""
                        <div style="background-color: #e8f5e9; padding: 10px; border-radius: 8px; border-left: 4px solid #2e7d32; font-size: 0.85rem;">
                            <p style="font-weight: bold; color: #1b5e20;">ℹ️ Informação</p>
                            <p>O relatório será gerado com os dados do paciente e a decisão clínica atual.</p>
                            <p>A assinatura eletrónica confirma a autoria do relatório.</p>
                            <p>📱 O QR Code permite validar a autenticidade do documento.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("📄 Gerar PDF com QR Code", use_container_width=True, key=f"btn_gerar_pdf_edit_{selected}"):
                            if not medico_nome:
                                st.warning("⚠️ Por favor, insira o nome do médico responsável")
                            elif not assinatura:
                                st.warning("⚠️ Por favor, digite a sua assinatura eletrónica")
                            else:
                                # ===== OBTER VALORES DE FORMA SEGURA =====
                                try:
                                    diag = diagnostico if 'diagnostico' in locals() and diagnostico else ""
                                except:
                                    diag = ""
                                
                                try:
                                    presc = prescricao if 'prescricao' in locals() and prescricao else ""
                                except:
                                    presc = ""
                                
                                try:
                                    seg = seguimento if 'seguimento' in locals() and seguimento else "30 dias"
                                except:
                                    seg = "30 dias"
                                
                                try:
                                    obs = observacoes if 'observacoes' in locals() and observacoes else "N/A"
                                except:
                                    obs = "N/A"
                                
                                if not diag and not presc:
                                    st.warning("⚠️ Preencha o diagnóstico ou a prescrição antes de gerar o relatório")
                                else:
                                    record_temp = {
                                        'data': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                        'diagnostico': diag if diag else "Não especificado",
                                        'prescricao': presc if presc else "Não especificada",
                                        'seguimento': seg,
                                        'observacoes': obs
                                    }
                                    
                                    with st.spinner("Gerando relatório com QR Code..."):
                                        pdf_data = gerar_relatorio_pdf_com_qr(
                                            patient_data, 
                                            record_temp, 
                                            medico_nome, 
                                            assinatura
                                        )
                                        if pdf_data:
                                            b64 = base64.b64encode(pdf_data).decode()
                                            href = f'''
                                            <a href="data:application/pdf;base64,{b64}" 
                                               download="relatorio_{patient_data.get('nome', 'paciente')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                                               style="display: inline-block; 
                                                      background: linear-gradient(135deg, #2E7D32, #4CAF50);
                                                      color: white;
                                                      padding: 12px 24px;
                                                      border-radius: 12px;
                                                      text-decoration: none;
                                                      font-weight: bold;
                                                      text-align: center;
                                                      width: 100%;
                                                      box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
                                                      transition: all 0.3s ease;">
                                                📥 Baixar PDF com QR Code
                                            </a>
                                            '''
                                            st.markdown(href, unsafe_allow_html=True)
                                            st.success("✅ Relatório PDF com QR Code gerado com sucesso!")
                                            st.info("📱 O QR Code pode ser escaneado para validar a autenticidade do relatório.")
                                        else:
                                            st.error("❌ Erro ao gerar o PDF")
    
    # ============================================================
    # ===== TAB 2: DASHBOARD =====
    # ============================================================
    with tab2:
        st.subheader("📊 Dashboard de Acompanhamento")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total = len(patients)
            st.metric("👶 Total Pacientes", total)
        
        with col2:
            hb_baixa = sum(1 for p in patients if p.get('hemoglobina') is not None and p.get('hemoglobina', 12) < 11)
            st.metric("🩸 Hb < 11 g/dL", hb_baixa)
        
        with col3:
            alto_risco = sum(1 for p in patients if p.get('anemia_risco') == 'ALTO')
            st.metric("🔴 Alto Risco", alto_risco)
        
        with col4:
            seguidos = len(st.session_state.medical_records)
            st.metric("📋 Decisões Registadas", seguidos)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if patients and 'anemia_risco' in patients[0]:
                df = pd.DataFrame(patients)
                fig = px.pie(df, names='anemia_risco', 
                            title='Distribuição de Risco de Anemia',
                            color='anemia_risco',
                            color_discrete_map={'ALTO': '#c62828', 'MÉDIO': '#ef6c00', 'BAIXO': '#2e7d32'})
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if patients and 'tipo_anemia' in patients[0]:
                df = pd.DataFrame(patients)
                df_valid = df[df['tipo_anemia'].notna() & (df['tipo_anemia'] != "Selecionar...")]
                if not df_valid.empty:
                    fig = px.pie(df_valid, names='tipo_anemia', 
                                title='Distribuição - Tipo de Anemia')
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📋 Nenhum tipo de anemia registado")
        
        st.subheader("📋 Lista de Pacientes")
        df_patients = pd.DataFrame(patients)
        colunas_mostrar = ['nome', 'idade_meses', 'hemoglobina', 'tipo_anemia', 'densidade_parasitaria', 
                          'diarreia', 'doenca_cronica', 'anemia_risco']
        colunas_existentes = [c for c in colunas_mostrar if c in df_patients.columns]
        st.dataframe(df_patients[colunas_existentes], use_container_width=True)
    
    # ============================================================
    # ===== TAB 3: HISTÓRICO =====
    # ============================================================
    with tab3:
        st.subheader("📜 Histórico de Decisões Clínicas")
        
        if st.session_state.medical_records:
            df_records = pd.DataFrame(st.session_state.medical_records)
            st.dataframe(df_records[['paciente', 'data', 'diagnostico', 'prescricao', 'seguimento']], 
                        use_container_width=True)
            
            st.subheader("🔍 Detalhes por Paciente")
            selected_hist = st.selectbox(
                "Selecione um paciente para ver histórico:",
                df_records['paciente'].unique().tolist()
            )
            
            if selected_hist:
                df_paciente = df_records[df_records['paciente'] == selected_hist]
                for _, row in df_paciente.iterrows():
                    with st.expander(f"📋 {row['data']}"):
                        st.markdown(f"**Diagnóstico:** {row['diagnostico']}")
                        st.markdown(f"**Prescrição:** {row['prescricao']}")
                        st.markdown(f"**Seguimento:** {row['seguimento']}")
                        st.markdown(f"**Observações:** {row.get('observacoes', 'N/A')}")
                        st.markdown(f"**Hemoglobina:** {row.get('hemoglobina', 'N/A')} g/dL")
                        st.markdown(f"**Tipo Anemia:** {row.get('tipo_anemia', 'N/A')}")
        else:
            st.info("📋 Nenhum registo clínico disponível ainda.")
    
    # ============================================================
    # ===== TAB 4: ENCAMINHAMENTOS =====
    # ============================================================
    with tab4:
        st.subheader("📨 Gestão de Encaminhamentos")
        
        if 'encaminhamentos' in st.session_state and st.session_state.encaminhamentos:
            df_enc = pd.DataFrame(st.session_state.encaminhamentos)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📋 Total", len(df_enc))
            with col2:
                pendentes = len(df_enc[df_enc['status'] == 'Pendente'])
                st.metric("⏳ Pendentes", pendentes)
            with col3:
                if 'especialidade' in df_enc.columns:
                    nutri = len(df_enc[df_enc['especialidade'] == 'Nutricionista'])
                    st.metric("🍎 Nutricionista", nutri)
                else:
                    st.metric("🍎 Nutricionista", 0)
            with col4:
                if 'especialidade' in df_enc.columns:
                    agro = len(df_enc[df_enc['especialidade'] == 'Agrônomo'])
                    st.metric("🌾 Agrônomo", agro)
                else:
                    st.metric("🌾 Agrônomo", 0)
            
            st.divider()
            
            st.subheader("🔍 Filtrar Encaminhamentos")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                especialidade_filtro = st.selectbox(
                    "Especialidade:",
                    ["Todas", "Nutricionista", "Agrônomo"],
                    key="filtro_especialidade"
                )
            with col2:
                status_filtro = st.selectbox(
                    "Status:",
                    ["Todos", "Pendente", "Em andamento", "Concluído"],
                    key="filtro_status"
                )
            with col3:
                data_inicio = st.date_input(
                    "Data de Início:",
                    value=datetime.now() - timedelta(days=30),
                    key="filtro_data_inicio"
                )
                data_fim = st.date_input(
                    "Data de Fim:",
                    value=datetime.now(),
                    key="filtro_data_fim"
                )
            
            df_filtrado = df_enc.copy()
            
            if especialidade_filtro != "Todas":
                df_filtrado = df_filtrado[df_filtrado['especialidade'] == especialidade_filtro]
            
            if status_filtro != "Todos":
                df_filtrado = df_filtrado[df_filtrado['status'] == status_filtro]
            
            if 'data' in df_filtrado.columns:
                df_filtrado['data_filtro'] = pd.to_datetime(df_filtrado['data']).dt.date
                df_filtrado = df_filtrado[
                    (df_filtrado['data_filtro'] >= data_inicio) & 
                    (df_filtrado['data_filtro'] <= data_fim)
                ]
            
            st.info(f"📋 Mostrando {len(df_filtrado)} encaminhamentos")
            
            colunas_tabela = ['paciente', 'especialidade', 'urgencia', 'data', 'status']
            colunas_existentes = [c for c in colunas_tabela if c in df_filtrado.columns]
            st.dataframe(df_filtrado[colunas_existentes], use_container_width=True)
            
            st.subheader("🔍 Detalhes do Encaminhamento")
            
            if not df_filtrado.empty:
                selected_enc = st.selectbox(
                    "Selecione um encaminhamento para ver detalhes:",
                    df_filtrado['paciente'].unique().tolist(),
                    key="select_enc_detalhes"
                )
                
                if selected_enc:
                    df_selected = df_filtrado[df_filtrado['paciente'] == selected_enc]
                    for idx, row in df_selected.iterrows():
                        titulo = f"📋 {row.get('especialidade', 'N/A')} - {row['data']}"
                        with st.expander(titulo, expanded=True):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"**Paciente:** {row['paciente']}")
                                st.markdown(f"**Especialidade:** {row.get('especialidade', 'N/A')}")
                                st.markdown(f"**Urgência:** {row.get('urgencia', 'Normal')}")
                                st.markdown(f"**Status:** {row.get('status', 'Pendente')}")
                                st.markdown(f"**Data:** {row['data']}")
                                st.markdown(f"**Médico:** {row.get('medico_responsavel', 'N/A')}")
                            
                            with col2:
                                st.markdown("**Motivo:**")
                                st.markdown(f"{row.get('motivo', 'Não especificado')}")
                            
                            st.markdown("**📊 Dados Clínicos Enviados:**")
                            dados_clinicos = obter_dados_clinicos(row)
                            if dados_clinicos:
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown(f"- Hemoglobina: {dados_clinicos.get('hemoglobina', 'N/A')} g/dL")
                                    st.markdown(f"- Tipo de Anemia: {dados_clinicos.get('tipo_anemia', 'N/A')}")
                                    st.markdown(f"- Densidade Parasitária: {dados_clinicos.get('densidade_parasitaria', 'N/A')}")
                                with col2:
                                    st.markdown(f"- DDS: {dados_clinicos.get('dds', 0)}/9")
                                    st.markdown(f"- MUAC: {dados_clinicos.get('muac', 0)} mm")
                                    st.markdown(f"- Risco de Anemia: {dados_clinicos.get('anemia_risco', 'N/A')}")
                            else:
                                st.info("📋 Dados clínicos não disponíveis")
                            
                            if row.get('status') == 'Pendente':
                                if st.button(
                                    f"✅ Marcar como Concluído - {row['paciente']}", 
                                    key=f"btn_concluir_{idx}_{row['paciente']}_{row['data']}"
                                ):
                                    for enc in st.session_state.encaminhamentos:
                                        if enc['paciente'] == selected_enc and enc['data'] == row['data']:
                                            enc['status'] = 'Concluído'
                                            st.rerun()
            else:
                st.info("📋 Nenhum encaminhamento com os filtros selecionados.")
        else:
            st.info("📋 Nenhum encaminhamento registado ainda.")

# ========== MAIN ==========
if __name__ == "__main__":
    render_medico()
    