# pages/enfermeiro.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# ===== IMPORTAR SUPABASE =====
try:
    from supabase_client import SUPABASE_AVAILABLE, salvar_crianca_supabase, carregar_criancas_supabase
except ImportError:
    SUPABASE_AVAILABLE = False
    def salvar_crianca_supabase(dados):
        return False, "Supabase nao disponivel"
    def carregar_criancas_supabase():
        return False, []

# ========== CLASSE IA ==========
class IAClassifier:
    def __init__(self):
        self.historico_predicoes = []
    
    def predict_anemia(self, data):
        score = 0
        fatores = []
        confianca = 0.85 + random.uniform(-0.05, 0.05)
        
        if data['muac'] < 115:
            score += 25
            fatores.append("MUAC critico (<115mm)")
        elif data['muac'] < 125:
            score += 20
            fatores.append("MUAC baixo (<125mm)")
        elif data['muac'] < 135:
            score += 10
            fatores.append("MUAC limitrofe")
        
        if data['altura'] > 0 and data['peso'] > 0:
            imc = data['peso'] / ((data['altura']/100) ** 2)
            if imc < 14:
                score += 20
                fatores.append(f"IMC muito baixo ({imc:.1f})")
            elif imc < 16:
                score += 15
                fatores.append(f"IMC baixo ({imc:.1f})")
            elif imc < 18.5:
                score += 8
                fatores.append(f"IMC abaixo do normal ({imc:.1f})")
        
        if data['edema'] == "Presente":
            score += 15
            fatores.append("Edema presente")
        
        if data['perda_peso'] == "Sim":
            score += 10
            fatores.append("Perda de peso recente")
        
        dds = data.get('dds_calculado', 0)
        if dds <= 2:
            score += 25
            fatores.append("DDS muito baixo")
        elif dds <= 3:
            score += 20
            fatores.append("DDS baixo")
        
        if data['refeicoes_dia'] == "1":
            score += 15
            fatores.append("Apenas 1 refeicao/dia")
        elif data['refeicoes_dia'] == "2":
            score += 8
            fatores.append("Apenas 2 refeicoes/dia")
        
        resultado = self._classificar(score)
        return resultado, score, fatores[:5], min(0.99, confianca)
    
    def predict_fome_oculta(self, data):
        score = 0
        fatores = []
        confianca = 0.85 + random.uniform(-0.05, 0.05)
        
        dds = data.get('dds_calculado', 0)
        if dds <= 2:
            score += 30
            fatores.append("DDS muito baixo")
        elif dds <= 3:
            score += 20
            fatores.append("DDS baixo")
        
        if data['cabelo'] == "Despigmentado fino e raro":
            score += 15
            fatores.append("Cabelo despigmentado")
        elif data['cabelo'] == "Despigmentado":
            score += 10
            fatores.append("Cabelo despigmentado")
        
        if data['mucosa'] == "Muito Hipocoradas":
            score += 15
            fatores.append("Mucosas muito hipocoradas")
        elif data['mucosa'] == "Hipocoradas":
            score += 10
            fatores.append("Mucosas hipocoradas")
        
        resultado = self._classificar(score)
        return resultado, score, fatores[:5], min(0.99, confianca)
    
    def predict_inseguranca(self, data):
        score = 0
        fatores = []
        confianca = 0.85 + random.uniform(-0.05, 0.05)
        
        dds = data.get('dds_calculado', 0)
        if dds <= 2:
            score += 25
            fatores.append("DDS muito baixo")
        
        if data['refeicoes_dia'] == "1":
            score += 20
            fatores.append("Apenas 1 refeicao/dia")
        elif data['refeicoes_dia'] == "2":
            score += 10
            fatores.append("Apenas 2 refeicoes/dia")
        
        if data['muac'] < 115:
            score += 15
            fatores.append("MUAC critico")
        elif data['muac'] < 125:
            score += 10
            fatores.append("MUAC baixo")
        
        resultado = self._classificar(score)
        return resultado, score, fatores[:5], min(0.99, confianca)
    
    def _classificar(self, score):
        if score >= 50:
            return "ALTO"
        elif score >= 30:
            return "MEDIO"
        else:
            return "BAIXO"

