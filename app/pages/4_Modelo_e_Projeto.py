from pathlib import Path

import streamlit as st

from utils.styles import aplicar_estilo


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Modelo & Projeto | Passos Mágicos",
    layout="wide",
)

aplicar_estilo()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ==========================================================
# PALETA DA PÁGINA
# ==========================================================

CORES = {
    "navy": "#073B63",
    "teal": "#18A6A6",
    "teal_soft": "#E7F8F7",

    "sky": "#42A5D9",
    "sky_soft": "#EDF7FC",

    "green": "#45B98C",
    "green_soft": "#EDF9F3",

    "amber": "#F2B544",
    "amber_soft": "#FFF8E8",

    "purple": "#8B73C7",
    "purple_soft": "#F4F0FB",

    "coral": "#F47C6C",
    "coral_soft": "#FFF1EE",

    "border": "#DDEAF0",
    "text": "#526D80",
}


# ==========================================================
# ÍCONES SVG
# ==========================================================

ICONS = {

    "target": """
        <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="8"></circle>
            <circle cx="12" cy="12" r="4"></circle>
            <circle cx="12" cy="12" r="1"></circle>
            <path d="M14.5 9.5L21 3"></path>
            <path d="M17 3h4v4"></path>
        </svg>
    """,

    "database": """
        <svg viewBox="0 0 24 24">
            <ellipse cx="12" cy="5" rx="7" ry="3"></ellipse>
            <path d="M5 5v6c0 1.7 3.1 3 7 3s7-1.3 7-3V5"></path>
            <path d="M5 11v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"></path>
        </svg>
    """,

    "settings": """
        <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6V21h-4v-.1a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1L4.2 17l.1-.1a1.7 1.7 0 0 0 .3-1.9A1.7 1.7 0 0 0 3 14H3v-4h.1a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9L4.2 7 7 4.2l.1.1A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-1.6V3h4v.1a1.7 1.7 0 0 0 1 1.6 1.7 1.7 0 0 0 1.9-.3l.1-.1L19.8 7l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.6 1h.1v4H21a1.7 1.7 0 0 0-1.6 1z"></path>
        </svg>
    """,

    "chart": """
        <svg viewBox="0 0 24 24">
            <path d="M4 20V10"></path>
            <path d="M10 20V4"></path>
            <path d="M16 20v-7"></path>
            <path d="M22 20V7"></path>
        </svg>
    """,

    "network": """
        <svg viewBox="0 0 24 24">
            <circle cx="12" cy="5" r="2"></circle>
            <circle cx="5" cy="18" r="2"></circle>
            <circle cx="19" cy="18" r="2"></circle>
            <path d="M11 7 6 16"></path>
            <path d="m13 7 5 9"></path>
            <path d="M7 18h10"></path>
        </svg>
    """,

    "document": """
        <svg viewBox="0 0 24 24">
            <path d="M6 3h9l3 3v15H6z"></path>
            <path d="M15 3v4h4"></path>
            <path d="M9 11h6"></path>
            <path d="M9 15h6"></path>
        </svg>
    """,

    "search": """
        <svg viewBox="0 0 24 24">
            <circle cx="10.5" cy="10.5" r="6.5"></circle>
            <path d="m15.5 15.5 5 5"></path>
        </svg>
    """,

    "clock": """
        <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="9"></circle>
            <path d="M12 7v6l4 2"></path>
        </svg>
    """,

    "users": """
        <svg viewBox="0 0 24 24">
            <circle cx="9" cy="8" r="3"></circle>
            <path d="M3 20v-2c0-3 2.7-5 6-5s6 2 6 5v2"></path>
            <circle cx="17" cy="9" r="2.5"></circle>
            <path d="M16 14c3.1 0 5 1.8 5 4.5V20"></path>
        </svg>
    """,

    "eye": """
        <svg viewBox="0 0 24 24">
            <path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"></path>
            <circle cx="12" cy="12" r="2.5"></circle>
        </svg>
    """,

    "shield": """
        <svg viewBox="0 0 24 24">
            <path d="M12 3 19 6v5c0 4.5-2.7 8-7 10-4.3-2-7-5.5-7-10V6z"></path>
            <path d="m9 12 2 2 4-4"></path>
        </svg>
    """,

    "refresh": """
        <svg viewBox="0 0 24 24">
            <path d="M20 7v5h-5"></path>
            <path d="M4 17v-5h5"></path>
            <path d="M6.1 8A7 7 0 0 1 18 7l2 5"></path>
            <path d="M17.9 16A7 7 0 0 1 6 17l-2-5"></path>
        </svg>
    """,

    "code": """
        <svg viewBox="0 0 24 24">
            <path d="m8 9-4 3 4 3"></path>
            <path d="m16 9 4 3-4 3"></path>
            <path d="m14 5-4 14"></path>
        </svg>
    """,

    "layers": """
        <svg viewBox="0 0 24 24">
            <path d="m12 3 9 5-9 5-9-5z"></path>
            <path d="m3 12 9 5 9-5"></path>
            <path d="m3 16 9 5 9-5"></path>
        </svg>
    """,

    "monitor": """
        <svg viewBox="0 0 24 24">
            <rect x="3" y="4" width="18" height="13" rx="2"></rect>
            <path d="M8 21h8"></path>
            <path d="M12 17v4"></path>
        </svg>
    """,

    "table": """
        <svg viewBox="0 0 24 24">
            <rect x="3" y="4" width="18" height="16" rx="2"></rect>
            <path d="M3 9h18"></path>
            <path d="M9 9v11"></path>
        </svg>
    """,
}


