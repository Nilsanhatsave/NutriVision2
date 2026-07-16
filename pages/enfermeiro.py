# pages/enfermeiro.py
# ===== PERFIL ENFERMEIRO - TRIAGEM NUTRICIONAL =====

import streamlit as st
from datetime import datetime, timedelta
import random
import sys
import os

# Adicionar o diretório pai ao path para importar funções
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import t, calcular_idade, IAClassifier, SUPABASE_AVAILABLE, salvar_crianca_supabase, carregar_criancas_supabase

# ============================================================
# FORMULÁRIO ENFERMEIRO
# ============================================================
def render_enfermeiro():
    submitted = False
    data = {}
    
    if SUPABASE_AVAILABLE:
        try:
            sucesso, dados = carregar_criancas_supabase()
            if sucesso and dados:
                st.session_state.criancas = dados
                st.success(f"✅ {len(dados)} {t('registos_carregados')}")
            else:
                st.session_state.criancas = []
                st.info(t('nenhum_registo'))
        except Exception as e:
            st.error(f"❌ {t('erro_carregar')} {e}")
            st.session_state.criancas = []
    else:
        st.warning(t('supabase_indisponivel'))
        st.session_state.criancas = []
    
    st.title(f"{st.session_state.icone} {t('triagem')}")
    st.markdown(t('descricao_triagem'))
    
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
        
        st.markdown(f'<div class="section-title">{t("dados_crianca")}</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            primeiro_nome = st.text_input(t('primeiro_nome'), placeholder=t('ex_joao'))
        with col2:
            nome_meio = st.text_input(t('nome_meio'), placeholder=t('ex_manuel'))
        with col3:
            ultimo_nome = st.text_input(t('apelido'), placeholder=t('ex_silva'))
        
        nome_completo = f"{primeiro_nome} {nome_meio} {ultimo_nome}".strip()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            data_nascimento = st.date_input(
                t('data_nascimento'),
                value=datetime.now() - timedelta(days=730),
                max_value=datetime.now()
            )
            idade_meses = calcular_idade(data_nascimento)
        
        with col2:
            st.write("")
            st.write("")
            if st.form_submit_button(t('salvar_dados'), use_container_width=True):
                if nome_completo:
                    st.session_state.dados_basicos_salvos = True
                    st.session_state.nome_salvo = nome_completo
                    st.session_state.data_salva = data_nascimento
                    st.session_state.idade_calculada = idade_meses
                    st.success(f"✅ {nome_completo} - {idade_meses} {t('meses')}")
                    st.rerun()
                else:
                    st.warning(t('preencher_nome'))
        
        if not st.session_state.dados_basicos_salvos:
            st.warning(t('clicar_salvar_dados'))
            st.stop()
        
        nome_completo = st.session_state.nome_salvo
        data_nascimento = st.session_state.data_salva
        idade_meses = st.session_state.idade_calculada
        
        st.info(f"👶 {nome_completo} - {idade_meses} {t('meses')}")
        st.divider()
        
        st.markdown(f"### {t('localizacao')}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            provincia = st.selectbox(
                t('provincia'),
                ["Cabo Delgado", "Gaza", "Inhambane", "Manica", "Maputo Cidade", 
                 "Maputo Província", "Nampula", "Niassa", "Sofala", "Tete", "Zambézia"]
            )
        with col2:
            distrito = st.text_input(t('distrito'))
        with col3:
            residencia = st.text_input(t('residencia'))
        with col4:
            hospital = st.text_input(t('hospital'))
        
        st.divider()
        
        st.markdown(f'<div class="section-title">{t("dados_mae")}</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            nome_mae = st.text_input(t('nome_mae'), placeholder=t('ex_maria'))
        with col2:
            idade_mae = st.number_input(t('idade_mae'), 12, 60, 25)
        with col3:
            escolaridade_mae = st.selectbox(t('escolaridade_mae'), 
                ["Nenhum", t('ensino_primario'), t('ensino_secundario'), t('ensino_superior')])
        with col4:
            ocupacao_mae = st.text_input(t('ocupacao_mae'))
        
        col1, col2 = st.columns(2)
        with col1:
            agregado_familiar_mae = st.number_input(t('agregado_familiar'), 1, 20, 5)
        with col2:
            rendimento_familiar_mae = st.number_input(t('rendimento_familiar'), 0, 100000, 5000)
        
        st.divider()
        
        st.markdown(f'<div class="section-title">{t("avaliacao_antropometrica")}</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            peso = st.number_input(t('peso_kg'), 0.0, 50.0, 10.0, 0.1)
        with col2:
            altura = st.number_input(t('altura_cm'), 0.0, 120.0, 85.0, 0.1)
        with col3:
            muac = st.number_input(t('muac_mm'), 0, 200, 130)
        with col4:
            if altura > 0 and peso > 0:
                imc = peso / ((altura/100) ** 2)
                st.metric("IMC", f"{imc:.1f}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            edema = st.radio(t('edema'), [t('ausente'), t('presente')], horizontal=True)
        with col2:
            perda_peso = st.selectbox(t('perda_peso'), [t('nao'), t('sim')])
        with col3:
            apatia = st.selectbox(t('apatia'), [t('nao'), t('sim')])
        with col4:
            febre = st.selectbox(t('febre'), [t('nao'), t('sim')])
        
        diarreia = st.selectbox(
            t('diarreia'),
            [t('nao'), t('sim_1_3_dias'), t('sim_4_7_dias'), t('sim_mais_7_dias')]
        )
        
        doenca_cronica = st.selectbox(
            t('doenca_cronica'),
            [t('nenhuma'), "HIV/SIDA", "Tuberculose", t('doenca_cardiaca'), 
             t('doenca_renal'), "Diabetes", "Asma", t('desnutricao_cronica'), t('outra')]
        )
        
        if doenca_cronica == t('outra'):
            doenca_especificar = st.text_input(t('especificar_doenca'))
        else:
            doenca_especificar = ""
        
        st.divider()
        
        st.markdown(f'<div class="section-title">{t("avaliacao_fisica")}</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            cabelo = st.selectbox(
                t('cabelo'),
                [t('pigmentado_abundante'), t('pigmentado_fino'), t('despigmentado'), t('despigmentado_fino_raro')]
            )
        with col2:
            mucosa = st.selectbox(
                t('mucosas'),
                [t('coradas'), t('hipocoradas'), t('muito_hipocoradas')]
            )
        
        st.divider()
        
        st.markdown(f'<div class="section-title">{t("suplementacao")}</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            suplementacao_ferro = st.selectbox(t('suplementacao_ferro'), [t('nao'), t('sim'), t('em_curso')])
        with col2:
            suplementacao_vit_a = st.selectbox(t('suplementacao_vit_a'), [t('nao'), t('sim'), t('em_curso')])
        with col3:
            desparasitacao = st.selectbox(t('desparasitacao'), [t('nao'), t('sim'), t('nao_sabe')])
        
        st.divider()
        
        st.markdown(f'<div class="section-title">{t("historico_alimentar")}</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if idade_meses > 24:
                amamentacao = t('nao')
                meses_amamentacao = 0
                st.info(t('amamentacao_desativada'))
            else:
                amamentacao = st.selectbox(t('amamentacao'), [t('nao'), t('sim')])
                if amamentacao == t('sim'):
                    meses_amamentacao = st.number_input(t('meses_amamentacao'), 0, 24, 6)
                else:
                    meses_amamentacao = 0
        with col2:
            refeicoes_dia = st.selectbox(t('refeicoes_dia'), ["1", "2", "3", "4", "5+"])
        with col3:
            dds_score = st.slider(t('diversidade_alimentar'), 0, 9, 5)
        
        st.divider()
        
        st.markdown(f'<div class="section-title">{t("alimentos_consumidos")}</div>', unsafe_allow_html=True)
        
        alimentos = {
            t('frutas'): ["Banana", "Manga", "Laranja", "Goiaba"],
            t('carnes'): [t('carne_bovina'), t('carne_frango'), t('carne_cabra')],
            t('peixe'): [t('peixe_fresco'), t('peixe_seco')],
            t('ovos'): [t('ovo_galinha')],
            t('leguminosas'): ["Feijão", "Amendoim"],
            t('cereais'): ["Milho", "Arroz", "Mandioca"],
            t('verduras'): ["Espinafre", "Couve", "Cenoura"]
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
        
        st.markdown(f'<div class="section-title">{t("producao_agricola")}</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            producao_familiar = st.selectbox(
                t('producao_familiar'),
                [t('produz_consumo'), t('produz_venda'), t('produz_consumo_venda'), t('nao_produz')],
                key="producao_familiar"
            )
        with col2:
            acesso_terra = st.selectbox(
                t('acesso_terra'),
                [t('terra_propria'), t('terra_comunitaria'), t('terra_arrendada'), t('nao_tem_terra')],
                key="acesso_terra"
            )

        col1, col2 = st.columns(2)
        with col1:
            culturas_produzidas = st.selectbox(
                t('culturas_produzidas'),
                ["Milho", "Feijão", "Mandioca", "Amendoim", "Batata Doce", 
                 "Hortaliças", "Frutas", "Arroz", "Cana-de-Açúcar", t('outra')],
                key="culturas_produzidas"
            )
            if culturas_produzidas == t('outra'):
                outras_culturas = st.text_input(t('especificar_culturas'), key="outras_culturas")
            else:
                outras_culturas = ""
        with col2:
            fonte_agua = st.selectbox(
                t('fonte_agua'),
                ["Rio", "Poço", "Furo", "Lago", "Nascente", t('agua_chuva'), t('sistema_irrigacao'), t('nenhuma')],
                key="fonte_agua"
            )

        dificuldades = st.selectbox(
            t('dificuldades_producao'),
            [t('falta_sementes'), t('falta_fertilizantes'), t('solo_pouco_fertil'), 
             t('pragas_doencas'), t('falta_chuva_seca'), t('cheias_excesso_chuva'), 
             t('falta_conhecimento_tecnico'), t('falta_mao_obra'), 
             t('falta_equipamento_agricola'), t('nenhuma_dificuldade')],
            key="dificuldades"
        )

        st.divider()
        
        submitted = st.form_submit_button(t('calcular_risco'), use_container_width=True)
    
    if submitted:
        if idade_meses >= 60:
            st.error(t('crianca_5_anos'))
        elif not nome_completo:
            st.error(t('preencher_nome'))
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
                'culturas_produzidas': outras_culturas if culturas_produzidas == t('outra') else culturas_produzidas,
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
                        st.success(f"✅ {nome_completo} {t('registado_supabase')}")
                    else:
                        st.warning(f"⚠️ {t('erro_salvar')} {resultado}")
                        st.session_state.criancas.append(data)
                        st.success(f"✅ {nome_completo} {t('registado_local')}")
                except Exception as e:
                    st.session_state.criancas.append(data)
                    st.success(f"✅ {nome_completo} {t('registado_local')}")
            else:
                st.session_state.criancas.append(data)
                st.success(f"✅ {nome_completo} {t('registado_local')}")
            
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
                    <h4>🩸 {t('anemia')}</h4>
                    <h2>{t(risco_anemia.lower())}</h2>
                    <p>{t('score')}: {score_anemia}/100</p>
                    <p>{t('confianca')}: {conf_anemia*100:.1f}%</p>
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
                    <h4>🍽️ {t('fome_oculta')}</h4>
                    <h2>{t(risco_fome.lower())}</h2>
                    <p>{t('score')}: {score_fome}/100</p>
                    <p>{t('confianca')}: {conf_fome*100:.1f}%</p>
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
                    <h4>🏠 {t('inseguranca_alimentar')}</h4>
                    <h2>{t(risco_inseg.lower())}</h2>
                    <p>{t('score')}: {score_inseg}/100</p>
                    <p>{t('confianca')}: {conf_inseg*100:.1f}%</p>
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
                st.warning(f"🔴 {t('recomendacao_anemia_alto')}")
                st.info(f"🥩 {t('recomendacao_anemia_alto_2')}")
            elif risco_anemia == "MÉDIO":
                st.info(f"🟠 {t('recomendacao_anemia_medio')}")
                st.info(f"🍊 {t('recomendacao_anemia_medio_2')}")
            
            if risco_fome == "ALTO":
                st.warning(f"🔴 {t('recomendacao_fome_alto')}")
                st.info(f"🥬 {t('recomendacao_fome_alto_2')}")
            
            if risco_inseg == "ALTO":
                st.warning(f"🔴 {t('recomendacao_inseg_alto')}")
                st.info(f"🏠 {t('recomendacao_inseg_alto_2')}")
            
            if risco_anemia == "BAIXO" and risco_fome == "BAIXO" and risco_inseg == "BAIXO":
                st.success(f"✅ {t('recomendacao_ok')}")
    # ============================================================
    # BOTÃO NOVO CASO
    # ============================================================
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🆕 Novo Caso", use_container_width=True):
            st.session_state.dados_basicos_salvos = False
            st.session_state.nome_salvo = ""
            st.session_state.data_salva = None
            st.session_state.idade_calculada = 0
            st.rerun()

if __name__ == "__main__":
    render_enfermeiro()
