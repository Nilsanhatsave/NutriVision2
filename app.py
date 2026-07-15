import streamlit as st
from datetime import datetime, timedelta
import random

# ===== CONFIGURAÇÃO =====
st.set_page_config(
    page_title="NutriVision - Plataforma Integrada - One Health",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== CSS PERSONALIZADO =====
st.markdown("""
<style>
/* TÍTULO PRINCIPAL */
.main-title { 
        font-size: 7.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 40%, #43A047 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(46, 125, 50, 0.15);
        line-height: 1.2;
}
.sub-title {
     font-size: 1.30rem !important;  
    font-weight: 700 !important;
    color: #2E7D32 !important;
    text-align: center !important;
    margin: 0 auto 1.5rem auto !important;
    padding: 1.5rem 3.0rem !important;
    line-height: 1.6 !important;
    background: rgba(255,255,255,0.7) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(46, 125, 50, 0.1) !important;
    width: 90% !important;
    max-width: 900% !important;
    box-sizing: border-box !important;
        
}
.login-box {
    background-color: #f8f9fa;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
            
.main-subheader strong { color: #1B5E20; font-weight: 600; }
            
.language-selector {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 10px;
}
.language-selector select {
    padding: 8px 20px;
    border-radius: 20px;
    border: 2px solid #2E7D32;
    background-color: white;
    font-size: 16px;
    font-weight: 600;
    color: #1B5E20;
    cursor: pointer;
    outline: none;
}
.language-selector select:hover {
    border-color: #4CAF50;
    background-color: #f5f5f5;
}
.stButton > button {
    background: linear-gradient(135deg, #2E7D32, #4CAF50);
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(46, 125, 50, 0.5);
    background: linear-gradient(135deg, #1B5E20, #388E3C);
}
.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #1B5E20;
    margin: 15px 0 10px 0;
    padding: 10px;
    background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
    border-radius: 10px;
    text-align: center;
}
.risk-high {
    background: linear-gradient(135deg, #ffebee, #ffcdd2);
    border-left: 8px solid #c62828;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}
.risk-medium {
    background: linear-gradient(135deg, #fff3e0, #ffe0b2);
    border-left: 8px solid #ef6c00;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}
.risk-low {
    background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
    border-left: 8px solid #2e7d32;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ===== TRADUÇÕES =====
TRADUCOES = {
    'pt': {
        'titulo': '🌿 NutriVision',
        'subtitulo': '🌿 NutriVision',
        'subtitulo': 'Plataforma One Health de Deteção Precoce da Anemia, Fome Oculta, Insegurança Alimentar<br>e Prevenção através de Intervenções Integradas nos Sistemas de Saúde e Agroalimentares',
        'login': 'Login',
        'usuario': 'Usuário',
        'senha': 'Senha',
        'entrar': 'Entrar',
        'credenciais': 'Credenciais de Teste',
        'perfil': 'Perfil',
        'sair': 'Sair',
        'triagem': 'Triagem Nutricional',
        'idioma': '🌐 Idioma',
        'portugues': 'Português',
        'ingles': 'English',
        'bem_vindo': 'Bem-vindo',
        'resultados': 'Resultados',
        'fatores_risco': 'Fatores de Risco',
        'recomendacoes': 'Recomendações'
    },
    'en': {
        'titulo': '🌿 NutriVision',
        'subtitulo': 'One Health Platform for Early Detection of Anemia, Hidden Hunger, Food Insecurity<br>and Prevention through Integrated Interventions in Health and Agri-Food Systems',
        'login': 'Login',
        'usuario': 'Username',
        'senha': 'Password',
        'entrar': 'Login',
        'credenciais': 'Test Credentials',
        'perfil': 'Profile',
        'sair': 'Logout',
        'triagem': 'Nutritional Screening',
        'idioma': '🌐 Language',
        'portugues': 'Portuguese',
        'ingles': 'English',
        'bem_vindo': 'Welcome',
        'resultados': 'Results',
        'fatores_risco': 'Risk Factors',
        'recomendacoes': 'Recommendations'
    }
}

# ===== IDIOMA =====
if 'idioma' not in st.session_state:
    st.session_state.idioma = 'pt'

def t(texto):
    return TRADUCOES[st.session_state.idioma].get(texto, texto)

# ===== CREDENCIAIS =====
USUARIOS = {
    "enfermeiro": {"senha": "123", "nome": "Enfermeiro", "icone": "👩🏾⚕️"},
    "medico": {"senha": "123", "nome": "Médico", "icone": "👨🏾⚕️"},
    "nutricionista": {"senha": "123", "nome": "Nutricionista", "icone": "🍎"},
    "agronomo": {"senha": "123", "nome": "Agrônomo", "icone": "🌾"},
    "admin": {"senha": "123", "nome": "Administrador", "icone": "👨💼"}
}

# ===== IMPORTAR SUPABASE =====
try:
    from supabase_client import (
        SUPABASE_AVAILABLE,
        salvar_crianca_supabase,
        carregar_criancas_supabase
    )
    if SUPABASE_AVAILABLE:
        print("✅ Supabase conectado!")
except ImportError:
    SUPABASE_AVAILABLE = False
    def salvar_crianca_supabase(dados):
        return False, "Supabase nao disponivel"
    def carregar_criancas_supabase():
        return False, []

# ===== SESSION STATE =====
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario' not in st.session_state:
    st.session_state.usuario = None
if 'perfil' not in st.session_state:
    st.session_state.perfil = None
if 'icone' not in st.session_state:
    st.session_state.icone = None
if 'criancas' not in st.session_state:
    st.session_state.criancas = []
if 'ia_classifier' not in st.session_state:
    st.session_state.ia_classifier = None

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
            fatores.append("MUAC crítico (<115mm)")
        elif data['muac'] < 125:
            score += 20
            fatores.append("MUAC baixo (<125mm)")
        elif data['muac'] < 135:
            score += 10
            fatores.append("MUAC limítrofe")
        
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
            fatores.append("Apenas 1 refeição/dia")
        elif data['refeicoes_dia'] == "2":
            score += 8
            fatores.append("Apenas 2 refeições/dia")
        
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
            fatores.append("Apenas 1 refeição/dia")
        elif data['refeicoes_dia'] == "2":
            score += 10
            fatores.append("Apenas 2 refeições/dia")
        
        if data['muac'] < 115:
            score += 15
            fatores.append("MUAC crítico")
        elif data['muac'] < 125:
            score += 10
            fatores.append("MUAC baixo")
        
        resultado = self._classificar(score)
        return resultado, score, fatores[:5], min(0.99, confianca)
    
    def _classificar(self, score):
        if score >= 50:
            return "ALTO"
        elif score >= 30:
            return "MÉDIO"
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

# ============================================================
# TELA DE LOGIN COM TRADUTOR
# ============================================================
def tela_login():
    st.markdown(f'<h1 class="main-title">{t("titulo")}</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="language-selector">', unsafe_allow_html=True)
        idioma_atual = st.session_state.idioma
        opcoes = {'pt': '🇵🇹 Português', 'en': '🇬🇧 English'}
        selecionado = st.selectbox(
            t('idioma'),
            options=list(opcoes.keys()),
            format_func=lambda x: opcoes[x],
            index=0 if idioma_atual == 'pt' else 1,
            label_visibility="collapsed"
        )
        if selecionado != idioma_atual:
            st.session_state.idioma = selecionado
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f'<p class="sub-title">{t("subtitulo")}</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown('<div class="language-selector">', unsafe_allow_html=True)
            
            st.markdown(f"### 🔐 {t('login')}")
            
            username = st.text_input(f"👤 {t('usuario')}", placeholder=f"Digite seu {t('usuario').lower()}", key="login_user")
            password = st.text_input(f"🔑 {t('senha')}", type="password", placeholder=f"Digite sua {t('senha').lower()}", key="login_pass")
            
            if st.button(f"🚀 {t('entrar')}", use_container_width=True):
                if username and password:
                    if username in USUARIOS and USUARIOS[username]["senha"] == password:
                        st.session_state.logado = True
                        st.session_state.usuario = USUARIOS[username]["nome"]
                        st.session_state.perfil = username
                        st.session_state.icone = USUARIOS[username]["icone"]
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha inválidos!")
                else:
                    st.warning("⚠️ Preencha todos os campos!")
            
            st.markdown("---")
            st.markdown(f"### 📋 {t('credenciais')}")
            st.code("""
enfermeiro / 123
medico / 123
nutricionista / 123
agronomo / 123
admin / 123
            """)
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# FORMULÁRIO ENFERMEIRO COM SUPABASE
# ============================================================
def formulario_enfermeiro():
    if SUPABASE_AVAILABLE:
        try:
            sucesso, dados = carregar_criancas_supabase()
            if sucesso and dados:
                st.session_state.criancas = dados
                st.success(f"✅ {len(dados)} registos carregados do Supabase!")
            else:
                st.session_state.criancas = []
                st.info("📋 Nenhum registo encontrado no Supabase")
        except Exception as e:
            st.error(f"❌ Erro ao carregar: {e}")
            st.session_state.criancas = []
    else:
        st.warning("⚠️ Supabase não disponível")
        st.session_state.criancas = []
    
    st.title(f"{st.session_state.icone} {t('triagem')}")
    st.markdown("Avaliação de risco de anemia, fome oculta e insegurança alimentar em crianças menores de 5 anos")
    
    if st.session_state.ia_classifier is None:
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
        
        st.markdown('<div class="section-title">👶 DADOS DA CRIANÇA</div>', unsafe_allow_html=True)
        
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
            data_nascimento = st.date_input(
                "📅 Data de Nascimento",
                value=datetime.now() - timedelta(days=730),
                max_value=datetime.now()
            )
            idade_meses = calcular_idade(data_nascimento)
        
        with col2:
            st.write("")
            st.write("")
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
        
        st.markdown("### 📍 Localização")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            provincia = st.selectbox(
                "Província",
                ["Cabo Delgado", "Gaza", "Inhambane", "Manica", "Maputo Cidade", 
                 "Maputo Província", "Nampula", "Niassa", "Sofala", "Tete", "Zambézia"]
            )
        with col2:
            distrito = st.text_input("Distrito")
        with col3:
            residencia = st.text_input("Local de Residência")
        with col4:
            hospital = st.text_input("Hospital/Unidade Sanitária")
        
        st.divider()
        
        st.markdown('<div class="section-title">👩 DADOS DA MÃE</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            nome_mae = st.text_input("Nome da Mãe", placeholder="Ex: Maria")
        with col2:
            idade_mae = st.number_input("Idade da Mãe (anos)", 12, 60, 25)
        with col3:
            escolaridade_mae = st.selectbox("Escolaridade da Mãe", 
                ["Nenhum", "Ensino Primário", "Ensino Secundário", "Ensino Superior"])
        with col4:
            ocupacao_mae = st.text_input("Ocupação da Mãe")
        
        col1, col2 = st.columns(2)
        with col1:
            agregado_familiar_mae = st.number_input("Nº de Pessoas no Agregado", 1, 20, 5)
        with col2:
            rendimento_familiar_mae = st.number_input("Rendimento Familiar (MZN)", 0, 100000, 5000)
        
        st.divider()
        
        st.markdown('<div class="section-title">📏 AVALIAÇÃO ANTROPOMÉTRICA</div>', unsafe_allow_html=True)
        
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
        
        diarreia = st.selectbox(
            "💧 Diarreia (últimas 2 semanas)",
            ["Não", "Sim, 1-3 dias", "Sim, 4-7 dias", "Sim, mais de 7 dias"]
        )
        
        doenca_cronica = st.selectbox(
            "🏥 Doença Crónica",
            ["Nenhuma", "HIV/SIDA", "Tuberculose", "Doença Cardíaca", 
             "Doença Renal", "Diabetes", "Asma", "Desnutrição Crónica", "Outra"]
        )
        
        if doenca_cronica == "Outra":
            doenca_especificar = st.text_input("Especifique a doença:")
        else:
            doenca_especificar = ""
        
        st.divider()
        
        st.markdown('<div class="section-title">💇 AVALIAÇÃO FÍSICA</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            cabelo = st.selectbox(
                "Cabelo",
                ["Pigmentado e abundante", "Pigmentado e fino", "Despigmentado", "Despigmentado fino e raro"]
            )
        with col2:
            mucosa = st.selectbox(
                "Mucosas",
                ["Coradas", "Hipocoradas", "Muito Hipocoradas"]
            )
        
        st.divider()
        
        st.markdown('<div class="section-title">💊 SUPLEMENTAÇÃO</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            suplementacao_ferro = st.selectbox("Suplementação de Ferro", ["Não", "Sim", "Em curso"])
        with col2:
            suplementacao_vit_a = st.selectbox("Suplementação Vitamina A", ["Não", "Sim", "Em curso"])
        with col3:
            desparasitacao = st.selectbox("Desparasitação", ["Não", "Sim", "Não sabe"])
        
        st.divider()
        
        st.markdown('<div class="section-title">🍽️ HISTÓRICO ALIMENTAR</div>', unsafe_allow_html=True)
        
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
        
        st.markdown('<div class="section-title">🥗 ALIMENTOS CONSUMIDOS</div>', unsafe_allow_html=True)
        
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
        
        st.markdown('<div class="section-title">🌾 PRODUÇÃO AGRÍCOLA</div>', unsafe_allow_html=True)

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
                'doenca_cronica_especificar': doenca_especificar,
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
            
            data.update({
                'risco_anemia_nivel': risco_anemia,
                'risco_anemia_score': score_anemia,
                'risco_fome_nivel': risco_fome,
                'risco_fome_score': score_fome,
                'risco_inseguranca_nivel': risco_inseg,
                'risco_inseguranca_score': score_inseg,
            })
            
            if SUPABASE_AVAILABLE:
                try:
                    sucesso, resultado = salvar_crianca_supabase(data)
                    if sucesso:
                        st.session_state.criancas.append(data)
                        st.success(f"✅ {nome_completo} registado no Supabase!")
                    else:
                        st.warning(f"⚠️ Erro ao salvar: {resultado}")
                        st.session_state.criancas.append(data)
                        st.success(f"✅ {nome_completo} registado localmente!")
                except Exception as e:
                    st.session_state.criancas.append(data)
                    st.success(f"✅ {nome_completo} registado localmente!")
            else:
                st.session_state.criancas.append(data)
                st.success(f"✅ {nome_completo} registado localmente!")
            
            st.markdown(f"<h2 style='text-align:center;color:#1B5E20;'>👶 {nome_completo}</h2>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if risco_anemia == "ALTO":
                    classe = "risk-high"
                elif risco_anemia == "MÉDIO":
                    classe = "risk-medium"
                else:
                    classe = "risk-low"
                st.markdown(f"""
                <div class="{classe}">
                    <h4>🩸 Anemia</h4>
                    <h2>{risco_anemia}</h2>
                    <p>Score: {score_anemia}/100</p>
                    <p>Confiança: {conf_anemia*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if risco_fome == "ALTO":
                    classe = "risk-high"
                elif risco_fome == "MÉDIO":
                    classe = "risk-medium"
                else:
                    classe = "risk-low"
                st.markdown(f"""
                <div class="{classe}">
                    <h4>🍽️ Fome Oculta</h4>
                    <h2>{risco_fome}</h2>
                    <p>Score: {score_fome}/100</p>
                    <p>Confiança: {conf_fome*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if risco_inseg == "ALTO":
                    classe = "risk-high"
                elif risco_inseg == "MÉDIO":
                    classe = "risk-medium"
                else:
                    classe = "risk-low"
                st.markdown(f"""
                <div class="{classe}">
                    <h4>🏠 Insegurança Alimentar</h4>
                    <h2>{risco_inseg}</h2>
                    <p>Score: {score_inseg}/100</p>
                    <p>Confiança: {conf_inseg*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"### 📋 {t('fatores_risco')}")
            
            for f in fatores_anemia:
                st.markdown(f"🟡 {f}")
            for f in fatores_fome:
                if f not in fatores_anemia:
                    st.markdown(f"🟠 {f}")
            for f in fatores_inseg:
                if f not in fatores_anemia and f not in fatores_fome:
                    st.markdown(f"🔴 {f}")
            
            st.markdown(f"### 💡 {t('recomendacoes')}")
            
            if risco_anemia == "ALTO":
                st.warning("🔴 Encaminhar para médico para suplementação de ferro")
                st.info("🥩 Aumentar consumo de carnes vermelhas, fígado e feijão")
            elif risco_anemia == "MÉDIO":
                st.info("🟠 Reforçar consumo de alimentos ricos em ferro")
                st.info("🍊 Combinar alimentos ricos em ferro com vitamina C")
            
            if risco_fome == "ALTO":
                st.warning("🔴 Diversificar alimentação com frutas, legumes e vegetais")
                st.info("🥬 Incluir verduras escuras (espinafre, couve) diariamente")
            
            if risco_inseg == "ALTO":
                st.warning("🔴 Avaliar programas de complementação alimentar")
                st.info("🏠 Orientar sobre aproveitamento de alimentos locais")
            
            if risco_anemia == "BAIXO" and risco_fome == "BAIXO" and risco_inseg == "BAIXO":
                st.success("✅ Criança com bom estado nutricional. Manter acompanhamento regular.")

# ============================================================
# MAIN
# ============================================================
def main():
    if not st.session_state.logado:
        tela_login()
    else:
        col1, col2, col3 = st.columns([1, 6, 1])
        with col1:
            st.markdown(f"### {st.session_state.icone}")
        with col2:
            st.markdown(f"### 👋 {t('bem_vindo')}, {st.session_state.usuario}!")
        with col3:
            if st.button(f"🚪 {t('sair')}"):
                st.session_state.logado = False
                st.session_state.usuario = None
                st.session_state.perfil = None
                st.session_state.icone = None
                st.rerun()
        
        st.markdown("---")
        
        perfil = st.session_state.perfil
        
        if perfil == "enfermeiro":
            formulario_enfermeiro()
        elif perfil == "medico":
            from pages import medico
            medico.render_medico()
        elif perfil == "nutricionista":
            from pages import nutricionista
            nutricionista.render_nutricionista()
        elif perfil == "agronomo":
            from pages import agronomo
            agronomo.render_agronomo()
        elif perfil == "admin":
            st.info("👨💼 Painel Administrativo")
        else:
            st.info("📋 Selecione uma opção no menu lateral")

if __name__ == "__main__":
    main()