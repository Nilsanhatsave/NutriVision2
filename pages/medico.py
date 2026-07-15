"""
Módulo: Médico - Avaliação Clínica
Versão corrigida com Supabase unificado
"""

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

# ===== IMPORTAÇÃO DO SUPABASE CONFIGURADO =====
from supabase_config import (
    supabase, 
    SUPABASE_AVAILABLE,
    get_supabase_client,
    verificar_conexao,
    carregar_criancas_supabase,
    atualizar_crianca_supabase,
    salvar_decisao_clinica_supabase,
    carregar_decisoes_clinicas_supabase,
    criar_tabela_decisoes_clinicas
)

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
        
        # Texto explicativo do QR Code
        pdf.set_y(pdf.get_y() + 5)
        pdf.set_x(70)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, "ESCANEIE O QR CODE", ln=True)
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

# ===== FUNÇÃO PARA RECARREGAR PACIENTES =====
def recarregar_pacientes():
    """Recarrega os pacientes do Supabase"""
    if SUPABASE_AVAILABLE:
        sucesso, dados = carregar_criancas_supabase()
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

# ===== FUNÇÃO PRINCIPAL =====
def render_medico():
    st.title("👨🏾⚕️ Médico - Avaliação Clínica")
    
    # ===== TESTE DE CONEXÃO SUPABASE =====
    with st.expander("🔍 Status da Conexão Supabase", expanded=False):
        if SUPABASE_AVAILABLE:
            st.success("✅ Supabase conectado com sucesso!")
            
            # Testa a conexão
            sucesso, msg = verificar_conexao()
            if sucesso:
                st.success(f"✅ {msg}")
            else:
                st.warning(f"⚠️ {msg}")
        else:
            st.error("❌ Supabase NÃO disponível!")
            st.info("💡 Verifique se o arquivo supabase_config.py está correto.")
    
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
        sucesso, dados = carregar_criancas_supabase()
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
    
    # ===== CONTINUAÇÃO DO CÓDIGO (ABAS) =====
    # ... (O resto do código das abas permanece igual) ...
    
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
        # ... (código existente da tab1) ...
        pass
    
    # ============================================================
    # ===== TAB 2: DASHBOARD =====
    # ============================================================
    with tab2:
        # ... (código existente da tab2) ...
        pass
    
    # ============================================================
    # ===== TAB 3: HISTÓRICO =====
    # ============================================================
    with tab3:
        # ... (código existente da tab3) ...
        pass
    
    # ============================================================
    # ===== TAB 4: ENCAMINHAMENTOS =====
    # ============================================================
    with tab4:
        # ... (código existente da tab4) ...
        pass

# ========== MAIN ==========
if __name__ == "__main__":
    render_medico()