# ========== FUNÇÃO PARA CALCULAR IDADE ==========
def calcular_idade(data_nascimento):
    hoje = datetime.now().date()
    if data_nascimento <= hoje:
        meses = (hoje.year - data_nascimento.year) * 12 + (hoje.month - data_nascimento.month)
        if hoje.day < data_nascimento.day:
            meses -= 1
        return max(0, meses)
    return 0

# ========== FUNÇÃO PRINCIPAL ==========
def render_enfermeiro():
    st.title("👩🏾⚕️ Enfermeiro - Triagem Nutricional")
    st.markdown("Avaliação de risco de anemia, fome oculta e insegurança alimentar")
    
    # ===== CARREGAR DADOS DO SUPABASE =====
    if 'criancas' not in st.session_state:
        if SUPABASE_AVAILABLE:
            sucesso, dados = carregar_criancas_supabase()
            if sucesso and dados:
                st.session_state.criancas = dados
                st.success(f"✅ {len(dados)} registos carregados do Supabase!")
            else:
                st.session_state.criancas = []
                st.info("📋 Nenhum registo encontrado")
        else:
            st.session_state.criancas = []
            st.warning("⚠️ Supabase não disponível")
    
    if 'ia_classifier' not in st.session_state:
        st.session_state.ia_classifier = IAClassifier()
    
    if 'dados_basicos_salvos' not in st.session_state:
        st.session_state.dados_basicos_salvos = False
    if 'nome_salvo' not in st.session_state:
        st.session_state.nome_salvo = ""
    if 'data_salva' not in st.session_state:
        st.session_state.data_salva = None
    if 'idade_calculada' not in st.session_state:
        st.session_state.idade_calculada = 0
    
    with st.form("triagem_form", clear_on_submit=False):
        
        st.markdown("### 👶 DADOS DA CRIANÇA")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            primeiro_nome = st.text_input("Primeiro Nome", placeholder="Ex: João")
        with col2:
            nome_meio = st.text_input("Nome do Meio", placeholder="Ex: Manuel")
        with col3:
            ultimo_nome = st.text_input("Apelido", placeholder="Ex: Silva")
        nome_completo = f"{primeiro_nome} {nome_meio} {ultimo_nome}".strip()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            data_nascimento = st.date_input("📅 Data de Nascimento", value=datetime.now() - timedelta(days=730), max_value=datetime.now())
            idade_meses = calcular_idade(data_nascimento)
        with col2:
            if st.form_submit_button("💾 Salvar Dados", use_container_width=True):
                if nome_completo:
                    st.session_state.dados_basicos_salvos = True
                    st.session_state.nome_salvo = nome_completo
                    st.session_state.data_salva = data_nascimento
                    st.session_state.idade_calculada = idade_meses
                    st.success(f"✅ {nome_completo} - {idade_meses} meses")
                    st.rerun()
                else:
                    st.warning("⚠️ Preencha o nome completo")
        
        if not st.session_state.dados_basicos_salvos:
            st.warning("⚠️ Clique em 'Salvar Dados' para continuar.")
            st.stop()
        
        nome_completo = st.session_state.nome_salvo
        data_nascimento = st.session_state.data_salva
        idade_meses = st.session_state.idade_calculada
        
        st.info(f"👶 {nome_completo} - {idade_meses} meses")
        st.divider()
        
        st.markdown("### 📍 LOCALIZAÇÃO")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            provincia = st.selectbox("Província", ["Cabo Delgado", "Gaza", "Inhambane", "Manica", "Maputo Cidade", "Maputo Província", "Nampula", "Niassa", "Sofala", "Tete", "Zambézia"])
        with col2:
            distrito = st.text_input("Distrito")
        with col3:
            residencia = st.text_input("Local de Residência")
        with col4:
            hospital = st.text_input("Hospital/Unidade Sanitária")
        st.divider()
        
        st.markdown("### 👩 DADOS DA MÃE")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            nome_mae = st.text_input("Nome da Mãe", placeholder="Ex: Maria")
        with col2:
            idade_mae = st.number_input("Idade da Mãe (anos)", 12, 60, 25)
        with col3:
            escolaridade_mae = st.selectbox("Escolaridade da Mãe", ["Nenhum", "Ensino Primário", "Ensino Secundário", "Ensino Superior"])
        with col4:
            ocupacao_mae = st.text_input("Ocupação da Mãe")
        col1, col2 = st.columns(2)
        with col1:
            agregado_familiar_mae = st.number_input("Nº de Pessoas no Agregado", 1, 20, 5)
        with col2:
            rendimento_familiar_mae = st.number_input("Rendimento Familiar (MZN)", 0, 100000, 5000)
        st.divider()
        
        st.markdown("### 📏 AVALIAÇÃO ANTROPOMÉTRICA")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            peso = st.number_input("Peso (kg)", 0.0, 50.0, 10.0, 0.1)
        with col2:
            altura = st.number_input("Altura (cm)", 0.0, 120.0, 85.0, 0.1)
        with col3:
            muac = st.number_input("MUAC (mm)", 0, 200, 130)
        with col4:
            if altura > 0 and peso > 0:
                imc = peso / ((altura/100) ** 2)
                st.metric("IMC", f"{imc:.1f}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            edema = st.radio("Edema", ["Ausente", "Presente"], horizontal=True)
        with col2:
            perda_peso = st.selectbox("Perda de peso", ["Não", "Sim"])
        with col3:
            apatia = st.selectbox("Apatia", ["Não", "Sim"])
        with col4:
            febre = st.selectbox("Febre", ["Não", "Sim"])
        
        diarreia = st.selectbox("💧 Diarreia (últimas 2 semanas)", ["Não", "Sim, 1-3 dias", "Sim, 4-7 dias", "Sim, mais de 7 dias"])
        doenca_cronica = st.selectbox("🏥 Doença Crónica", ["Nenhuma", "HIV/SIDA", "Tuberculose", "Doença Cardíaca", "Doença Renal", "Diabetes", "Asma", "Desnutrição Crónica", "Outra"])
        if doenca_cronica == "Outra":
            doenca_especificar = st.text_input("Especifique a doença:")
        else:
            doenca_especificar = ""
        st.divider()
        
        st.markdown("### 💇 AVALIAÇÃO FÍSICA")
        col1, col2 = st.columns(2)
        with col1:
            cabelo = st.selectbox("Cabelo", ["Pigmentado e abundante", "Pigmentado e fino", "Despigmentado", "Despigmentado fino e raro"])
        with col2:
            mucosa = st.selectbox("Mucosas", ["Coradas", "Hipocoradas", "Muito Hipocoradas"])
        st.divider()
        
        st.markdown("### 💊 SUPLEMENTAÇÃO")
        col1, col2, col3 = st.columns(3)
        with col1:
            suplementacao_ferro = st.selectbox("Suplementação de Ferro", ["Não", "Sim", "Em curso"])
        with col2:
            suplementacao_vit_a = st.selectbox("Suplementação Vitamina A", ["Não", "Sim", "Em curso"])
        with col3:
            desparasitacao = st.selectbox("Desparasitação", ["Não", "Sim", "Não sabe"])
        st.divider()
        
        st.markdown("### 🍽️ HISTÓRICO ALIMENTAR")
        col1, col2, col3 = st.columns(3)
        with col1:
            if idade_meses > 24:
                amamentacao = "Não"
                meses_amamentacao = 0
                st.info("🚫 Amamentação desativada (>24 meses)")
            else:
                amamentacao = st.selectbox("Amamentação", ["Não", "Sim"])
                if amamentacao == "Sim":
                    meses_amamentacao = st.number_input("Meses amamentação exclusiva", 0, 24, 6)
                else:
                    meses_amamentacao = 0
        with col2:
            refeicoes_dia = st.selectbox("Refeições por dia", ["1", "2", "3", "4", "5+"])
        with col3:
            dds_score = st.slider("Diversidade Alimentar (DDS)", 0, 9, 5)
        st.divider()
        
        st.markdown("### 🥗 ALIMENTOS CONSUMIDOS")
        alimentos = {
            "Frutas": ["Banana", "Manga", "Laranja", "Goiaba"],
            "Carnes": ["Carne bovina", "Carne de frango", "Carne de cabra"],
            "Peixe": ["Peixe fresco", "Peixe seco"],
            "Ovos": ["Ovo de galinha"],
            "Leguminosas": ["Feijão", "Amendoim"],
            "Cereais": ["Milho", "Arroz", "Mandioca"],
            "Verduras": ["Espinafre", "Couve", "Cenoura"]
        }
        selecionados = []
        col1, col2, col3 = st.columns(3)
        for idx, (categoria, items) in enumerate(alimentos.items()):
            col = [col1, col2, col3][idx % 3]
            with col:
                st.markdown(f"**{categoria}**")
                for item in items:
                    if st.checkbox(item, key=f"alim_{item}"):
                        selecionados.append(item)
                st.markdown("---")
        
        grupos = 0
        for categoria, items in alimentos.items():
            for item in items:
                if item in selecionados:
                    grupos += 1
                    break
        dds_calculado = min(9, grupos)
        
        # ===== PRODUÇÃO AGRÍCOLA =====
        st.markdown("### 🌾 PRODUÇÃO AGRÍCOLA")
        
        col1, col2 = st.columns(2)
        with col1:
            producao_familiar = st.selectbox(
                "1. A família produz alimentos?",
                ["Produz para consumo", "Produz para venda", "Produz para consumo e venda", "Não produz"],
                key="producao_familiar"
            )
        with col2:
            acesso_terra = st.selectbox(
                "2. A família tem acesso à terra?",
                ["Tem terra própria", "Tem terra comunitária", "Tem terra arrendada", "Não tem terra"],
                key="acesso_terra"
            )
        
        col1, col2 = st.columns(2)
        with col1:
            culturas_produzidas = st.selectbox(
                "3. Principais culturas produzidas:",
                ["Milho", "Feijão", "Mandioca", "Amendoim", "Batata Doce", 
                 "Hortaliças", "Frutas", "Arroz", "Cana-de-Açúcar", "Outra"],
                key="culturas_produzidas"
            )
            if culturas_produzidas == "Outra":
                outras_culturas = st.text_input("Especifique outras culturas:", key="outras_culturas")
            else:
                outras_culturas = ""
        with col2:
            fonte_agua = st.selectbox(
                "4. Fonte de água para produção:",
                ["Rio", "Poço", "Furo", "Lago", "Nascente", "Água da chuva", "Sistema de irrigação", "Nenhuma"],
                key="fonte_agua"
            )
        
        dificuldades = st.selectbox(
            "5. Principais dificuldades na produção:",
            ["Falta de sementes", "Falta de fertilizantes/adubo", "Solo pouco fértil", 
             "Pragas e doenças", "Falta de chuva/seca", "Cheias/excesso de chuva", 
             "Falta de conhecimento técnico", "Falta de mão de obra", 
             "Falta de equipamento agrícola", "Nenhuma dificuldade"],
            key="dificuldades"
        )
        
        st.divider()
        
        submitted = st.form_submit_button("🧮 Calcular Risco", use_container_width=True)
    
    if submitted:
        if idade_meses >= 60:
            st.error("❌ Criança com 5 anos ou mais!")
        elif not nome_completo:
            st.error("❌ Preencha o nome completo")
        else:
            data = {
                'nome_completo': nome_completo,
                'idade_meses': idade_meses,
                'data_nascimento': data_nascimento.strftime('%Y-%m-%d'),
                'provincia': provincia,
                'distrito': distrito,
                'residencia': residencia,
                'hospital': hospital,
                'nome_mae': nome_mae,
                'idade_mae': idade_mae,
                'escolaridade_mae': escolaridade_mae,
                'ocupacao_mae': ocupacao_mae,
                'agregado_familiar_mae': agregado_familiar_mae,
                'rendimento_familiar_mae': rendimento_familiar_mae,
                'peso': peso,
                'altura': altura,
                'muac': muac,
                'edema': edema,
                'perda_peso': perda_peso,
                'apatia': apatia,
                'febre': febre,
                'diarreia': diarreia,
                'doenca_cronica': doenca_cronica,
                'doenca_especificar': doenca_especificar,
                'cabelo': cabelo,
                'mucosa': mucosa,
                'suplementacao_ferro': suplementacao_ferro,
                'suplementacao_vit_a': suplementacao_vit_a,
                'desparasitacao': desparasitacao,
                'amamentacao': amamentacao,
                'meses_amamentacao': meses_amamentacao,
                'refeicoes_dia': refeicoes_dia,
                'dds_score': dds_score,
                'dds_calculado': dds_calculado,
                'producao_familiar': producao_familiar,
                'acesso_terra': acesso_terra,
                'culturas_produzidas': outras_culturas if culturas_produzidas == "Outra" else culturas_produzidas,
                'fonte_agua': fonte_agua,
                'dificuldades_producao': dificuldades,
                'data_registo': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            
            ia = st.session_state.ia_classifier
            risco_anemia, score_anemia, fatores_anemia, conf_anemia = ia.predict_anemia(data)
            risco_fome, score_fome, fatores_fome, conf_fome = ia.predict_fome_oculta(data)
            risco_inseg, score_inseg, fatores_inseg, conf_inseg = ia.predict_inseguranca(data)
            
            if SUPABASE_AVAILABLE:
                try:
                    sucesso, resultado = salvar_crianca_supabase(data)
                    if sucesso:
                        st.session_state.criancas.append(data)
                        st.success(f"✅ {nome_completo} registado no Supabase!")
                        if risco_anemia == "ALTO" or risco_fome == "ALTO" or risco_inseg == "ALTO":
                            st.markdown("""
                            <div style="background:#ffebee;border:3px solid #c62828;border-radius:15px;padding:20px;margin:10px 0;">
                                <h2 style="color:#c62828;text-align:center;">🚨 ALTO RISCO DETETADO!</h2>
                                <p style="color:#b71c1c;text-align:center;font-weight:bold;font-size:1.1rem;">✅ Gravado no Supabase e encaminhado ao médico!</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning(f"⚠️ Erro ao salvar: {resultado}")
                        st.session_state.criancas.append(data)
                        st.success(f"✅ {nome_completo} registado localmente!")
                except:
                    st.session_state.criancas.append(data)
                    st.success(f"✅ {nome_completo} registado localmente!")
            else:
                st.session_state.criancas.append(data)
                st.success(f"✅ {nome_completo} registado localmente!")
            
            st.markdown(f"<h2 style='text-align:center;color:#1B5E20;'>👶 {nome_completo}</h2>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                classe = "risk-high" if risco_anemia == "ALTO" else "risk-medium" if risco_anemia == "MEDIO" else "risk-low"
                st.markdown(f'<div style="background:{classe};padding:15px;border-radius:12px;margin:10px 0;"><h4>🩸 Anemia</h4><h2>{risco_anemia}</h2><p>Score: {score_anemia}/100</p></div>', unsafe_allow_html=True)
            with col2:
                classe = "risk-high" if risco_fome == "ALTO" else "risk-medium" if risco_fome == "MEDIO" else "risk-low"
                st.markdown(f'<div style="background:{classe};padding:15px;border-radius:12px;margin:10px 0;"><h4>🍽️ Fome Oculta</h4><h2>{risco_fome}</h2><p>Score: {score_fome}/100</p></div>', unsafe_allow_html=True)
            with col3:
                classe = "risk-high" if risco_inseg == "ALTO" else "risk-medium" if risco_inseg == "MEDIO" else "risk-low"
                st.markdown(f'<div style="background:{classe};padding:15px;border-radius:12px;margin:10px 0;"><h4>🏠 Insegurança Alimentar</h4><h2>{risco_inseg}</h2><p>Score: {score_inseg}/100</p></div>', unsafe_allow_html=True)
            
            st.subheader("📋 Fatores de Risco")
            if risco_anemia == "ALTO" or risco_fome == "ALTO" or risco_inseg == "ALTO":
                st.warning("⚠️ Fatores Críticos:")
                for f in fatores_anemia[:3]:
                    st.write(f"- {f}")
            else:
                st.success("✅ Nenhum fator crítico detetado.")
            
            st.subheader("💡 Recomendações")
            if risco_anemia == "ALTO":
                st.error("🔴 Encaminhar para médico para suplementação de ferro")
            elif risco_anemia == "MEDIO":
                st.warning("🟠 Reforçar consumo de alimentos ricos em ferro")
            else:
                st.success("🟢 Manter alimentação equilibrada")
            
            if st.button("🔄 Novo Caso", use_container_width=True):
                st.session_state.dados_basicos_salvos = False
                st.session_state.nome_salvo = ""
                st.session_state.data_salva = None
                st.session_state.idade_calculada = 0
                st.rerun()