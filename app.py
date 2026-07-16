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
.main-title { 
    font-size: 5.5rem !important;
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
    font-size: 1.1rem !important;  
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
    max-width: 900px !important;
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
        'medico_titulo': 'Médico - Avaliação Clínica',
        'gestao_pacientes': '👤 Gestão de Pacientes',
        'nenhum_paciente': '📋 Nenhum paciente registado no sistema.',
        'dados_crianca': '👶 DADOS DA CRIANÇA',
        'primeiro_nome': 'Primeiro Nome',
        'nome_meio': 'Nome do Meio',
        'apelido': 'Apelido',
        'data_nascimento': '📅 Data de Nascimento',
        'salvar_dados': '💾 Salvar Dados',
        # ===== TÍTULOS E MENUS =====
        'titulo': '🌿 NutriVision',
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
        'recomendacoes': 'Recomendações',
        
        # ===== PERFIS =====
        'medico_titulo': 'Médico - Avaliação Clínica',
        'nutricionista_titulo': 'Nutricionista - Avaliação Nutricional',
        'agronomo_titulo': 'Agrônomo - Intervenção Agroalimentar',
        'enfermeiro_titulo': 'Enfermeiro - Triagem Nutricional',
        'admin_titulo': 'Administrador - Painel de Controlo',
        
        # ===== ABAS =====
        'avaliacao': '📋 Avaliação',
        'dashboard': '📊 Dashboard',
        'historico': '📜 Histórico',
        'encaminhamentos': '📨 Encaminhamentos',
        'pacientes': 'Pacientes',
        'gestao_pacientes': '👤 Gestão de Pacientes',
        'selecionar_paciente': '👤 Selecionar Paciente para Avaliação',
        'dados_paciente': '📊 Dados do Paciente',
        'avaliacao_risco': '🩺 Avaliação de Risco',
        'decisao_clinica': '📝 Decisão Clínica',
        'gerar_relatorio': '📄 Gerar Relatório',
        
        # ===== CAMPOS DO FORMULÁRIO =====
        'prescricao': '💊 Prescrição',
        'diagnostico': '📋 Diagnóstico',
        'seguimento': '📅 Plano de Seguimento',
        'observacoes': '📋 Observações',
        'salvar': '💾 Salvar',
        'cancelar': '🔒 Cancelar',
        'editar': '✏️ Editar',
        'fechar': '🔒 Fechar Caso',
        'atualizar': '🔄 Atualizar',
        'recarregar': '🔄 Recarregar Pacientes',
        'nova_decisao': '🧹 Nova Decisão',
        
        # ===== BOTÕES =====
        'btn_salvar': '💾 Salvar Decisão',
        'btn_encaminhar': '📨 Encaminhar',
        'btn_pdf': '📄 Gerar PDF com QR Code',
        'btn_editar': '✏️ Editar',
        'btn_fechar': '🔒 Fechar Caso',
        'btn_cancelar': '🔒 Cancelar e Voltar',
        'btn_atualizar_dados': '💾 Atualizar Dados Clínicos',
        
        # ===== TABELAS =====
        'nome': 'Nome',
        'idade': 'Idade (meses)',
        'peso': 'Peso (kg)',
        'altura': 'Altura (cm)',
        'muac': 'MUAC (mm)',
        'dds': 'DDS',
        'hemoglobina': 'Hemoglobina',
        'tipo_anemia': 'Tipo de Anemia',
        'risco_anemia': 'Risco de Anemia',
        'risco_fome': 'Fome Oculta',
        'risco_inseguranca': 'Insegurança Alimentar',
        'provincia': 'Província',
        'distrito': 'Distrito',
        'residencia': 'Residência',
        'hospital': 'Hospital',
        'data_registo': 'Data de Registo',
        'data': 'Data',
        'status': 'Status',
        'urgencia': 'Urgência',
        'especialidade': 'Especialidade',
        'motivo': 'Motivo',
        'medico_responsavel': 'Médico Responsável',
        
        # ===== MENSAGENS =====
        'nenhum_paciente': '📋 Nenhum paciente registado no sistema.',
        'nenhum_registo': '📋 Nenhum registo encontrado.',
        'nenhum_encaminhamento': '📋 Nenhum encaminhamento registado ainda.',
        'carregando': '⏳ Carregando...',
        'erro_carregar': '❌ Erro ao carregar:',
        'sucesso_salvar': '✅ Dados salvos com sucesso!',
        'erro_salvar': '❌ Erro ao salvar:',
        'confirmar_exclusao': '⚠️ Tem certeza que deseja excluir?',
        
        # ===== ENCAMINHAMENTOS =====
        'encaminhamento_integrado': '📨 Encaminhamento Integrado',
        'encaminhamento_texto': 'O paciente será encaminhado simultaneamente para <strong>Nutricionista</strong> e <strong>Agrônomo</strong>.',
        'urgencia_normal': 'Normal',
        'urgencia_urgente': 'Urgente',
        'urgencia_muito_urgente': 'Muito Urgente',
        'alta_urgencia': '🔴 ALTA URGÊNCIA!',
        'urgencia_texto': '🟠 URGENTE!',
        'encaminhado_sucesso': '✅ {paciente} encaminhado para Nutricionista e Agrônomo!',
        'encaminhamento_existente': '⚠️ {paciente} já possui encaminhamento ativo!',
        
        # ===== FILTROS =====
        'filtrar_risco': 'Filtrar por Risco de Anemia',
        'filtrar_provincia': 'Filtrar por Província',
        'todas': 'Todas',
        'todos': 'Todos',
        'pendente': 'Pendente',
        'em_andamento': 'Em andamento',
        'concluido': 'Concluído',
        'data_inicio': 'Data de Início',
        'data_fim': 'Data de Fim',
        
        # ===== GRÁFICOS =====
        'distribuicao_risco': 'Distribuição de Risco de Anemia',
        'distribuicao_fome': 'Distribuição de Fome Oculta',
        'distribuicao_inseguranca': 'Distribuição de Insegurança Alimentar',
        'distribuicao_tipo_anemia': 'Distribuição - Tipo de Anemia',
        'distribuicao_dds': 'Distribuição - Diversidade Alimentar (DDS)',
        'lista_pacientes': '📋 Lista de Pacientes',
        
        # ===== STATUS =====
        'alto': 'ALTO',
        'medio': 'MÉDIO',
        'baixo': 'BAIXO',
        'sim': 'Sim',
        'nao': 'Não',
        'presente': 'Presente',
        'ausente': 'Ausente',
        
        # ===== RELATÓRIO PDF =====
        'relatorio_clinico': 'RELATÓRIO CLÍNICO',
        'dados_clinicos': 'DADOS CLÍNICOS',
        'assinatura_medico': 'ASSINATURA DO MÉDICO',
        'validade': 'Validade',
        'codigo': 'Código',
        'escanear_qr': 'ESCANEIE O QR CODE',
        'validar_autenticidade': 'Para validar a autenticidade do relatório',
        'documento_validado': 'Documento validado digitalmente',
        
        # ===== PRODUÇÃO AGRÍCOLA =====
        'producao_familiar': 'Produção Familiar',
        'acesso_terra': 'Acesso à Terra',
        'fonte_agua': 'Fonte de Água',
        'culturas_produzidas': 'Culturas Produzidas',
        'dificuldades_producao': 'Dificuldades na Produção',
        'produz_consumo': 'Produz para consumo',
        'produz_venda': 'Produz para venda',
        'produz_consumo_venda': 'Produz para consumo e venda',
        'nao_produz': 'Não produz',
        'terra_propria': 'Tem terra própria',
        'terra_comunitaria': 'Tem terra comunitária',
        'terra_arrendada': 'Tem terra arrendada',
        'nao_tem_terra': 'Não tem terra',
         # ===== ENFERMEIRO =====
        'registos_carregados': 'registos carregados do Supabase!',
        'supabase_indisponivel': '⚠️ Supabase não disponível',
        'descricao_triagem': 'Avaliação de risco de anemia, fome oculta e insegurança alimentar em crianças menores de 5 anos',
        'dados_crianca': '👶 DADOS DA CRIANÇA',
        'primeiro_nome': 'Primeiro Nome',
        'nome_meio': 'Nome do Meio',
        'apelido': 'Apelido',
        'ex_joao': 'Ex: João',
        'ex_manuel': 'Ex: Manuel',
        'ex_silva': 'Ex: Silva',
        'data_nascimento': '📅 Data de Nascimento',
        'salvar_dados': '💾 Salvar Dados',
        'preencher_nome': '⚠️ Preencha o nome completo',
        'clicar_salvar_dados': '⚠️ Clique em \'Salvar Dados\' para continuar.',
        'meses': 'meses',
        'localizacao': '📍 Localização',
        'dados_mae': '👩 DADOS DA MÃE',
        'nome_mae': 'Nome da Mãe',
        'ex_maria': 'Ex: Maria',
        'idade_mae': 'Idade da Mãe (anos)',
        'escolaridade_mae': 'Escolaridade da Mãe',
        'ensino_primario': 'Ensino Primário',
        'ensino_secundario': 'Ensino Secundário',
        'ensino_superior': 'Ensino Superior',
        'ocupacao_mae': 'Ocupação da Mãe',
        'agregado_familiar': 'Nº de Pessoas no Agregado',
        'rendimento_familiar': 'Rendimento Familiar (MZN)',
        'avaliacao_antropometrica': '📏 AVALIAÇÃO ANTROPOMÉTRICA',
        'peso_kg': 'Peso (kg)',
        'altura_cm': 'Altura (cm)',
        'muac_mm': 'MUAC (mm)',
        'edema': 'Edema',
        'ausente': 'Ausente',
        'presente': 'Presente',
        'perda_peso': 'Perda de peso',
        'nao': 'Não',
        'sim': 'Sim',
        'apatia': 'Apatia',
        'febre': 'Febre',
        'diarreia': '💧 Diarreia (últimas 2 semanas)',
        'sim_1_3_dias': 'Sim, 1-3 dias',
        'sim_4_7_dias': 'Sim, 4-7 dias',
        'sim_mais_7_dias': 'Sim, mais de 7 dias',
        'doenca_cronica': '🏥 Doença Crónica',
        'nenhuma': 'Nenhuma',
        'doenca_cardiaca': 'Doença Cardíaca',
        'doenca_renal': 'Doença Renal',
        'desnutricao_cronica': 'Desnutrição Crónica',
        'outra': 'Outra',
        'especificar_doenca': 'Especifique a doença:',
        'avaliacao_fisica': '💇 AVALIAÇÃO FÍSICA',
        'cabelo': 'Cabelo',
        'pigmentado_abundante': 'Pigmentado e abundante',
        'pigmentado_fino': 'Pigmentado e fino',
        'despigmentado': 'Despigmentado',
        'despigmentado_fino_raro': 'Despigmentado fino e raro',
        'mucosas': 'Mucosas',
        'coradas': 'Coradas',
        'hipocoradas': 'Hipocoradas',
        'muito_hipocoradas': 'Muito Hipocoradas',
        'suplementacao': '💊 SUPLEMENTAÇÃO',
        'suplementacao_ferro': 'Suplementação de Ferro',
        'suplementacao_vit_a': 'Suplementação Vitamina A',
        'em_curso': 'Em curso',
        'desparasitacao': 'Desparasitação',
        'nao_sabe': 'Não sabe',
        'historico_alimentar': '🍽️ HISTÓRICO ALIMENTAR',
        'amamentacao': 'Amamentação',
        'meses_amamentacao': 'Meses amamentação exclusiva',
        'amamentacao_desativada': '🚫 Amamentação desativada (>24 meses)',
        'refeicoes_dia': 'Refeições por dia',
        'diversidade_alimentar': 'Diversidade Alimentar (DDS)',
        'alimentos_consumidos': '🥗 ALIMENTOS CONSUMIDOS',
        'frutas': 'Frutas',
        'carnes': 'Carnes',
        'carne_bovina': 'Carne bovina',
        'carne_frango': 'Carne de frango',
        'carne_cabra': 'Carne de cabra',
        'peixe': 'Peixe',
        'peixe_fresco': 'Peixe fresco',
        'peixe_seco': 'Peixe seco',
        'ovos': 'Ovos',
        'ovo_galinha': 'Ovo de galinha',
        'leguminosas': 'Leguminosas',
        'cereais': 'Cereais',
        'verduras': 'Verduras',
        'producao_agricola': '🌾 PRODUÇÃO AGRÍCOLA',
        'produz_consumo': 'Produz para consumo',
        'produz_venda': 'Produz para venda',
        'produz_consumo_venda': 'Produz para consumo e venda',
        'nao_produz': 'Não produz',
        'terra_propria': 'Tem terra própria',
        'terra_comunitaria': 'Tem terra comunitária',
        'terra_arrendada': 'Tem terra arrendada',
        'nao_tem_terra': 'Não tem terra',
        'culturas_produzidas': '3. Principais culturas produzidas:',
        'especificar_culturas': 'Especifique outras culturas:',
        'fonte_agua': '4. Fonte de água para produção:',
        'agua_chuva': 'Água da chuva',
        'sistema_irrigacao': 'Sistema de irrigação',
        'nenhuma': 'Nenhuma',
        'dificuldades_producao': '5. Principais dificuldades na produção:',
        'falta_sementes': 'Falta de sementes',
        'falta_fertilizantes': 'Falta de fertilizantes/adubo',
        'solo_pouco_fertil': 'Solo pouco fértil',
        'pragas_doencas': 'Pragas e doenças',
        'falta_chuva_seca': 'Falta de chuva/seca',
        'cheias_excesso_chuva': 'Cheias/excesso de chuva',
        'falta_conhecimento_tecnico': 'Falta de conhecimento técnico',
        'falta_mao_obra': 'Falta de mão de obra',
        'falta_equipamento_agricola': 'Falta de equipamento agrícola',
        'nenhuma_dificuldade': 'Nenhuma dificuldade',
        'calcular_risco': '🧮 Calcular Risco',
        'crianca_5_anos': '❌ Criança com 5 anos ou mais!',
        'registado_supabase': 'registado no Supabase!',
        'registado_local': 'registado localmente!',
        'erro_salvar': '⚠️ Erro ao salvar:',
        'anemia': 'Anemia',
        'fome_oculta': 'Fome Oculta',
        'inseguranca_alimentar': 'Insegurança Alimentar',
        'score': 'Score',
        'confianca': 'Confiança',
        'alto': 'ALTO',
        'medio': 'MÉDIO',
        'baixo': 'BAIXO',
        'recomendacao_anemia_alto': 'Encaminhar para médico para suplementação de ferro',
        'recomendacao_anemia_alto_2': 'Aumentar consumo de carnes vermelhas, fígado e feijão',
        'recomendacao_anemia_medio': 'Reforçar consumo de alimentos ricos em ferro',
        'recomendacao_anemia_medio_2': 'Combinar alimentos ricos em ferro com vitamina C',
        'recomendacao_fome_alto': 'Diversificar alimentação com frutas, legumes e vegetais',
        'recomendacao_fome_alto_2': 'Incluir verduras escuras (espinafre, couve) diariamente',
        'recomendacao_inseg_alto': 'Avaliar programas de complementação alimentar',
        'recomendacao_inseg_alto_2': 'Orientar sobre aproveitamento de alimentos locais',
        'recomendacao_ok': 'Criança com bom estado nutricional. Manter acompanhamento regular.',
        'recomendacao_ok_2': 'Incentivar consumo de alimentos variados e nutritivos.',
        'nutricionista_titulo': 'Nutricionista - Avaliação Nutricional',
        'descricao_nutricionista': 'Avaliação nutricional, acompanhamento e recomendações para pacientes.',
        'anemia_alta': 'Anemia ALTA',
        'fome_oculta_alta': 'Fome Oculta ALTA',
        'inseguranca_alta': 'Insegurança ALTA',
        'pacientes_anemia_alta': 'pacientes com ALTO risco de anemia',
        'pacientes_anemia_media': 'pacientes com MÉDIO risco de anemia',
        'pacientes_fome_alta': 'pacientes com ALTA fome oculta',
        'pacientes_inseguranca_alta': 'pacientes com ALTA insegurança alimentar',
        'todos_baixo_risco': 'Todos os pacientes estão com BAIXO risco. Manter acompanhamento preventivo.',
        'recomendacao_anemia_alta': 'Priorizar suplementação de ferro e alimentação rica em ferro.',
        'recomendacao_anemia_media': 'Reforçar orientação nutricional e monitoramento.',
        'recomendacao_fome_alta': 'Diversificar alimentação com frutas, legumes e vegetais.',
        'recomendacao_inseguranca_alta': 'Avaliar programas de complementação alimentar.',
        'orientacoes_familia': 'Orientações para a Família',
        'dica_1': 'Alimentação variada com 5 grupos alimentares por dia',
        'dica_2': 'Incluir alimentos ricos em ferro (carnes, feijão, espinafre)',
        'dica_3': 'Consumir frutas e verduras coloridas diariamente',
        'dica_4': 'Evitar consumo excessivo de açúcares e gorduras',
        'dica_5': 'Beber água potável e manter boas práticas de higiene',
                # ===== NUTRICIONISTA - TRADUÇÕES =====
        # ============================================================
        'nutricionista_titulo': 'Nutricionista - Avaliação Nutricional',
        'descricao_nutricionista': 'Avaliação nutricional, acompanhamento e recomendações para pacientes.',
        'anemia_alta': 'Anemia ALTA',
        'fome_oculta_alta': 'Fome Oculta ALTA',
        'inseguranca_alta': 'Insegurança ALTA',
        'pacientes_anemia_alta': 'pacientes com ALTO risco de anemia',
        'pacientes_anemia_media': 'pacientes com MÉDIO risco de anemia',
        'pacientes_fome_alta': 'pacientes com ALTA fome oculta',
        'pacientes_inseguranca_alta': 'pacientes com ALTA insegurança alimentar',
        'todos_baixo_risco': 'Todos os pacientes estão com BAIXO risco. Manter acompanhamento preventivo.',
        'recomendacao_anemia_alta': 'Priorizar suplementação de ferro e alimentação rica em ferro.',
        'recomendacao_anemia_media': 'Reforçar orientação nutricional e monitoramento.',
        'recomendacao_fome_alta': 'Diversificar alimentação com frutas, legumes e vegetais.',
        'recomendacao_inseguranca_alta': 'Avaliar programas de complementação alimentar.',
        'orientacoes_familia': '📋 Orientações para a Família',
        'dica_1': 'Alimentação variada com 5 grupos alimentares por dia',
        'dica_2': 'Incluir alimentos ricos em ferro (carnes, feijão, espinafre)',
        'dica_3': 'Consumir frutas e verduras coloridas diariamente',
        'dica_4': 'Evitar consumo excessivo de açúcares e gorduras',
        'dica_5': 'Beber água potável e manter boas práticas de higiene',
        'avaliacao_nutricional': '🥗 Avaliação Nutricional',
        'diversidade_alimentar_dds': '📊 Diversidade Alimentar (DDS)',
        'dds_slider': 'DDS (Diversidade Alimentar)',
        'frequencia_refeicoes': '🍽️ Frequência de Refeições',
        'refeicoes_por_dia': 'Refeições por dia',
        'consumo_proteina': '🥩 Consumo de Proteína',
        'fonte_proteina': 'Fonte de proteína',
        'consumo_vitamina_c': '🍊 Consumo de Vitamina C',
        'fonte_vitamina_c': 'Fonte de vitamina C',
        'observacoes_nutricionais': '🥬 Observações Nutricionais',
        'observacoes_placeholder': 'Notas sobre a avaliação nutricional...',
        'salvar_avaliacao': '💾 Salvar Avaliação',
        'avaliacao_salva': 'Avaliação nutricional salva para',
        'plano_alimentar': '📝 Plano Alimentar',
        'frequencia_refeicoes_recomendada': '🍽️ Frequência de refeições recomendada',
        'proteinas_recomendadas': '🥩 Proteínas recomendadas',
        'frutas_verduras_recomendadas': '🍎 Frutas e verduras recomendadas',
        'observacoes_plano': '📋 Observações do Plano',
        'observacoes_plano_placeholder': 'Notas sobre o plano alimentar...',
        'registar_plano': '💾 Registar Plano',
        'plano_registado': 'Plano alimentar registado para',
        'selecionar_alimentos': '⚠️ Selecione pelo menos uma proteína ou fruta/verdura.',
        'plano_intervencao': '📝 Plano de Intervenção Nutricional',
        'objetivos_intervencao': '🎯 Objetivos da Intervenção',
        'objetivo_principal': '📋 Objetivo Principal',
        'objetivo_principal_placeholder': 'Descreva o objetivo principal da intervenção...',
        'metas_especificas': '📊 Metas Específicas',
        'metas_placeholder': 'Liste as metas a serem alcançadas...',
        'prazo_execucao': '⏱️ Prazo de Execução',
        'data_inicio': '📅 Data de Início',
        'intervencoes_nutricionais': '🍽️ Intervenções Nutricionais',
        'recomendacoes_dieteticas': '🥗 Recomendações Dietéticas',
        'recomendacoes_placeholder': 'Descreva as recomendações dietéticas...',
        'suplementacao_recomendada': '💊 Suplementação Recomendada',
        'suplementacao_placeholder': 'Descreva a suplementação recomendada...',
        'atividades_educativas': '📋 Atividades Educativas',
        'atividades_placeholder': 'Descreva as atividades educativas planeadas...',
        'envolvimento_familiar': '👨‍👩‍👧‍👦 Envolvimento Familiar',
        'envolvimento_placeholder': 'Descreva como a família será envolvida...',
        'monitoramento_avaliacao': '📊 Monitoramento e Avaliação',
        'frequencia_monitoramento': '📅 Frequência de Monitoramento',
        'indicadores_avaliacao': '📋 Indicadores de Avaliação',
        'indicadores_placeholder': 'Descreva os indicadores a serem avaliados...',
        'observacoes_finais': '📝 Observações Finais',
        'observacoes_plano_placeholder': 'Observações adicionais sobre o plano...',
        'planos_registados': '📋 Planos Registados',
        'plano': 'Plano',
        'marcar_concluido': '✅ Marcar como Concluído',
        'remover': '🗑️ Remover',
        'nenhum_plano_registado': '📋 Nenhum plano registado para este paciente.',
        'preencher_objetivo_recomendacoes': '⚠️ Preencha o objetivo principal ou as recomendações dietéticas.',
        'lista_pendentes': '📋 Lista de Pendentes',
        'lista_atendidos': '📋 Lista de Atendidos',
        'todos_atendidos': '✅ Todos os encaminhamentos foram atendidos!',
        'encaminhamentos_recebidos': '📨 Encaminhamentos Recebidos',
        'nenhum_encaminhamento_nutricionista': '📋 Nenhum encaminhamento para nutricionista recebido ainda.',
        'recomendacoes_nutricionais': '💡 Recomendações Nutricionais',
        'analise_nutricional': '📊 Análise Nutricional',
                # ===== AGRÔNOMO - TRADUÇÕES =====
        # ============================================================
        'agronomo_titulo': 'Agrônomo - Intervenção Agroalimentar',
        'descricao_agronomo': 'Avaliação agroalimentar, resiliência climática e recomendações para famílias encaminhadas pelo médico.',
        'total_pacientes': 'Total Pacientes',
        'encaminhamentos': 'Encaminhamentos',
        'pendentes': 'Pendentes',
        'atendidos': 'Atendidos',
        'selecionar_paciente': '👤 Selecionar Paciente',
        'dados_paciente': '📊 Dados do Paciente',
        'nome': 'Nome',
        'idade': 'Idade (meses)',
        'peso': 'Peso (kg)',
        'altura': 'Altura (cm)',
        'muac': 'MUAC (mm)',
        'dds': 'DDS',
        'provincia': 'Província',
        'distrito': 'Distrito',
        'risco': '🩺 Risco',
        'risco_anemia': 'Risco de Anemia',
        'risco_fome': 'Fome Oculta',
        'risco_inseguranca': 'Insegurança Alimentar',
        'producao_familiar': '🌾 Produção Familiar',
        'acesso_terra': '🏠 Acesso à Terra',
        'fonte_agua': '💧 Fonte de Água',
        'culturas_produzidas': '🌱 Culturas Produzidas',
        'dificuldades_producao': '🌾 Dificuldades na Produção',
        'nenhuma_dificuldade': 'Nenhuma dificuldade registada',
        'avaliacao_resiliencia': '🌾 Avaliação de Resiliência Agroalimentar',
        'descricao_resiliencia': 'Preencha o formulário para avaliar a resiliência climática e produtiva da família.',
        'pergunta_disponibilidade_agua': 'Qual é a disponibilidade de água para a produção agrícola?',
        'pergunta_exposicao_climatica': 'Como classifica a exposição da exploração agrícola a eventos climáticos nos últimos 5 anos?',
        'pergunta_estado_solo': 'Qual é o estado atual do solo e as práticas de conservação?',
        'pergunta_sistema_producao': 'Como caracteriza o sistema de produção agrícola?',
        'pergunta_capacidade_adaptativa': 'Qual é o nível de capacidade adaptativa da família agrícola?',
        'pergunta_impacto_producao': 'Qual foi o impacto da produção agrícola na segurança alimentar da família nos últimos 12 meses?',
        'selecione_opcao': 'Selecione a opção:',
        'legenda_calcular_indices': 'Após preencher todas as perguntas, clique em "Calcular Índices" para obter os resultados.',
        'calcular_indices': '📊 Calcular Índices',
        'indices_calculados': 'Índices calculados com sucesso!',
        'resultados_indices': '📊 Resultados dos Índices',
        'recomendacoes': '💡 Recomendações',
        'registar_intervencao': '📝 Registar Intervenção',
        'recomendacoes_tecnicas': '🌾 Recomendações Técnicas',
        'culturas_recomendadas': '🌱 Culturas Recomendadas',
        'praticas_recomendadas': '🔄 Práticas Agrícolas Recomendadas',
        'observacoes': '📋 Observações',
        'registar': '💾 Registar',
        'intervencao_registada': 'Intervenção registada com sucesso!',
        'preencher_recomendacoes': '⚠️ Preencha as recomendações técnicas.',
        'analise_agroalimentar': '📊 Análise Agroalimentar',
        'dados_encaminhamento': '📋 Dados do Encaminhamento',
        'especialidade': 'Especialidade',
        'urgencia': 'Urgência',
        'motivo': 'Motivo',
        'status': 'Status',
        'medico_responsavel': 'Médico Responsável',
        'dados_agroalimentares': '📊 Dados Agroalimentares',
        'marcar_atendido': '✅ Marcar como Atendido',
        'nenhum_encaminhamento_agronomo': '📋 Nenhum encaminhamento para agrônomo recebido ainda.',
        'distribuicao': 'Distribuição',
        'principais_culturas': '🌱 Principais Culturas Produzidas',
        'carregados': 'carregados',
        'supabase_indisponivel': '⚠️ Supabase não disponível',
        'nenhum_paciente': '📋 Nenhum paciente registado no sistema.',
        'nenhum_registo': '📋 Nenhum registo encontrado.',
        'casos_aguardam_avaliacao': 'casos aguardam avaliação médica',
        'recarregar': '🔄 Recarregar',
        'atualizar_dados_clinicos': '🩺 Atualizar Dados Clínicos',
        'atualizar_dados_caption': 'Atualize os dados clínicos se necessário. Deixe em branco para manter os valores atuais.',
        'selecione_tipo': 'Selecione o tipo:',
        'selecione_resultado': 'Selecione o resultado:',
        'ultimas_2_semanas': 'últimas 2 semanas',
        'doenca_cronica': '🏥 Doença Crónica',
        'doenca_cronica_conhecida': 'Doença Crónica conhecida:',
        'especificar_doenca': '📋 Especificar Doença',
        'especificar_doenca_texto': 'Especifique a doença crónica (se aplicável):',
        'btn_atualizar_dados': '💾 Atualizar Dados Clínicos',
        'dados_atualizados': 'Dados clínicos de',
        'dados_atualizados_local': 'Dados clínicos de',
        'erro_atualizar': '❌ Erro ao atualizar',
        'nenhum_dado_alterado': '⚠️ Nenhum dado foi alterado',
        'selecionar_paciente_valido': '❌ Selecione um paciente válido',
        'nova_decisao_clinica': '📝 Nova Decisão Clínica',
        'preencher_campos_decisao': 'Preencha os campos abaixo para registrar uma nova decisão clínica para este paciente.',
        'prescricao': '💊 Prescrição',
        'diagnostico': '📋 Diagnóstico',
        'seguimento': '📅 Plano de Seguimento',
        'notas_caso': 'Notas sobre o caso...',
        'btn_salvar': '💾 Salvar Decisão',
        'decisao_registada': 'Decisão de',
        'no_supabase': 'registada no Supabase!',
        'decisao_local_erro': 'Decisão salva localmente. Erro:',
        'localmente': 'registada localmente!',
        'preencher_diagnostico_prescricao': '⚠️ Preencha diagnóstico ou prescrição',
        'btn_nova_decisao': '🧹 Nova Decisão',
        'clicar_limpar_campos': 'Clique para limpar os campos e adicionar uma nova decisão',
        'encaminhamento_integrado': '📨 Encaminhamento Integrado',
        'encaminhamento_texto': 'O paciente será encaminhado simultaneamente para <strong>Nutricionista</strong> e <strong>Agrônomo</strong>.',
        'encaminhamento_info': 'As decisões já salvas serão mantidas no histórico.',
        'urgencia_normal': 'Normal',
        'urgencia_urgente': 'Urgente',
        'urgencia_muito_urgente': 'Muito Urgente',
        'alta_urgencia': '🔴 ALTA URGÊNCIA!',
        'urgencia_texto': '🟠 URGENTE!',
        'encaminhado_sucesso': 'encaminhado para Nutricionista e Agrônomo!',
        'encaminhamento_existente': 'já possui encaminhamento ativo!',
        'btn_encaminhar': '📨 Encaminhar',
        'btn_fechar': '🔒 Fechar Caso',
        'caso_fechado': 'ℹ️ Caso de',
        'fechado': 'fechado.',
        'gerar_relatorio': '📄 Gerar Relatório',
        'relatorio_clinico': 'RELATÓRIO CLÍNICO',
        'btn_pdf': '📄 Gerar PDF com QR Code',
        'medico_responsavel': 'Nome do Médico Responsável:',
        'assinatura_medico': '✍️ Assinatura Eletrónica',
        'digitar_assinatura': 'Digite a sua assinatura (nome completo):',
        'digitar_nome_assinar': 'Digite o seu nome para assinar eletronicamente',
        'informacao': 'ℹ️ Informação',
        'relatorio_info': 'O relatório será gerado com os dados do paciente e a decisão clínica atual.',
        'assinatura_info': 'A assinatura eletrónica confirma a autoria do relatório.',
        'qr_code_info': 'O QR Code permite validar a autenticidade do documento.',
        'inserir_medico_responsavel': '⚠️ Por favor, insira o nome do médico responsável',
        'inserir_assinatura': '⚠️ Por favor, digite a sua assinatura eletrónica',
        'gerando_pdf': 'Gerando relatório...',
        'pdf_gerado': 'PDF gerado com sucesso!',
        'qr_code_validar': 'O QR Code pode ser escaneado para validar a autenticidade do relatório.',
        'erro_gerar_pdf': '❌ Erro ao gerar o PDF',
        'lista_pacientes': '📋 Lista de Pacientes',
        'dashboard': '📊 Dashboard',
        'historico': '📜 Histórico',

        # ============================================================
        # ===== AGRÔNOMO - PLANO DE INTERVENÇÃO =====
        # ============================================================
        'plano_intervencao_agronomica': '📝 Plano de Intervenção Agronómica',
        'objetivos_intervencao_agro': '🎯 Objetivos da Intervenção Agronómica',
        'objetivo_principal_agro': '📋 Objetivo Principal',
        'objetivo_principal_agro_placeholder': 'Descreva o objetivo principal da intervenção agronómica...',
        'metas_especificas_agro': '📊 Metas Específicas',
        'metas_agro_placeholder': 'Liste as metas a serem alcançadas...',
        'prazo_execucao_agro': '⏱️ Prazo de Execução',
        'data_inicio_agro': '📅 Data de Início',
        'intervencoes_agronomicas': '🌾 Intervenções Agronómicas',
        'praticas_agricolas_recomendadas': '🌱 Práticas Agrícolas Recomendadas',
        'praticas_agricolas_placeholder': 'Descreva as práticas agrícolas recomendadas...',
        'culturas_recomendadas': '🌿 Culturas Recomendadas',
        'culturas_placeholder': 'Liste as culturas recomendadas...',
        'recomendacoes_agua': '💧 Recomendações sobre Água',
        'recomendacoes_agua_placeholder': 'Descreva as recomendações sobre uso da água...',
        'formacao_tecnica': '🧑‍🌾 Formação Técnica',
        'formacao_tecnica_placeholder': 'Descreva as necessidades de formação técnica...',
        'monitoramento_avaliacao_agro': '📊 Monitoramento e Avaliação',
        'frequencia_monitoramento_agro': '📅 Frequência de Monitoramento',
        'indicadores_avaliacao_agro': '📋 Indicadores de Avaliação',
        'indicadores_agro_placeholder': 'Descreva os indicadores a serem avaliados...',
        'observacoes_finais_agro': '📝 Observações Finais',
        'observacoes_agro_placeholder': 'Observações adicionais sobre o plano...',
        'planos_registados_agro': '📋 Planos Registados',
        'nenhum_plano_registado_agro': '📋 Nenhum plano registado para este paciente.',
        'preencher_objetivo_praticas': '⚠️ Preencha o objetivo principal ou as práticas agrícolas.',
        'plano_registado_agro': 'Plano agronómico registado para',
        'registar_plano_agro': '💾 Registar Plano Agronómico',
        'todos_atendidos_agro': '✅ Todos os encaminhamentos foram atendidos!',
        'lista_atendidos_agro': '📋 Lista de Atendidos',
        'recomendacoes_agroalimentares': '💡 Recomendações Agroalimentares',
    
    },
    'en': {
         'medico_titulo': 'Doctor - Clinical Assessment',
        'gestao_pacientes': '👤 Patient Management',
        'nenhum_paciente': '📋 No patients registered in the system.',
        'dados_crianca': '👶 CHILD DATA',
        'primeiro_nome': 'First Name',
        'nome_meio': 'Middle Name',
        'apelido': 'Surname',
        'data_nascimento': '📅 Date of Birth',
        'salvar_dados': '💾 Save Data',
        # ===== TÍTULOS E MENUS =====
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
        'recomendacoes': 'Recommendations',
        
        # ===== PERFIS =====
        'medico_titulo': 'Doctor - Clinical Assessment',
        'nutricionista_titulo': 'Nutritionist - Nutritional Assessment',
        'agronomo_titulo': 'Agronomist - Agri-Food Intervention',
        'enfermeiro_titulo': 'Nurse - Nutritional Screening',
        'admin_titulo': 'Administrator - Control Panel',
        
        # ===== ABAS =====
        'avaliacao': '📋 Assessment',
        'dashboard': '📊 Dashboard',
        'historico': '📜 History',
        'encaminhamentos': '📨 Referrals',
        'pacientes': 'Patients',
        'gestao_pacientes': '👤 Patient Management',
        'selecionar_paciente': '👤 Select Patient for Assessment',
        'dados_paciente': '📊 Patient Data',
        'avaliacao_risco': '🩺 Risk Assessment',
        'decisao_clinica': '📝 Clinical Decision',
        'gerar_relatorio': '📄 Generate Report',
        
        # ===== CAMPOS DO FORMULÁRIO =====
        'prescricao': '💊 Prescription',
        'diagnostico': '📋 Diagnosis',
        'seguimento': '📅 Follow-up Plan',
        'observacoes': '📋 Observations',
        'salvar': '💾 Save',
        'cancelar': '🔒 Cancel',
        'editar': '✏️ Edit',
        'fechar': '🔒 Close Case',
        'atualizar': '🔄 Update',
        'recarregar': '🔄 Reload Patients',
        'nova_decisao': '🧹 New Decision',
        
        # ===== BOTÕES =====
        'btn_salvar': '💾 Save Decision',
        'btn_encaminhar': '📨 Refer',
        'btn_pdf': '📄 Generate PDF with QR Code',
        'btn_editar': '✏️ Edit',
        'btn_fechar': '🔒 Close Case',
        'btn_cancelar': '🔒 Cancel and Return',
        'btn_atualizar_dados': '💾 Update Clinical Data',
        
        # ===== TABELAS =====
        'nome': 'Name',
        'idade': 'Age (months)',
        'peso': 'Weight (kg)',
        'altura': 'Height (cm)',
        'muac': 'MUAC (mm)',
        'dds': 'DDS',
        'hemoglobina': 'Hemoglobin',
        'tipo_anemia': 'Anemia Type',
        'risco_anemia': 'Anemia Risk',
        'risco_fome': 'Hidden Hunger',
        'risco_inseguranca': 'Food Insecurity',
        'provincia': 'Province',
        'distrito': 'District',
        'residencia': 'Residence',
        'hospital': 'Hospital',
        'data_registo': 'Registration Date',
        'data': 'Date',
        'status': 'Status',
        'urgencia': 'Urgency',
        'especialidade': 'Specialty',
        'motivo': 'Reason',
        'medico_responsavel': 'Responsible Doctor',
        
        # ===== MENSAGENS =====
        'nenhum_paciente': '📋 No patients registered in the system.',
        'nenhum_registo': '📋 No records found.',
        'nenhum_encaminhamento': '📋 No referrals registered yet.',
        'carregando': '⏳ Loading...',
        'erro_carregar': '❌ Error loading:',
        'sucesso_salvar': '✅ Data saved successfully!',
        'erro_salvar': '❌ Error saving:',
        'confirmar_exclusao': '⚠️ Are you sure you want to delete?',
        
        # ===== ENCAMINHAMENTOS =====
        'encaminhamento_integrado': '📨 Integrated Referral',
        'encaminhamento_texto': 'The patient will be referred simultaneously to <strong>Nutritionist</strong> and <strong>Agronomist</strong>.',
        'urgencia_normal': 'Normal',
        'urgencia_urgente': 'Urgent',
        'urgencia_muito_urgente': 'Very Urgent',
        'alta_urgencia': '🔴 HIGH URGENCY!',
        'urgencia_texto': '🟠 URGENT!',
        'encaminhado_sucesso': '✅ {paciente} referred to Nutritionist and Agronomist!',
        'encaminhamento_existente': '⚠️ {paciente} already has an active referral!',
        
        # ===== FILTROS =====
        'filtrar_risco': 'Filter by Anemia Risk',
        'filtrar_provincia': 'Filter by Province',
        'todas': 'All',
        'todos': 'All',
        'pendente': 'Pending',
        'em_andamento': 'In progress',
        'concluido': 'Completed',
        'data_inicio': 'Start Date',
        'data_fim': 'End Date',
        
        # ===== GRÁFICOS =====
        'distribuicao_risco': 'Anemia Risk Distribution',
        'distribuicao_fome': 'Hidden Hunger Distribution',
        'distribuicao_inseguranca': 'Food Insecurity Distribution',
        'distribuicao_tipo_anemia': 'Distribution - Anemia Type',
        'distribuicao_dds': 'Distribution - Dietary Diversity (DDS)',
        'lista_pacientes': '📋 Patient List',
        
        # ===== STATUS =====
        'alto': 'HIGH',
        'medio': 'MEDIUM',
        'baixo': 'LOW',
        'sim': 'Yes',
        'nao': 'No',
        'presente': 'Present',
        'ausente': 'Absent',
        
        # ===== RELATÓRIO PDF =====
        'relatorio_clinico': 'CLINICAL REPORT',
        'dados_clinicos': 'CLINICAL DATA',
        'assinatura_medico': 'DOCTOR\'S SIGNATURE',
        'validade': 'Validity',
        'codigo': 'Code',
        'escanear_qr': 'SCAN THE QR CODE',
        'validar_autenticidade': 'To validate the authenticity of the report',
        'documento_validado': 'Digitally validated document',
        
        # ===== PRODUÇÃO AGRÍCOLA =====
        'producao_familiar': 'Family Production',
        'acesso_terra': 'Land Access',
        'fonte_agua': 'Water Source',
        'culturas_produzidas': 'Produced Crops',
        'dificuldades_producao': 'Production Difficulties',
        'produz_consumo': 'Produces for consumption',
        'produz_venda': 'Produces for sale',
        'produz_consumo_venda': 'Produces for consumption and sale',
        'nao_produz': 'Does not produce',
        'terra_propria': 'Has own land',
        'terra_comunitaria': 'Has communal land',
        'terra_arrendada': 'Has leased land',
        'nao_tem_terra': 'Has no land',
        # ===== ENFERMEIRO =====
        'registos_carregados': 'records loaded from Supabase!',
        'supabase_indisponivel': '⚠️ Supabase not available',
        'descricao_triagem': 'Risk assessment of anemia, hidden hunger and food insecurity in children under 5 years',
        'dados_crianca': '👶 CHILD DATA',
        'primeiro_nome': 'First Name',
        'nome_meio': 'Middle Name',
        'apelido': 'Surname',
        'ex_joao': 'Ex: John',
        'ex_manuel': 'Ex: Manuel',
        'ex_silva': 'Ex: Silva',
        'data_nascimento': '📅 Date of Birth',
        'salvar_dados': '💾 Save Data',
        'preencher_nome': '⚠️ Please fill in the full name',
        'clicar_salvar_dados': '⚠️ Click \'Save Data\' to continue.',
        'meses': 'months',
        'localizacao': '📍 Location',
        'dados_mae': '👩 MOTHER\'S DATA',
        'nome_mae': 'Mother\'s Name',
        'ex_maria': 'Ex: Maria',
        'idade_mae': 'Mother\'s Age (years)',
        'escolaridade_mae': 'Mother\'s Education',
        'ensino_primario': 'Primary Education',
        'ensino_secundario': 'Secondary Education',
        'ensino_superior': 'Higher Education',
        'ocupacao_mae': 'Mother\'s Occupation',
        'agregado_familiar': 'Household Size',
        'rendimento_familiar': 'Family Income (MZN)',
        'avaliacao_antropometrica': '📏 ANTHROPOMETRIC ASSESSMENT',
        'peso_kg': 'Weight (kg)',
        'altura_cm': 'Height (cm)',
        'muac_mm': 'MUAC (mm)',
        'edema': 'Edema',
        'ausente': 'Absent',
        'presente': 'Present',
        'perda_peso': 'Weight loss',
        'nao': 'No',
        'sim': 'Yes',
        'apatia': 'Apathy',
        'febre': 'Fever',
        'diarreia': '💧 Diarrhea (last 2 weeks)',
        'sim_1_3_dias': 'Yes, 1-3 days',
        'sim_4_7_dias': 'Yes, 4-7 days',
        'sim_mais_7_dias': 'Yes, more than 7 days',
        'doenca_cronica': '🏥 Chronic Disease',
        'nenhuma': 'None',
        'doenca_cardiaca': 'Heart Disease',
        'doenca_renal': 'Kidney Disease',
        'desnutricao_cronica': 'Chronic Malnutrition',
        'outra': 'Other',
        'especificar_doenca': 'Specify the disease:',
        'avaliacao_fisica': '💇 PHYSICAL ASSESSMENT',
        'cabelo': 'Hair',
        'pigmentado_abundante': 'Pigmented and abundant',
        'pigmentado_fino': 'Pigmented and thin',
        'despigmentado': 'Depigmented',
        'despigmentado_fino_raro': 'Depigmented thin and rare',
        'mucosas': 'Mucous membranes',
        'coradas': 'Colored',
        'hipocoradas': 'Hypocolored',
        'muito_hipocoradas': 'Very hypocolored',
        'suplementacao': '💊 SUPPLEMENTATION',
        'suplementacao_ferro': 'Iron Supplementation',
        'suplementacao_vit_a': 'Vitamin A Supplementation',
        'em_curso': 'In progress',
        'desparasitacao': 'Deworming',
        'nao_sabe': 'Don\'t know',
        'historico_alimentar': '🍽️ FEEDING HISTORY',
        'amamentacao': 'Breastfeeding',
        'meses_amamentacao': 'Months of exclusive breastfeeding',
        'amamentacao_desativada': '🚫 Breastfeeding disabled (>24 months)',
        'refeicoes_dia': 'Meals per day',
        'diversidade_alimentar': 'Dietary Diversity (DDS)',
        'alimentos_consumidos': '🥗 FOODS CONSUMED',
        'frutas': 'Fruits',
        'carnes': 'Meats',
        'carne_bovina': 'Beef',
        'carne_frango': 'Chicken',
        'carne_cabra': 'Goat meat',
        'peixe': 'Fish',
        'peixe_fresco': 'Fresh fish',
        'peixe_seco': 'Dried fish',
        'ovos': 'Eggs',
        'ovo_galinha': 'Chicken egg',
        'leguminosas': 'Legumes',
        'cereais': 'Cereals',
        'verduras': 'Vegetables',
        'producao_agricola': '🌾 AGRICULTURAL PRODUCTION',
        'produz_consumo': 'Produces for consumption',
        'produz_venda': 'Produces for sale',
        'produz_consumo_venda': 'Produces for consumption and sale',
        'nao_produz': 'Does not produce',
        'terra_propria': 'Has own land',
        'terra_comunitaria': 'Has communal land',
        'terra_arrendada': 'Has leased land',
        'nao_tem_terra': 'Has no land',
        'culturas_produzidas': '3. Main crops produced:',
        'especificar_culturas': 'Specify other crops:',
        'fonte_agua': '4. Water source for production:',
        'agua_chuva': 'Rainwater',
        'sistema_irrigacao': 'Irrigation system',
        'dificuldades_producao': '5. Main production difficulties:',
        'falta_sementes': 'Lack of seeds',
        'falta_fertilizantes': 'Lack of fertilizers',
        'solo_pouco_fertil': 'Low fertility soil',
        'pragas_doencas': 'Pests and diseases',
        'falta_chuva_seca': 'Lack of rain/drought',
        'cheias_excesso_chuva': 'Floods/excess rain',
        'falta_conhecimento_tecnico': 'Lack of technical knowledge',
        'falta_mao_obra': 'Lack of labor',
        'falta_equipamento_agricola': 'Lack of agricultural equipment',
        'nenhuma_dificuldade': 'No difficulties',
        'calcular_risco': '🧮 Calculate Risk',
        'crianca_5_anos': '❌ Child is 5 years or older!',
        'registado_supabase': 'registered in Supabase!',
        'registado_local': 'registered locally!',
        'erro_salvar': '⚠️ Error saving:',
        'anemia': 'Anemia',
        'fome_oculta': 'Hidden Hunger',
        'inseguranca_alimentar': 'Food Insecurity',
        'score': 'Score',
        'confianca': 'Confidence',
        'alto': 'HIGH',
        'medio': 'MEDIUM',
        'baixo': 'LOW',
        'recomendacao_anemia_alto': 'Refer to doctor for iron supplementation',
        'recomendacao_anemia_alto_2': 'Increase consumption of red meat, liver and beans',
        'recomendacao_anemia_medio': 'Increase consumption of iron-rich foods',
        'recomendacao_anemia_medio_2': 'Combine iron-rich foods with vitamin C',
        'recomendacao_fome_alto': 'Diversify diet with fruits, vegetables and greens',
        'recomendacao_fome_alto_2': 'Include dark leafy greens (spinach, kale) daily',
        'recomendacao_inseg_alto': 'Assess food supplementation programs',
        'recomendacao_inseg_alto_2': 'Guide on using local food resources',
        'recomendacao_ok': 'Child has good nutritional status. Maintain regular follow-up.',
        'nutricionista_titulo': 'Nutritionist - Nutritional Assessment',
        'descricao_nutricionista': 'Nutritional assessment, monitoring and recommendations for patients.',
        'anemia_alta': 'HIGH Anemia',
        'fome_oculta_alta': 'HIGH Hidden Hunger',
        'inseguranca_alta': 'HIGH Food Insecurity',
        'pacientes_anemia_alta': 'patients with HIGH anemia risk',
        'pacientes_anemia_media': 'patients with MEDIUM anemia risk',
        'pacientes_fome_alta': 'patients with HIGH hidden hunger',
        'pacientes_inseguranca_alta': 'patients with HIGH food insecurity',
        'todos_baixo_risco': 'All patients have LOW risk. Maintain preventive follow-up.',
        'recomendacao_anemia_alta': 'Prioritize iron supplementation and iron-rich foods.',
        'recomendacao_anemia_media': 'Strengthen nutritional guidance and monitoring.',
        'recomendacao_fome_alta': 'Diversify diet with fruits, vegetables and greens.',
        'recomendacao_inseguranca_alta': 'Assess food supplementation programs.',
        'orientacoes_familia': 'Guidelines for the Family',
        'dica_1': 'Varied diet with 5 food groups per day',
        'dica_2': 'Include iron-rich foods (meat, beans, spinach)',
        'dica_3': 'Eat colorful fruits and vegetables daily',
        'dica_4': 'Avoid excessive sugar and fats',
        'dica_5': 'Drink clean water and maintain good hygiene practices',
        # ============================================================
        # ===== NUTRITIONIST - TRANSLATIONS =====
        # ============================================================
        'nutricionista_titulo': 'Nutritionist - Nutritional Assessment',
        'descricao_nutricionista': 'Nutritional assessment, monitoring and recommendations for patients.',
        'anemia_alta': 'HIGH Anemia',
        'fome_oculta_alta': 'HIGH Hidden Hunger',
        'inseguranca_alta': 'HIGH Food Insecurity',
        'pacientes_anemia_alta': 'patients with HIGH anemia risk',
        'pacientes_anemia_media': 'patients with MEDIUM anemia risk',
        'pacientes_fome_alta': 'patients with HIGH hidden hunger',
        'pacientes_inseguranca_alta': 'patients with HIGH food insecurity',
        'todos_baixo_risco': 'All patients have LOW risk. Maintain preventive follow-up.',
        'recomendacao_anemia_alta': 'Prioritize iron supplementation and iron-rich foods.',
        'recomendacao_anemia_media': 'Strengthen nutritional guidance and monitoring.',
        'recomendacao_fome_alta': 'Diversify diet with fruits, vegetables and greens.',
        'recomendacao_inseguranca_alta': 'Assess food supplementation programs.',
        'orientacoes_familia': '📋 Guidelines for the Family',
        'dica_1': 'Varied diet with 5 food groups per day',
        'dica_2': 'Include iron-rich foods (meat, beans, spinach)',
        'dica_3': 'Eat colorful fruits and vegetables daily',
        'dica_4': 'Avoid excessive sugar and fats',
        'dica_5': 'Drink clean water and maintain good hygiene practices',
        'avaliacao_nutricional': '🥗 Nutritional Assessment',
        'diversidade_alimentar_dds': '📊 Dietary Diversity (DDS)',
        'dds_slider': 'DDS (Dietary Diversity)',
        'frequencia_refeicoes': '🍽️ Meal Frequency',
        'refeicoes_por_dia': 'Meals per day',
        'consumo_proteina': '🥩 Protein Consumption',
        'fonte_proteina': 'Protein source',
        'consumo_vitamina_c': '🍊 Vitamin C Consumption',
        'fonte_vitamina_c': 'Vitamin C source',
        'observacoes_nutricionais': '🥬 Nutritional Observations',
        'observacoes_placeholder': 'Notes about the nutritional assessment...',
        'salvar_avaliacao': '💾 Save Assessment',
        'avaliacao_salva': 'Nutritional assessment saved for',
        'plano_alimentar': '📝 Meal Plan',
        'frequencia_refeicoes_recomendada': '🍽️ Recommended meal frequency',
        'proteinas_recomendadas': '🥩 Recommended proteins',
        'frutas_verduras_recomendadas': '🍎 Recommended fruits and vegetables',
        'observacoes_plano': '📋 Plan Observations',
        'observacoes_plano_placeholder': 'Notes about the meal plan...',
        'registar_plano': '💾 Register Plan',
        'plano_registado': 'Meal plan registered for',
        'selecionar_alimentos': '⚠️ Select at least one protein or fruit/vegetable.',
        'plano_intervencao': '📝 Nutrition Intervention Plan',
        'objetivos_intervencao': '🎯 Intervention Objectives',
        'objetivo_principal': '📋 Main Objective',
        'objetivo_principal_placeholder': 'Describe the main objective of the intervention...',
        'metas_especificas': '📊 Specific Goals',
        'metas_placeholder': 'List the goals to be achieved...',
        'prazo_execucao': '⏱️ Execution Deadline',
        'data_inicio': '📅 Start Date',
        'intervencoes_nutricionais': '🍽️ Nutritional Interventions',
        'recomendacoes_dieteticas': '🥗 Dietary Recommendations',
        'recomendacoes_placeholder': 'Describe the dietary recommendations...',
        'suplementacao_recomendada': '💊 Recommended Supplementation',
        'suplementacao_placeholder': 'Describe the recommended supplementation...',
        'atividades_educativas': '📋 Educational Activities',
        'atividades_placeholder': 'Describe the planned educational activities...',
        'envolvimento_familiar': '👨‍👩‍👧‍👦 Family Involvement',
        'envolvimento_placeholder': 'Describe how the family will be involved...',
        'monitoramento_avaliacao': '📊 Monitoring and Evaluation',
        'frequencia_monitoramento': '📅 Monitoring Frequency',
        'indicadores_avaliacao': '📋 Evaluation Indicators',
        'indicadores_placeholder': 'Describe the indicators to be evaluated...',
        'observacoes_finais': '📝 Final Observations',
        'observacoes_plano_placeholder': 'Additional observations about the plan...',
        'planos_registados': '📋 Registered Plans',
        'plano': 'Plan',
        'marcar_concluido': '✅ Mark as Completed',
        'remover': '🗑️ Remove',
        'nenhum_plano_registado': '📋 No plan registered for this patient.',
        'preencher_objetivo_recomendacoes': '⚠️ Fill in the main objective or dietary recommendations.',
        'lista_pendentes': '📋 Pending List',
        'lista_atendidos': '📋 Attended List',
        'todos_atendidos': '✅ All referrals have been attended!',
        'encaminhamentos_recebidos': '📨 Referrals Received',
        'nenhum_encaminhamento_nutricionista': '📋 No referrals for nutritionist received yet.',
        'recomendacoes_nutricionais': '💡 Nutritional Recommendations',
        'analise_nutricional': '📊 Nutritional Analysis',

        # ============================================================
        # ===== AGRONOMIST - TRANSLATIONS =====
        # ============================================================
        'agronomo_titulo': 'Agronomist - Agri-Food Intervention',
        'descricao_agronomo': 'Agri-food assessment, climate resilience and recommendations for families referred by the doctor.',
        'total_pacientes': 'Total Patients',
        'encaminhamentos': 'Referrals',
        'pendentes': 'Pending',
        'atendidos': 'Attended',
        'selecionar_paciente': '👤 Select Patient',
        'dados_paciente': '📊 Patient Data',
        'nome': 'Name',
        'idade': 'Age (months)',
        'peso': 'Weight (kg)',
        'altura': 'Height (cm)',
        'muac': 'MUAC (mm)',
        'dds': 'DDS',
        'provincia': 'Province',
        'distrito': 'District',
        'risco': '🩺 Risk',
        'risco_anemia': 'Anemia Risk',
        'risco_fome': 'Hidden Hunger',
        'risco_inseguranca': 'Food Insecurity',
        'producao_familiar': '🌾 Family Production',
        'acesso_terra': '🏠 Land Access',
        'fonte_agua': '💧 Water Source',
        'culturas_produzidas': '🌱 Produced Crops',
        'dificuldades_producao': '🌾 Production Difficulties',
        'nenhuma_dificuldade': 'No difficulties recorded',
        'avaliacao_resiliencia': '🌾 Agri-Food Resilience Assessment',
        'descricao_resiliencia': 'Fill out the form to assess the family\'s climate and productive resilience.',
        'pergunta_disponibilidade_agua': 'What is the water availability for agricultural production?',
        'pergunta_exposicao_climatica': 'How do you classify the farm\'s exposure to climate events in the last 5 years?',
        'pergunta_estado_solo': 'What is the current soil condition and conservation practices?',
        'pergunta_sistema_producao': 'How do you characterize the agricultural production system?',
        'pergunta_capacidade_adaptativa': 'What is the level of adaptive capacity of the farming family?',
        'pergunta_impacto_producao': 'What was the impact of agricultural production on the family\'s food security in the last 12 months?',
        'selecione_opcao': 'Select an option:',
        'legenda_calcular_indices': 'After answering all questions, click "Calculate Indices" to get the results.',
        'calcular_indices': '📊 Calculate Indices',
        'indices_calculados': 'Indices calculated successfully!',
        'resultados_indices': '📊 Indices Results',
        'recomendacoes': '💡 Recommendations',
        'registar_intervencao': '📝 Register Intervention',
        'recomendacoes_tecnicas': '🌾 Technical Recommendations',
        'culturas_recomendadas': '🌱 Recommended Crops',
        'praticas_recomendadas': '🔄 Recommended Agricultural Practices',
        'observacoes': '📋 Observations',
        'registar': '💾 Register',
        'intervencao_registada': 'Intervention registered successfully!',
        'preencher_recomendacoes': '⚠️ Fill in the technical recommendations.',
        'analise_agroalimentar': '📊 Agri-Food Analysis',
        'dados_encaminhamento': '📋 Referral Data',
        'especialidade': 'Specialty',
        'urgencia': 'Urgency',
        'motivo': 'Reason',
        'status': 'Status',
        'medico_responsavel': 'Responsible Doctor',
        'dados_agroalimentares': '📊 Agri-Food Data',
        'marcar_atendido': '✅ Mark as Attended',
        'nenhum_encaminhamento_agronomo': '📋 No referrals for agronomist received yet.',
        'distribuicao': 'Distribution',
        'principais_culturas': '🌱 Main Crops Produced',
        'carregados': 'loaded',
        'supabase_indisponivel': '⚠️ Supabase not available',
        'nenhum_paciente': '📋 No patients registered in the system.',
        'nenhum_registo': '📋 No records found.',
        'casos_aguardam_avaliacao': 'cases awaiting medical evaluation',
        'recarregar': '🔄 Reload',
        'atualizar_dados_clinicos': '🩺 Update Clinical Data',
        'atualizar_dados_caption': 'Update clinical data if necessary. Leave blank to keep current values.',
        'selecione_tipo': 'Select the type:',
        'selecione_resultado': 'Select the result:',
        'ultimas_2_semanas': 'last 2 weeks',
        'doenca_cronica': '🏥 Chronic Disease',
        'doenca_cronica_conhecida': 'Known chronic disease:',
        'especificar_doenca': '📋 Specify Disease',
        'especificar_doenca_texto': 'Specify the chronic disease (if applicable):',
        'btn_atualizar_dados': '💾 Update Clinical Data',
        'dados_atualizados': 'Clinical data of',
        'dados_atualizados_local': 'Clinical data of',
        'erro_atualizar': '❌ Error updating',
        'nenhum_dado_alterado': '⚠️ No data was changed',
        'selecionar_paciente_valido': '❌ Select a valid patient',
        'nova_decisao_clinica': '📝 New Clinical Decision',
        'preencher_campos_decisao': 'Fill in the fields below to register a new clinical decision for this patient.',
        'prescricao': '💊 Prescription',
        'diagnostico': '📋 Diagnosis',
        'seguimento': '📅 Follow-up Plan',
        'notas_caso': 'Notes about the case...',
        'btn_salvar': '💾 Save Decision',
        'decisao_registada': 'Decision of',
        'no_supabase': 'registered in Supabase!',
        'decisao_local_erro': 'Decision saved locally. Error:',
        'localmente': 'registered locally!',
        'preencher_diagnostico_prescricao': '⚠️ Fill in diagnosis or prescription',
        'btn_nova_decisao': '🧹 New Decision',
        'clicar_limpar_campos': 'Click to clear fields and add a new decision',
        'encaminhamento_integrado': '📨 Integrated Referral',
        'encaminhamento_texto': 'The patient will be referred simultaneously to <strong>Nutritionist</strong> and <strong>Agronomist</strong>.',
        'encaminhamento_info': 'Saved decisions will be kept in the history.',
        'urgencia_normal': 'Normal',
        'urgencia_urgente': 'Urgent',
        'urgencia_muito_urgente': 'Very Urgent',
        'alta_urgencia': '🔴 HIGH URGENCY!',
        'urgencia_texto': '🟠 URGENT!',
        'encaminhado_sucesso': 'referred to Nutritionist and Agronomist!',
        'encaminhamento_existente': 'already has an active referral!',
        'btn_encaminhar': '📨 Refer',
        'btn_fechar': '🔒 Close Case',
        'caso_fechado': 'ℹ️ Case of',
        'fechado': 'closed.',
        'gerar_relatorio': '📄 Generate Report',
        'relatorio_clinico': 'CLINICAL REPORT',
        'btn_pdf': '📄 Generate PDF with QR Code',
        'medico_responsavel': 'Responsible Doctor Name:',
        'assinatura_medico': '✍️ Electronic Signature',
        'digitar_assinatura': 'Enter your signature (full name):',
        'digitar_nome_assinar': 'Enter your name to sign electronically',
        'informacao': 'ℹ️ Information',
        'relatorio_info': 'The report will be generated with patient data and the current clinical decision.',
        'assinatura_info': 'The electronic signature confirms the authorship of the report.',
        'qr_code_info': 'The QR Code allows validating the authenticity of the document.',
        'inserir_medico_responsavel': '⚠️ Please enter the responsible doctor\'s name',
        'inserir_assinatura': '⚠️ Please enter your electronic signature',
        'gerando_pdf': 'Generating report...',
        'pdf_gerado': 'PDF generated successfully!',
        'qr_code_validar': 'The QR Code can be scanned to validate the authenticity of the report.',
        'erro_gerar_pdf': '❌ Error generating PDF',
        'lista_pacientes': '📋 Patient List',
        'dashboard': '📊 Dashboard',
        'historico': '📜 History',

        # ============================================================
        # ===== AGRONOMIST - INTERVENTION PLAN =====
        # ============================================================
        'plano_intervencao_agronomica': '📝 Agronomic Intervention Plan',
        'objetivos_intervencao_agro': '🎯 Agronomic Intervention Objectives',
        'objetivo_principal_agro': '📋 Main Objective',
        'objetivo_principal_agro_placeholder': 'Describe the main objective of the agronomic intervention...',
        'metas_especificas_agro': '📊 Specific Goals',
        'metas_agro_placeholder': 'List the goals to be achieved...',
        'prazo_execucao_agro': '⏱️ Execution Deadline',
        'data_inicio_agro': '📅 Start Date',
        'intervencoes_agronomicas': '🌾 Agronomic Interventions',
        'praticas_agricolas_recomendadas': '🌱 Recommended Agricultural Practices',
        'praticas_agricolas_placeholder': 'Describe the recommended agricultural practices...',
        'culturas_recomendadas': '🌿 Recommended Crops',
        'culturas_placeholder': 'List the recommended crops...',
        'recomendacoes_agua': '💧 Water Recommendations',
        'recomendacoes_agua_placeholder': 'Describe the water use recommendations...',
        'formacao_tecnica': '🧑‍🌾 Technical Training',
        'formacao_tecnica_placeholder': 'Describe the technical training needs...',
        'monitoramento_avaliacao_agro': '📊 Monitoring and Evaluation',
        'frequencia_monitoramento_agro': '📅 Monitoring Frequency',
        'indicadores_avaliacao_agro': '📋 Evaluation Indicators',
        'indicadores_agro_placeholder': 'Describe the indicators to be evaluated...',
        'observacoes_finais_agro': '📝 Final Observations',
        'observacoes_agro_placeholder': 'Additional observations about the plan...',
        'planos_registados_agro': '📋 Registered Plans',
        'nenhum_plano_registado_agro': '📋 No plan registered for this patient.',
        'preencher_objetivo_praticas': '⚠️ Fill in the main objective or agricultural practices.',
        'plano_registado_agro': 'Agronomic plan registered for',
        'registar_plano_agro': '💾 Register Agronomic Plan',
        'todos_atendidos_agro': '✅ All referrals have been attended!',
        'lista_atendidos_agro': '📋 Attended List',
        'recomendacoes_agroalimentares': '💡 Agri-Food Recommendations',
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

# ===== SUPABASE =====
try:
    from supabase_config import (
        supabase,
        SUPABASE_AVAILABLE,
        salvar_crianca_supabase,
        carregar_criancas_supabase
    )
    print("✅ Supabase importado com sucesso!")
except ImportError:
    supabase = None
    SUPABASE_AVAILABLE = False
    def salvar_crianca_supabase(dados):
        return False, "Modo offline - Supabase não disponível"
    def carregar_criancas_supabase():
        return False, []
    print("⚠️ Modo offline - Supabase não disponível")

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
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            
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
# FORMULÁRIO ENFERMEIRO
# ============================================================
def formulario_enfermeiro():
    submitted = False
    data = {}
    
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
            from pages.enfermeiro import render_enfermeiro
            render_enfermeiro()
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

# ============================================================
# EXECUTAR APP
# ============================================================
if __name__ == "__main__":
    main()