# ==========================================================
# CSS DA PÁGINA
# ==========================================================

st.markdown(
    """
<style>

/* ======================================================
   SVG
   ====================================================== */

.vector-icon,
.pipeline-icon {
    display: flex;
    align-items: center;
    justify-content: center;
}

.vector-icon svg,
.pipeline-icon svg {
    width: 100%;
    height: 100%;
    fill: none;
    stroke: currentColor;
    stroke-width: 1.7;
    stroke-linecap: round;
    stroke-linejoin: round;
}


/* ======================================================
   DESTAQUES
   ====================================================== */

.project-highlight {
    border-radius: 16px;
    padding: 1.15rem 1.25rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    border: 1px solid #DDEAF0;
}

.project-highlight .vector-icon {
    width: 43px;
    height: 43px;
    flex: 0 0 43px;
}

.project-highlight-content {
    color: #4F6B80;
    font-size: 0.86rem;
    line-height: 1.6;
}

.project-highlight-content strong {
    color: #073B63;
}

.highlight-teal {
    background: linear-gradient(135deg, #E7F8F7, #FFFFFF);
    border-color: #C9EAE7;
}

.highlight-teal .vector-icon {
    color: #18A6A6;
}

.highlight-sky {
    background: linear-gradient(135deg, #EDF7FC, #FFFFFF);
    border-color: #D2E9F4;
}

.highlight-sky .vector-icon {
    color: #42A5D9;
}

.highlight-purple {
    background: linear-gradient(135deg, #F4F0FB, #FFFFFF);
    border-color: #DDD4F1;
}

.highlight-purple .vector-icon {
    color: #8B73C7;
}


/* ======================================================
   PIPELINE
   ====================================================== */

.pipeline-box {
    background: #FFFFFF;
    border: 1px solid #DDEAF0;
    border-top: 4px solid var(--accent);
    border-radius: 15px;
    padding: 1rem 0.65rem;
    text-align: center;
    min-height: 188px;
    height: 100%;
    box-shadow: 0 5px 16px rgba(4, 55, 87, 0.03);
}

.pipeline-icon-wrap {
    width: 50px;
    height: 50px;
    margin: 0 auto 0.65rem auto;
    border-radius: 14px;
    background: var(--soft);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
}

.pipeline-icon {
    width: 30px;
    height: 30px;
}

.pipeline-title {
    color: #073B63;
    font-weight: 800;
    font-size: 0.86rem;
}

.pipeline-text {
    color: #718898;
    font-size: 0.69rem;
    line-height: 1.4;
    margin-top: 0.4rem;
}

.pipeline-number {
    width: 27px;
    height: 27px;
    margin: 0.7rem auto 0 auto;
    border-radius: 50%;
    background: var(--soft);
    color: var(--accent);
    font-size: 0.73rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
}


/* ======================================================
   FEATURE TAGS
   ====================================================== */

.feature-tag {
    display: inline-block;
    padding: 0.38rem 0.72rem;
    margin: 0.2rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 650;
    border: 1px solid;
}

.feature-sky {
    background: #EDF7FC;
    border-color: #D2E9F4;
    color: #27789F;
}

.feature-green {
    background: #EDF9F3;
    border-color: #D1ECDD;
    color: #287A60;
}

.feature-amber {
    background: #FFF8E8;
    border-color: #F0DFB7;
    color: #9A6A12;
}

.feature-purple {
    background: #F4F0FB;
    border-color: #DDD4F0;
    color: #6850A4;
}

.feature-coral {
    background: #FFF1EE;
    border-color: #F4D4CE;
    color: #B9574D;
}

.feature-teal {
    background: #E7F8F7;
    border-color: #CBEAE7;
    color: #087D79;
}


/* ======================================================
   CARDS
   ====================================================== */

.project-card {
    background: #FFFFFF;
    border: 1px solid #DDEAF0;
    border-top: 4px solid var(--accent);
    border-radius: 16px;
    padding: 1.15rem 1.2rem;
    min-height: 175px;
    height: 100%;
    box-shadow: 0 5px 18px rgba(4, 55, 87, 0.035);
}

.project-card-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.7rem;
}

.project-icon-wrap {
    width: 43px;
    height: 43px;
    flex: 0 0 43px;
    border-radius: 13px;
    background: var(--soft);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
}

.project-icon-wrap .vector-icon {
    width: 26px;
    height: 26px;
}

.project-card-title {
    color: #073B63;
    font-size: 1rem;
    font-weight: 800;
}

.project-card-text {
    color: #526D80;
    font-size: 0.84rem;
    line-height: 1.55;
}


/* ======================================================
   MÉTRICAS
   ====================================================== */

.model-metric {
    position: relative;
    overflow: hidden;
    background: #FFFFFF;
    border: 1px solid #DDEAF0;
    border-radius: 16px;
    padding: 1.15rem 1.2rem;
    min-height: 150px;
}

.model-metric::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 4px;
    background: var(--accent);
}

.model-metric-label {
    color: #6A8293;
    font-size: 0.76rem;
    margin-bottom: 0.35rem;
}

.model-metric-value {
    color: var(--accent);
    font-size: 1.9rem;
    font-weight: 800;
    line-height: 1.1;
}

.model-metric-detail {
    color: #718898;
    font-size: 0.75rem;
    margin-top: 0.5rem;
    line-height: 1.4;
}


/* ======================================================
   LIMIAR
   ====================================================== */

.decision-box {
    background:
        linear-gradient(
            135deg,
            #FFF8E8 0%,
            #FFFFFF 75%
        );

    border: 1px solid #F0DFB7;
    border-left: 4px solid #F2B544;

    border-radius: 0 14px 14px 0;

    padding: 1rem 1.15rem;

    color: #665B43;

    font-size: 0.84rem;
    line-height: 1.6;
}


/* ======================================================
   TECNOLOGIAS
   ====================================================== */

.stack-card {
    background: #FFFFFF;
    border: 1px solid #DDEAF0;
    border-top: 4px solid var(--accent);
    border-radius: 16px;
    padding: 1rem;
    min-height: 158px;
}

.stack-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.65rem;
}

.stack-icon {
    width: 39px;
    height: 39px;
    flex: 0 0 39px;
    border-radius: 12px;
    background: var(--soft);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
}

.stack-icon .vector-icon {
    width: 24px;
    height: 24px;
}

.stack-title {
    color: #073B63;
    font-weight: 800;
    font-size: 0.95rem;
}

.stack-text {
    color: #667E8F;
    font-size: 0.78rem;
    line-height: 1.5;
}


/* ======================================================
   CABEÇALHO COLORIDO DA PÁGINA
   ====================================================== */
.page-hero-soft {
    position: relative;
    overflow: hidden;
    border: 1px solid #8B73C72E;
    border-radius: 18px;
    padding: 1.35rem 8.5rem 1.35rem 1.55rem;
    margin: 0.15rem 0 1.25rem 0;
    background:
        radial-gradient(circle at 96% 18%, #8B73C71F 0 7%, transparent 7.5%),
        radial-gradient(circle at 91% 88%, #8B73C712 0 15%, transparent 15.5%),
        linear-gradient(110deg, #F4F0FB 0%, #F8F6FD 58%, #FFFFFF 100%);
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
    background: #8B73C712;
}
.page-hero-eyebrow {
    position: relative;
    z-index: 2;
    color: #745DB5;
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
    background: #8B73C7;
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
    color: #8B73C7;
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
# FUNÇÕES
# ==========================================================

def svg_icon(nome):
    return (
        '<div class="vector-icon">'
        f'{ICONS[nome]}'
        '</div>'
    )


def projeto_card(
    titulo,
    texto,
    icone,
    cor,
    soft,
):
    html = (
        f'<div class="project-card" '
        f'style="--accent:{cor}; --soft:{soft};">'
        '<div class="project-card-header">'
        '<div class="project-icon-wrap">'
        f'{svg_icon(icone)}'
        '</div>'
        f'<div class="project-card-title">{titulo}</div>'
        '</div>'
        f'<div class="project-card-text">{texto}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def etapa_pipeline(
    numero,
    titulo,
    texto,
    icone,
    cor,
    soft,
):
    html = (
        f'<div class="pipeline-box" '
        f'style="--accent:{cor}; --soft:{soft};">'
        '<div class="pipeline-icon-wrap">'
        '<div class="pipeline-icon">'
        f'{ICONS[icone]}'
        '</div>'
        '</div>'
        f'<div class="pipeline-title">{titulo}</div>'
        f'<div class="pipeline-text">{texto}</div>'
        f'<div class="pipeline-number">{numero}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def metrica_modelo(
    titulo,
    valor,
    detalhe,
    cor,
):
    html = (
        f'<div class="model-metric" '
        f'style="--accent:{cor};">'
        f'<div class="model-metric-label">{titulo}</div>'
        f'<div class="model-metric-value">{valor}</div>'
        f'<div class="model-metric-detail">{detalhe}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def stack_card(
    titulo,
    texto,
    icone,
    cor,
    soft,
):
    html = (
        f'<div class="stack-card" '
        f'style="--accent:{cor}; --soft:{soft};">'
        '<div class="stack-header">'
        '<div class="stack-icon">'
        f'{svg_icon(icone)}'
        '</div>'
        f'<div class="stack-title">{titulo}</div>'
        '</div>'
        f'<div class="stack-text">{texto}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ==========================================================
# CABEÇALHO
# ==========================================================

st.markdown(
    '<div class="page-hero-soft"><div class="page-hero-eyebrow">METODOLOGIA & MACHINE LEARNING</div><div class="page-hero-title">Modelo & Projeto</div><div class="page-hero-description">Conheça a arquitetura analítica, a estratégia de modelagem e os principais critérios utilizados na construção da solução preditiva para acompanhamento da defasagem educacional.</div><div class="page-hero-vector"><svg viewBox="0 0 24 24"><path d="M6 3h9l3 3v15H6z"></path><path d="M15 3v4h4"></path><path d="M9 11h6"></path><path d="M9 15h6"></path></svg></div></div>',
    unsafe_allow_html=True,
)

st.write("")


# ==========================================================
# 1. O DESAFIO
# ==========================================================

st.subheader("1. O desafio")

html_desafio = (
    '<div class="project-highlight highlight-teal">'
    f'{svg_icon("target")}'
    '<div class="project-highlight-content">'
    '<strong>'
    'Como utilizar os dados históricos para apoiar a identificação '
    'antecipada de alunos com maior probabilidade de apresentar '
    'defasagem educacional?'
    '</strong>'
    '<br><br>'
    'A solução foi estruturada para transformar indicadores '
    'educacionais em informação analítica, combinando análise '
    'histórica, modelagem preditiva e explicabilidade. '
    'O objetivo não é substituir a avaliação da equipe pedagógica, '
    'mas oferecer uma camada adicional de apoio ao acompanhamento '
    'dos alunos.'
    '</div>'
    '</div>'
)

st.markdown(
    html_desafio,
    unsafe_allow_html=True,
)

st.write("")


# ==========================================================
# 2. COMO A SOLUÇÃO FUNCIONA
# ==========================================================

st.subheader("2. Como a solução funciona")

st.caption(
    "Fluxo simplificado da informação até a geração da previsão."
)

colunas = st.columns(6)

etapas = [
    (
        "1",
        "Dados",
        "Histórico educacional e indicadores PEDE.",
        "database",
        CORES["sky"],
        CORES["sky_soft"],
    ),
    (
        "2",
        "Preparação",
        "Limpeza, padronização e estrutura longitudinal.",
        "settings",
        CORES["green"],
        CORES["green_soft"],
    ),
    (
        "3",
        "Features",
        "Construção das variáveis disponíveis no período atual.",
        "chart",
        CORES["amber"],
        CORES["amber_soft"],
    ),
    (
        "4",
        "Modelo",
        "Pipeline de machine learning treinado no histórico.",
        "network",
        CORES["purple"],
        CORES["purple_soft"],
    ),
    (
        "5",
        "Probabilidade",
        "Estimativa individual de risco para o período seguinte.",
        "document",
        CORES["coral"],
        CORES["coral_soft"],
    ),
    (
        "6",
        "Explicação",
        "Identificação dos fatores associados à previsão.",
        "search",
        CORES["teal"],
        CORES["teal_soft"],
    ),
]

for coluna, etapa in zip(
    colunas,
    etapas,
):
    with coluna:
        etapa_pipeline(
            numero=etapa[0],
            titulo=etapa[1],
            texto=etapa[2],
            icone=etapa[3],
            cor=etapa[4],
            soft=etapa[5],
        )

st.write("")


# ==========================================================
# 3. VARIÁVEIS
# ==========================================================

st.subheader(
    "3. Variáveis utilizadas pelo modelo"
)

st.caption(
    "As previsões utilizam somente informações disponíveis "
    "no momento da avaliação."
)

features = [
    ("Fase atual", "feature-sky"),
    ("Fase ideal", "feature-sky"),
    ("Defasagem calculada", "feature-coral"),

    ("IAN", "feature-teal"),
    ("IDA", "feature-teal"),
    ("IEG", "feature-teal"),
    ("IAA", "feature-teal"),
    ("IPS", "feature-teal"),
    ("IPV", "feature-teal"),

    ("Nota de Matemática", "feature-amber"),
    ("Nota de Português", "feature-amber"),
    ("Nota de Inglês", "feature-amber"),

    ("Idade", "feature-purple"),
    ("Ano de ingresso", "feature-green"),
]

html_features = "".join(
    (
        f'<span class="feature-tag {classe}">'
        f'{feature}'
        '</span>'
    )
    for feature, classe in features
)

st.markdown(
    html_features,
    unsafe_allow_html=True,
)

st.write("")


# ==========================================================
# 4. ESTRATÉGIA PREDITIVA
# ==========================================================

st.subheader("4. Estratégia preditiva")

col1, col2 = st.columns(2)


with col1:

    projeto_card(
        titulo="Risco futuro",
        icone="chart",
        cor=CORES["purple"],
        soft=CORES["purple_soft"],
        texto=(
            "Estima a probabilidade de o aluno apresentar "
            "defasagem no período seguinte utilizando os "
            "indicadores conhecidos no período atual."
            "<br><br>"
            "Esse modelo permite avaliar o risco futuro de "
            "forma mais abrangente dentro da população "
            "elegível para a análise."
        ),
    )


with col2:

    projeto_card(
        titulo="Nova incidência de defasagem",
        icone="users",
        cor=CORES["coral"],
        soft=CORES["coral_soft"],
        texto=(
            "Foca nos alunos que ainda não apresentavam "
            "defasagem no período atual e estima a "
            "probabilidade de surgimento de uma nova "
            "ocorrência no período seguinte."
            "<br><br>"
            "Essa abordagem permite analisar especificamente "
            "o início do problema."
        ),
    )


st.write("")


# ==========================================================
# 5. VALIDAÇÃO TEMPORAL
# ==========================================================

st.subheader("5. Validação temporal")

html_validacao = (
    '<div class="project-highlight highlight-sky">'
    f'{svg_icon("clock")}'
    '<div class="project-highlight-content">'
    '<strong>'
    'O tempo foi respeitado durante a validação.'
    '</strong>'
    '<br><br>'
    'Em vez de embaralhar aleatoriamente observações de '
    'diferentes períodos, a avaliação foi estruturada '
    'considerando a sequência temporal dos dados. '
    'Informações de períodos anteriores são utilizadas '
    'para prever acontecimentos posteriores.'
    '<br><br>'
    'Essa estratégia reduz o risco de '
    '<em>data leakage</em> e representa melhor o cenário '
    'real de utilização da solução.'
    '</div>'
    '</div>'
)

st.markdown(
    html_validacao,
    unsafe_allow_html=True,
)

st.write("")


# ==========================================================
# 6. DESEMPENHO
# ==========================================================

st.subheader("6. Desempenho dos modelos")

st.caption(
    "ROC-AUC mede a capacidade do modelo de ordenar casos "
    "positivos acima de casos negativos ao longo de diferentes "
    "limiares de classificação."
)

col1, col2, col3 = st.columns(3)


with col1:

    metrica_modelo(
        titulo="ROC-AUC • Risco futuro",
        valor="0,831",
        detalhe=(
            "Desempenho registrado na avaliação temporal "
            "do modelo de risco futuro."
        ),
        cor=CORES["purple"],
    )


with col2:

    metrica_modelo(
        titulo="ROC-AUC • Nova incidência",
        valor="0,693",
        detalhe=(
            "Desempenho registrado na avaliação temporal "
            "do modelo de nova incidência de defasagem."
        ),
        cor=CORES["coral"],
    )


with col3:

    metrica_modelo(
        titulo="Variáveis de entrada",
        valor="14",
        detalhe=(
            "Indicadores utilizados para gerar a "
            "probabilidade individual."
        ),
        cor=CORES["teal"],
    )


st.info(
    """
**Como interpretar o ROC-AUC?**

Quanto maior o valor, maior a capacidade de discriminação
entre os dois grupos ao longo dos diferentes limiares.
A métrica não define, sozinha, qual deve ser o ponto de corte
utilizado operacionalmente.
"""
)


# ==========================================================
# 7. EXPLICABILIDADE
# ==========================================================

st.subheader("7. Explicabilidade")

col1, col2, col3 = st.columns(3)


with col1:

    projeto_card(
        titulo="Probabilidade",
        icone="document",
        cor=CORES["coral"],
        soft=CORES["coral_soft"],
        texto=(
            "O modelo produz uma probabilidade individual "
            "associada ao evento analisado, em vez de "
            "apresentar somente uma classificação final."
        ),
    )


with col2:

    projeto_card(
        titulo="Contribuições",
        icone="chart",
        cor=CORES["green"],
        soft=CORES["green_soft"],
        texto=(
            "A aplicação apresenta os fatores que mais "
            "contribuíram para aumentar ou reduzir a previsão "
            "produzida para aquele perfil."
        ),
    )


with col3:

    projeto_card(
        titulo="Interpretação responsável",
        icone="eye",
        cor=CORES["purple"],
        soft=CORES["purple_soft"],
        texto=(
            "As contribuições explicam o comportamento "
            "estatístico do modelo. Elas representam "
            "associações aprendidas nos dados e não devem "
            "ser interpretadas como relações causais."
        ),
    )


st.write("")


# ==========================================================
# 8. PROBABILIDADE X DECISÃO
# ==========================================================

st.subheader("8. Probabilidade x decisão")

st.markdown(
    """
<div class="decision-box">
<strong>
O modelo estima probabilidade; a decisão sobre o ponto de corte
é uma escolha operacional.
</strong>
<br><br>

Na página de Avaliação de Risco, 50% é utilizado apenas como
<strong>limiar de referência</strong> para facilitar a demonstração
da sinalização binária.

O projeto não assume esse valor como um limiar definitivo de
produção. A escolha de um ponto de corte deve considerar fatores
como capacidade de atendimento, custo de falsos positivos,
consequências de falsos negativos e objetivos da instituição.
</div>
""",
    unsafe_allow_html=True,
)

st.write("")


# ==========================================================
# 9. LIMITAÇÕES
# ==========================================================

st.subheader("9. Limitações e cuidados")

col1, col2 = st.columns(2)


with col1:

    projeto_card(
        titulo="Dados históricos",
        icone="database",
        cor=CORES["sky"],
        soft=CORES["sky_soft"],
        texto=(
            "O modelo aprende padrões presentes no histórico "
            "disponível. Mudanças na população, no processo "
            "educacional ou na forma de coleta podem alterar "
            "seu desempenho ao longo do tempo."
        ),
    )

    st.write("")

    projeto_card(
        titulo="Apoio à análise",
        icone="shield",
        cor=CORES["green"],
        soft=CORES["green_soft"],
        texto=(
            "A previsão deve apoiar o acompanhamento e a "
            "priorização de análises. Ela não substitui a "
            "avaliação pedagógica, social ou individual "
            "realizada pelos profissionais responsáveis."
        ),
    )


with col2:

    projeto_card(
        titulo="Monitoramento",
        icone="refresh",
        cor=CORES["amber"],
        soft=CORES["amber_soft"],
        texto=(
            "Em um cenário de produção, o desempenho deve "
            "ser acompanhado periodicamente para identificar "
            "mudanças na distribuição dos dados e eventual "
            "necessidade de reavaliação do modelo."
        ),
    )

    st.write("")

    projeto_card(
        titulo="Associação não é causalidade",
        icone="search",
        cor=CORES["coral"],
        soft=CORES["coral_soft"],
        texto=(
            "Uma variável contribuir para determinada previsão "
            "não significa que ela seja a causa da defasagem. "
            "A explicabilidade descreve o comportamento do "
            "modelo, não uma relação causal."
        ),
    )


st.write("")


# ==========================================================
# 10. TECNOLOGIAS
# ==========================================================

st.subheader("10. Tecnologias utilizadas")

col1, col2, col3, col4 = st.columns(4)


with col1:

    stack_card(
        titulo="Python",
        icone="code",
        cor=CORES["sky"],
        soft=CORES["sky_soft"],
        texto=(
            "Preparação dos dados, análise, engenharia "
            "de features e integração da solução."
        ),
    )


with col2:

    stack_card(
        titulo="scikit-learn",
        icone="network",
        cor=CORES["purple"],
        soft=CORES["purple_soft"],
        texto=(
            "Pipelines de machine learning, treinamento, "
            "inferência e avaliação dos modelos."
        ),
    )


with col3:

    stack_card(
        titulo="Pandas",
        icone="table",
        cor=CORES["amber"],
        soft=CORES["amber_soft"],
        texto=(
            "Manipulação, transformação e estruturação "
            "dos dados analíticos."
        ),
    )


with col4:

    stack_card(
        titulo="Streamlit",
        icone="monitor",
        cor=CORES["coral"],
        soft=CORES["coral_soft"],
        texto=(
            "Interface analítica, dashboard e "
            "disponibilização da solução preditiva."
        ),
    )


st.write("")


# ==========================================================
# 11. DA ANÁLISE À APLICAÇÃO
# ==========================================================

st.subheader("11. Da análise à aplicação")

html_entrega = (
    '<div class="project-highlight highlight-purple">'
    f'{svg_icon("layers")}'
    '<div class="project-highlight-content">'
    'A entrega integra '
    '<strong>'
    'análise exploratória, visão longitudinal, '
    'machine learning e aplicação interativa'
    '</strong> '
    'em uma única solução.'
    '<br><br>'
    'O Dashboard permite compreender os padrões observados '
    'no histórico, enquanto a Avaliação de Risco utiliza os '
    'modelos treinados para produzir previsões individuais '
    'acompanhadas de elementos de explicabilidade.'
    '<br><br>'
    'Dessa forma, o projeto conecta a investigação dos dados '
    'à aplicação prática do modelo, mantendo explícitas suas '
    'limitações e seu papel como ferramenta de apoio.'
    '</div>'
    '</div>'
)

st.markdown(
    html_entrega,
    unsafe_allow_html=True,
)

st.write("")

st.caption(
    "Datathon FIAP • Passos Mágicos • "
    "Data Analytics & Machine Learning"
)