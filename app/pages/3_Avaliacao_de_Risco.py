from pathlib import Path
import sys

import joblib
import pandas as pd
import streamlit as st


# ==========================================================
# CAMINHOS DO PROJETO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.modeling import FEATURES_NUMERICAS, explicar_previsao
from utils.styles import aplicar_estilo


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Avaliação de Risco | Passos Mágicos",
    layout="wide",
)

aplicar_estilo()

# Limiar utilizado apenas como referência operacional.
# O projeto não definiu um limiar de produção baseado
# em uma regra de negócio.
LIMIAR_REFERENCIA = 0.50


# ==========================================================
# CSS LOCAL
# ==========================================================

st.markdown(
    """
<style>

/* ======================================================
   PALETA DA PÁGINA
   Azul-petróleo = estrutura
   Turquesa/azul = informação e entrada
   Âmbar = referência operacional
   Coral = atenção / aumento do risco
   Verde = não sinalizado / redução do risco
   Lilás = modelo / explicabilidade
   ====================================================== */

:root {
    --risk-navy: #073B63;
    --risk-teal: #18A6A6;
    --risk-sky: #42A5D9;
    --risk-green: #45B98C;
    --risk-amber: #F2B544;
    --risk-coral: #F47C6C;
    --risk-purple: #8B73C7;
    --risk-border: #DDEAF0;
    --risk-muted: #60798B;
}

/* ======================================================
   FORMULÁRIO
   ====================================================== */

/* Cabeçalhos vetoriais das subseções do formulário */
.form-section-head {
    display: flex;
    align-items: center;
    gap: 0.78rem;
    margin: 0.15rem 0 0.95rem 0;
    padding: 0.78rem 0.9rem;
    border-radius: 13px;
    border: 1px solid #E2EDF2;
    background: #F8FBFC;
}

.form-section-icon {
    width: 38px;
    height: 38px;
    min-width: 38px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.form-section-icon svg {
    width: 21px;
    height: 21px;
    fill: none;
    stroke: currentColor;
    stroke-width: 1.8;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.form-section-head.education .form-section-icon {
    background: #E8F7F5;
    color: #18A6A6;
}

.form-section-head.pede .form-section-icon {
    background: #F2EEFC;
    color: #8B73C7;
}

.form-section-head.academic .form-section-icon {
    background: #FFF5DF;
    color: #D99819;
}

.form-section-title {
    color: #073B63;
    font-size: 0.94rem;
    font-weight: 800;
    line-height: 1.2;
}

.form-section-subtitle {
    color: #718A9B;
    font-size: 0.74rem;
    margin-top: 0.18rem;
    line-height: 1.35;
}

/* Botão de cálculo: azul-petróleo sólido */
div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button,
div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button[kind="primary"],
div[data-testid="stForm"] button[data-testid="stBaseButton-primaryFormSubmit"] {
    min-height: 50px !important;
    background: #073B63 !important;
    background-color: #073B63 !important;
    color: #FFFFFF !important;
    border: 1px solid #073B63 !important;
    border-radius: 12px !important;
    box-shadow: 0 7px 18px rgba(7, 59, 99, 0.16) !important;
    font-weight: 800 !important;
    letter-spacing: 0.01em !important;
    transition: background-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease !important;
}

div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button *,
div[data-testid="stForm"] button[data-testid="stBaseButton-primaryFormSubmit"] * {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button:hover,
div[data-testid="stForm"] button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background: #0B5870 !important;
    background-color: #0B5870 !important;
    border-color: #0B5870 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
    box-shadow: 0 9px 22px rgba(7, 59, 99, 0.22) !important;
}

div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button:hover *,
div[data-testid="stForm"] button[data-testid="stBaseButton-primaryFormSubmit"]:hover * {
    color: #FFFFFF !important;
}

div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button:active,
div[data-testid="stForm"] button[data-testid="stBaseButton-primaryFormSubmit"]:active {
    background: #064B64 !important;
    background-color: #064B64 !important;
    transform: translateY(0);
}

/* Separação visual leve entre os grupos */
.form-group-space {
    height: 0.25rem;
}


div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.78);
    border: 1px solid #DDEAF0;
    border-radius: 18px;
    padding: 1.15rem 1.2rem 1.25rem 1.2rem;
    box-shadow: 0 7px 24px rgba(4, 55, 87, 0.025);
}

div[data-testid="stForm"] h4 {
    color: #073B63;
    font-weight: 800;
    margin-top: 0.15rem;
}

div[data-testid="stNumberInput"] input {
    border-radius: 10px;
}

div[data-testid="stNumberInput"]:focus-within input {
    border-color: #18A6A6;
}

/* Botão principal */
div[data-testid="stFormSubmitButton"] button {
    border-radius: 11px;
    font-weight: 750;
}

/* ======================================================
   CARDS DO RESULTADO
   ====================================================== */

.risk-result-card {
    --card-accent: #42A5D9;
    background: #FFFFFF;
    border: 1px solid #DDEAF0;
    border-top: 3px solid var(--card-accent);
    border-radius: 16px;
    padding: 1.15rem 1.25rem;
    min-height: 116px;
    box-shadow: 0 7px 24px rgba(4, 55, 87, 0.035);
}

.risk-result-label {
    color: #60798B;
    font-size: 0.77rem;
    margin-bottom: 0.45rem;
}

.risk-result-value {
    color: #073B63;
    font-size: 1.62rem;
    line-height: 1.15;
    font-weight: 800;
}

.risk-result-value-small {
    color: #073B63;
    font-size: 1.08rem;
    line-height: 1.28;
    font-weight: 800;
}

.risk-probability {
    --card-accent: #42A5D9;
}

.risk-status-attention {
    --card-accent: #F47C6C;
}

.risk-status-ok {
    --card-accent: #45B98C;
}

.risk-model {
    --card-accent: #8B73C7;
}

/* ======================================================
   REFERÊNCIA OPERACIONAL
   ====================================================== */

.threshold-note {
    background: #FFF9EC;
    border: 1px solid #F6D98C;
    border-left: 4px solid #F2B544;
    border-radius: 0 12px 12px 0;
    padding: 0.90rem 1rem;
    color: #665B43;
    font-size: 0.83rem;
    line-height: 1.55;
    margin-top: 0.9rem;
}

/* ======================================================
   CARDS DE EXPLICABILIDADE
   ====================================================== */

.factor-card {
    background: #FFFFFF;
    border: 1px solid #E1EBF0;
    border-left: 3px solid #8B73C7;
    border-radius: 13px;
    padding: 0.92rem 1rem;
    margin-bottom: 0.70rem;
    box-shadow: 0 4px 15px rgba(4, 55, 87, 0.025);
}

.factor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.55rem;
}

.factor-name {
    color: #073B63;
    font-weight: 750;
    font-size: 0.95rem;
}

.factor-direction-up {
    color: #D85E52;
    font-size: 0.78rem;
    font-weight: 700;
}

.factor-direction-down {
    color: #278C70;
    font-size: 0.78rem;
    font-weight: 700;
}

.factor-track {
    width: 100%;
    height: 9px;
    background: #EDF3F6;
    border-radius: 999px;
    overflow: hidden;
}

.factor-fill-up {
    height: 100%;
    background: #F47C6C;
    border-radius: 999px;
}

.factor-fill-down {
    height: 100%;
    background: #45B98C;
    border-radius: 999px;
}

.factor-value {
    color: #7890A0;
    font-size: 0.72rem;
    margin-top: 0.40rem;
}

/* ======================================================
   RESUMO DAS CONTRIBUIÇÕES
   ====================================================== */

.contribution-summary {
    background: #FFFFFF;
    border: 1px solid #DDEAF0;
    border-radius: 14px;
    padding: 1rem 1.05rem;
    min-height: 150px;
}

.contribution-summary-up {
    border-top: 3px solid #F47C6C;
}

.contribution-summary-down {
    border-top: 3px solid #45B98C;
}

.contribution-title {
    color: #073B63;
    font-weight: 800;
    font-size: 0.93rem;
    margin-bottom: 0.65rem;
}

.contribution-item {
    color: #527087;
    font-size: 0.84rem;
    line-height: 1.7;
}

/* ======================================================
   NOTA METODOLÓGICA
   ====================================================== */

.method-note {
    background: #F8F6FD;
    border-left: 4px solid #8B73C7;
    border-radius: 0 12px 12px 0;
    padding: 0.95rem 1rem;
    color: #4F6178;
    font-size: 0.84rem;
    line-height: 1.55;
    margin-top: 1rem;
}

/* ======================================================
   RESPONSIVIDADE
   ====================================================== */

@media (max-width: 900px) {
    .risk-result-card {
        min-height: auto;
    }

    .factor-header {
        align-items: flex-start;
        flex-direction: column;
        gap: 0.25rem;
    }
}


/* ======================================================
   CABEÇALHO COLORIDO DA PÁGINA
   ====================================================== */
.page-hero-soft {
    position: relative;
    overflow: hidden;
    border: 1px solid #F47C6C2E;
    border-radius: 18px;
    padding: 1.35rem 8.5rem 1.35rem 1.55rem;
    margin: 0.15rem 0 1.25rem 0;
    background:
        radial-gradient(circle at 96% 18%, #F47C6C1F 0 7%, transparent 7.5%),
        radial-gradient(circle at 91% 88%, #F47C6C12 0 15%, transparent 15.5%),
        linear-gradient(110deg, #FFF3F1 0%, #FFF7F5 58%, #FFFFFF 100%);
    box-shadow: 0 7px 24px rgba(7, 59, 99, 0.035);
}
.page-hero-soft::before {
    content: "";
    position: absolute;
    width: 145px;
    height: 145px;
    border-radius: 50%;
    left: -78px;
    top: -64px;
    background: #F47C6C12;
}
.page-hero-eyebrow {
    position: relative;
    z-index: 2;
    color: #E96C61;
    font-size: 0.73rem;
    font-weight: 850;
    letter-spacing: 0.17em;
    text-transform: uppercase;
    margin-bottom: 0.55rem;
}
.page-hero-eyebrow::after {
    content: "";
    display: block;
    width: 42px;
    height: 3px;
    margin-top: 0.42rem;
    border-radius: 999px;
    background: #F47C6C;
}
.page-hero-title {
    position: relative;
    z-index: 2;
    color: #073B63;
    font-size: clamp(2rem, 3vw, 2.75rem);
    line-height: 1.08;
    font-weight: 850;
    letter-spacing: -0.035em;
    margin-bottom: 0.55rem;
}
.page-hero-description {
    position: relative;
    z-index: 2;
    max-width: 900px;
    color: #526D80;
    font-size: 0.96rem;
    line-height: 1.55;
}
.page-hero-vector {
    position: absolute;
    z-index: 1;
    right: 2.2rem;
    top: 50%;
    transform: translateY(-50%);
    width: 78px;
    height: 78px;
    color: #F47C6C;
    opacity: 0.86;
}
.page-hero-vector svg {
    width: 100%;
    height: 100%;
    fill: none;
    stroke: currentColor;
    stroke-width: 1.65;
    stroke-linecap: round;
    stroke-linejoin: round;
}
@media (max-width: 900px) {
    .page-hero-soft {
        padding-right: 1.35rem;
    }
    .page-hero-vector {
        display: none;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# CARREGAMENTO DOS MODELOS
# ==========================================================

@st.cache_resource
def carregar_modelos():

    pasta_modelos = BASE_DIR / "models"

    return {
        "Risco futuro": {
            "modelo": joblib.load(
                pasta_modelos / "pipeline_risco_futuro.joblib"
            ),
            "explicativo": joblib.load(
                pasta_modelos
                / "pipeline_risco_futuro_explicativo.joblib"
            ),
        },

        "Nova incidência de defasagem": {
            "modelo": joblib.load(
                pasta_modelos
                / "pipeline_incidencia_nova_defasagem.joblib"
            ),
            "explicativo": joblib.load(
                pasta_modelos
                / "pipeline_incidencia_nova_defasagem_explicativo.joblib"
            ),
        },
    }


# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def cabecalho_formulario(titulo, subtitulo, tipo):
    """Cabeçalho visual com SVG vetorial para as subseções do formulário."""

    icones = {
        "education": """
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M4 10.5 12 6l8 4.5-8 4.5-8-4.5Z"/>
                <path d="M7 12.2V16c2.7 2 7.3 2 10 0v-3.8"/>
                <path d="M20 10.5V16"/>
            </svg>
        """,
        "pede": """
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M5 19V9"/>
                <path d="M10 19V5"/>
                <path d="M15 19v-7"/>
                <path d="M20 19V8"/>
                <path d="M3 19h19"/>
            </svg>
        """,
        "academic": """
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M4 5.5c3.2-.8 5.8-.3 8 1.5v12c-2.2-1.8-4.8-2.3-8-1.5v-12Z"/>
                <path d="M20 5.5c-3.2-.8-5.8-.3-8 1.5v12c2.2-1.8 4.8-2.3 8-1.5v-12Z"/>
            </svg>
        """,
    }

    html = (
        f'<div class="form-section-head {tipo}">'
        f'<div class="form-section-icon">{icones[tipo]}</div>'
        '<div>'
        f'<div class="form-section-title">{titulo}</div>'
        f'<div class="form-section-subtitle">{subtitulo}</div>'
        '</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def nome_feature(nome):

    mapa = {
        "FASE": "Fase atual",
        "FASE_IDEAL": "Fase ideal",
        "DEFASAGEM_CALCULADA": "Defasagem calculada",
        "IAN": "IAN",
        "IDA": "IDA",
        "IEG": "IEG",
        "IAA": "IAA",
        "IPS": "IPS",
        "IPV": "IPV",
        "NOTA_MATEMATICA": "Nota de Matemática",
        "NOTA_PORTUGUES": "Nota de Português",
        "NOTA_INGLES": "Nota de Inglês",
        "IDADE_ANOS": "Idade",
        "ANO_INGRESSO": "Ano de ingresso",
    }

    return mapa.get(nome, nome)


def card_resultado(
    label,
    valor,
    pequeno=False,
    classe_card="risk-probability",
):

    classe_valor = (
        "risk-result-value-small"
        if pequeno
        else "risk-result-value"
    )

    html = (
        f'<div class="risk-result-card {classe_card}">'
        f'<div class="risk-result-label">{label}</div>'
        f'<div class="{classe_valor}">{valor}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def mostrar_fator(item, maior_contribuicao):

    nome = nome_feature(item["feature"])

    contribuicao = float(
        item["contribuicao"]
    )

    percentual = (
        abs(contribuicao)
        / maior_contribuicao
        * 100
        if maior_contribuicao > 0
        else 0
    )

    if contribuicao > 0:

        classe_direcao = (
            "factor-direction-up"
        )

        classe_barra = (
            "factor-fill-up"
        )

        direcao = "↑ Aumenta o risco"

    else:

        classe_direcao = (
            "factor-direction-down"
        )

        classe_barra = (
            "factor-fill-down"
        )

        direcao = "↓ Reduz o risco"

    # IMPORTANTE:
    # HTML construído sem indentação para evitar que
    # o Streamlit interprete o conteúdo como bloco de código.

    html = (
        f'<div class="factor-card">'
        f'<div class="factor-header">'
        f'<span class="factor-name">{nome}</span>'
        f'<span class="{classe_direcao}">{direcao}</span>'
        f'</div>'
        f'<div class="factor-track">'
        f'<div class="{classe_barra}" '
        f'style="width:{percentual:.1f}%"></div>'
        f'</div>'
        f'<div class="factor-value">'
        f'Intensidade relativa da contribuição: '
        f'{percentual:.0f}%'
        f'</div>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ==========================================================
# CABEÇALHO
# ==========================================================

st.markdown(
    '<div class="page-hero-soft"><div class="page-hero-eyebrow">SOLUÇÃO PREDITIVA</div><div class="page-hero-title">Avaliação de risco de defasagem</div><div class="page-hero-description">Utilize os indicadores educacionais disponíveis para estimar a probabilidade de defasagem no período seguinte. A análise utiliza os modelos desenvolvidos a partir do histórico educacional do projeto.</div><div class="page-hero-vector"><svg viewBox="0 0 24 24"><circle cx="11" cy="13" r="7"></circle><circle cx="11" cy="13" r="3.5"></circle><path d="M13.5 10.5 21 3"></path><path d="M17 3h4v4"></path></svg></div></div>',
    unsafe_allow_html=True,
)

st.write("")


# ==========================================================
# 1. TIPO DE AVALIAÇÃO
# ==========================================================

st.subheader(
    "1. Tipo de avaliação"
)

tipo_modelo = st.radio(
    "Selecione o objetivo da análise:",
    [
        "Risco futuro",
        "Nova incidência de defasagem",
    ],
    horizontal=True,
)


if tipo_modelo == "Risco futuro":

    st.info(
        """
        **Risco futuro:** estima a probabilidade de o aluno
        apresentar defasagem no período seguinte considerando
        os indicadores disponíveis no período atual.
        """
    )

else:

    st.info(
        """
        **Nova incidência de defasagem:** estima a probabilidade
        de um aluno atualmente sem defasagem passar a apresentar
        defasagem no período seguinte.
        """
    )


st.divider()


# ==========================================================
# 2. INDICADORES DO ALUNO
# ==========================================================

st.subheader(
    "2. Indicadores do aluno"
)

st.caption(
    "Preencha os dados conhecidos no período atual. "
    "Nenhuma informação futura é utilizada na previsão."
)


with st.form(
    "formulario_risco"
):

    # ======================================================
    # SITUAÇÃO EDUCACIONAL
    # ======================================================

    cabecalho_formulario(
        "Situação educacional",
        "Contexto atual do aluno e relação com a fase educacional esperada.",
        "education",
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        fase = st.number_input(
            "Fase atual",
            min_value=0.0,
            max_value=9.0,
            value=3.0,
            step=1.0,
        )

    with col2:

        fase_ideal = st.number_input(
            "Fase ideal",
            min_value=0.0,
            max_value=9.0,
            value=3.0,
            step=1.0,
        )

    with col3:

        defasagem = st.number_input(
            "Defasagem calculada",
            min_value=-10.0,
            max_value=10.0,
            value=0.0,
            step=1.0,
            help=(
                "Diferença entre a situação observada "
                "e a fase educacional considerada ideal."
            ),
        )

    with col4:

        idade = st.number_input(
            "Idade",
            min_value=5,
            max_value=35,
            value=14,
            step=1,
        )


    st.write("")


    # ======================================================
    # INDICADORES PEDE
    # ======================================================

    cabecalho_formulario(
        "Indicadores PEDE",
        "Indicadores multidimensionais utilizados para caracterizar o acompanhamento educacional.",
        "pede",
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        ian = st.number_input(
            "IAN",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1,
            format="%.2f",
        )

        iaa = st.number_input(
            "IAA",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1,
            format="%.2f",
        )


    with col2:

        ida = st.number_input(
            "IDA",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1,
            format="%.2f",
        )

        ips = st.number_input(
            "IPS",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1,
            format="%.2f",
        )


    with col3:

        ieg = st.number_input(
            "IEG",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1,
            format="%.2f",
        )

        ipv = st.number_input(
            "IPV",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1,
            format="%.2f",
        )


    with col4:

        ano_ingresso = st.number_input(
            "Ano de ingresso",
            min_value=1990,
            max_value=2026,
            value=2020,
            step=1,
        )


    st.write("")


    # ======================================================
    # DESEMPENHO ACADÊMICO
    # ======================================================

    cabecalho_formulario(
        "Desempenho acadêmico",
        "Notas disponíveis de Matemática, Português e Inglês no período avaliado.",
        "academic",
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        nota_matematica = st.number_input(
            "Nota de Matemática",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1,
            format="%.2f",
        )


    with col2:

        nota_portugues = st.number_input(
            "Nota de Português",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1,
            format="%.2f",
        )


    with col3:

        nota_ingles = st.number_input(
            "Nota de Inglês",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1,
            format="%.2f",
        )


    st.write("")

    calcular = st.form_submit_button(
        "Calcular avaliação de risco",
        type="primary",
        use_container_width=True,
    )


# ==========================================================
# 3. PREVISÃO
# ==========================================================

if calcular:

    # ======================================================
    # VALIDAÇÃO DO MODELO DE NOVA INCIDÊNCIA
    # ======================================================

    if (
        tipo_modelo
        == "Nova incidência de defasagem"
        and defasagem < 0
    ):

        st.warning(
            """
            O modelo de **nova incidência de defasagem**
            foi desenvolvido para alunos que ainda não
            apresentavam defasagem no período utilizado
            para realizar a previsão.

            Para este perfil, utilize o modelo
            **Risco futuro**.
            """
        )

        st.stop()


    # ======================================================
    # DATAFRAME DE ENTRADA
    # ======================================================

    dados_aluno = pd.DataFrame(
        [
            {
                "FASE": fase,
                "FASE_IDEAL": fase_ideal,
                "DEFASAGEM_CALCULADA": defasagem,
                "IAN": ian,
                "IDA": ida,
                "IEG": ieg,
                "IAA": iaa,
                "IPS": ips,
                "IPV": ipv,
                "NOTA_MATEMATICA": nota_matematica,
                "NOTA_PORTUGUES": nota_portugues,
                "NOTA_INGLES": nota_ingles,
                "IDADE_ANOS": idade,
                "ANO_INGRESSO": ano_ingresso,
            }
        ],
        columns=list(
            FEATURES_NUMERICAS
        ),
    )


    try:

        # ==================================================
        # CARREGAR MODELOS
        # ==================================================

        modelos = carregar_modelos()

        modelo = (
            modelos[tipo_modelo]["modelo"]
        )

        modelo_explicativo = (
            modelos[tipo_modelo]["explicativo"]
        )


        # ==================================================
        # PROBABILIDADE
        # ==================================================

        probabilidade = float(
            modelo.predict_proba(
                dados_aluno
            )[0][1]
        )

        sinalizado = (
            probabilidade
            >= LIMIAR_REFERENCIA
        )


        # ==================================================
        # RESULTADO
        # ==================================================

        st.divider()

        st.subheader(
            "3. Resultado da avaliação"
        )

        col1, col2, col3 = st.columns(
            [1, 1, 1.35]
        )


        with col1:

            card_resultado(
                "Probabilidade estimada",
                f"{probabilidade:.1%}",
            )


        with col2:

            if sinalizado:

                status = "Atenção"
                classe_status = "risk-status-attention"

            else:

                status = "Não sinalizado"
                classe_status = "risk-status-ok"

            card_resultado(
                "Classificação de referência",
                status,
                pequeno=True,
            )


        with col3:

            card_resultado(
                "Modelo utilizado",
                tipo_modelo,
                pequeno=True,
                classe_card="risk-model",
            )


        # ==================================================
        # REFERÊNCIA OPERACIONAL
        # ==================================================

        st.markdown(
            (
                '<div class="threshold-note">'
                '<strong>Referência operacional:</strong> '
                f'o ponto de corte de {LIMIAR_REFERENCIA:.0%} '
                'é utilizado nesta página apenas para transformar '
                'a probabilidade em uma sinalização de referência. '
                'Ele não representa um limiar de produção definido '
                'pela instituição.'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

        # ==================================================
        # INTERPRETAÇÃO
        # ==================================================

        if sinalizado:

            st.warning(
                f"""
                **O perfil foi sinalizado para atenção pelo
                limiar de referência de
                {LIMIAR_REFERENCIA:.0%}.**

                A probabilidade estimada pelo modelo foi de
                **{probabilidade:.1%}**.

                O resultado pode apoiar a priorização de
                acompanhamento, mas deve ser interpretado
                em conjunto com a análise da equipe.
                """
            )

        else:

            st.success(
                f"""
                **O perfil não foi sinalizado pelo limiar de
                referência de
                {LIMIAR_REFERENCIA:.0%}.**

                A probabilidade estimada pelo modelo foi de
                **{probabilidade:.1%}**.

                Isso não elimina a necessidade de
                acompanhamento dos indicadores educacionais
                ao longo do tempo.
                """
            )


        # ==================================================
        # 4. EXPLICABILIDADE
        # ==================================================

        st.write("")

        st.subheader(
            "4. Fatores que mais influenciaram a previsão"
        )

        st.caption(
            "As barras representam a intensidade relativa "
            "das principais contribuições individuais. "
            "Elas ajudam a interpretar a direção da previsão, "
            "mas não devem ser lidas como causalidade."
        )


        explicacoes = explicar_previsao(
            modelo_explicativo,
            dados_aluno,
            top_n=5,
        )


        if explicacoes:

            maior_contribuicao = max(
                abs(
                    float(
                        item["contribuicao"]
                    )
                )
                for item in explicacoes
            )

            for item in explicacoes:

                mostrar_fator(
                    item,
                    maior_contribuicao,
                )


            # ==============================================
            # RESUMO DAS CONTRIBUIÇÕES
            # ==============================================

            aumentam = [
                nome_feature(
                    item["feature"]
                )
                for item in explicacoes
                if float(
                    item["contribuicao"]
                ) > 0
            ]

            reduzem = [
                nome_feature(
                    item["feature"]
                )
                for item in explicacoes
                if float(
                    item["contribuicao"]
                ) < 0
            ]


            col1, col2 = st.columns(2)

            with col1:

                itens_aumentam = (
                    "".join(
                        f'<div class="contribution-item">• {item}</div>'
                        for item in aumentam
                    )
                    if aumentam
                    else (
                        '<div class="contribution-item">'
                        'Nenhum dos cinco principais fatores.'
                        '</div>'
                    )
                )

                st.markdown(
                    (
                        '<div class="contribution-summary '
                        'contribution-summary-up">'
                        '<div class="contribution-title">'
                        'Pressionaram o risco para cima'
                        '</div>'
                        f'{itens_aumentam}'
                        '</div>'
                    ),
                    unsafe_allow_html=True,
                )


            with col2:

                itens_reduzem = (
                    "".join(
                        f'<div class="contribution-item">• {item}</div>'
                        for item in reduzem
                    )
                    if reduzem
                    else (
                        '<div class="contribution-item">'
                        'Nenhum dos cinco principais fatores.'
                        '</div>'
                    )
                )

                st.markdown(
                    (
                        '<div class="contribution-summary '
                        'contribution-summary-down">'
                        '<div class="contribution-title">'
                        'Pressionaram o risco para baixo'
                        '</div>'
                        f'{itens_reduzem}'
                        '</div>'
                    ),
                    unsafe_allow_html=True,
                )


        else:

            st.info(
                "Não foram retornadas contribuições "
                "individuais para esta previsão."
            )


        # ==================================================
        # DADOS UTILIZADOS
        # ==================================================

        st.write("")

        with st.expander(
            "Ver dados utilizados na previsão"
        ):

            dados_exibicao = (
                dados_aluno.copy()
            )

            dados_exibicao.columns = [
                nome_feature(coluna)
                for coluna
                in dados_exibicao.columns
            ]

            st.dataframe(
                dados_exibicao,
                use_container_width=True,
                hide_index=True,
            )


        # ==================================================
        # NOTA METODOLÓGICA
        # ==================================================

        nota_metodologica = (
            '<div class="method-note">'
            '<strong>Como interpretar:</strong> '
            'a probabilidade é a saída do modelo preditivo. '
            f'O limiar de {LIMIAR_REFERENCIA:.0%} é '
            'apresentado apenas como uma referência '
            'operacional para transformar a probabilidade '
            'em uma sinalização binária. '
            'O projeto não definiu um limiar de produção '
            'com base em uma regra de negócio. '
            'A escolha definitiva deve considerar o custo '
            'de falsos positivos, falsos negativos e a '
            'capacidade de acompanhamento da instituição.'
            '</div>'
        )

        st.markdown(
            nota_metodologica,
            unsafe_allow_html=True,
        )

        st.caption(
            "O modelo identifica associações existentes "
            "nos dados históricos. As contribuições "
            "apresentadas explicam a previsão estatística "
            "individual e não representam relações causais."
        )


    # ======================================================
    # TRATAMENTO DE ERROS
    # ======================================================

    except FileNotFoundError:

        st.error(
            """
            Não foi possível localizar os arquivos dos
            modelos na pasta `models/`.

            Verifique se os arquivos `.joblib` estão
            disponíveis antes de executar a aplicação.
            """
        )


    except Exception as erro:

        st.error(
            "Não foi possível realizar a previsão."
        )

        st.exception(
            erro
        )