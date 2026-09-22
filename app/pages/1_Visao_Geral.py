import base64
from pathlib import Path

import streamlit as st

from utils.styles import aplicar_estilo


# ============================================================
# ESTILO GLOBAL
# ============================================================

aplicar_estilo()


# ============================================================
# CAMINHOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

HERO_PATH = (
    BASE_DIR
    / "app"
    / "assets"
    / "hero_passos_magicos.png"
)


# ============================================================
# ÍCONES SVG
# ============================================================

ICONS = {

    "database": """
        <svg viewBox="0 0 24 24">
            <ellipse cx="12" cy="5" rx="7" ry="3"></ellipse>
            <path d="M5 5v6c0 1.7 3.1 3 7 3s7-1.3 7-3V5"></path>
            <path d="M5 11v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"></path>
        </svg>
    """,

    "calendar": """
        <svg viewBox="0 0 24 24">
            <rect x="3" y="5" width="18" height="16" rx="2"></rect>
            <path d="M7 3v4"></path>
            <path d="M17 3v4"></path>
            <path d="M3 10h18"></path>
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

    "dashboard": """
        <svg viewBox="0 0 24 24">
            <rect x="3" y="3" width="7" height="7" rx="1"></rect>
            <rect x="14" y="3" width="7" height="7" rx="1"></rect>
            <rect x="3" y="14" width="7" height="7" rx="1"></rect>
            <rect x="14" y="14" width="7" height="7" rx="1"></rect>
        </svg>
    """,

    "risk": """
        <svg viewBox="0 0 24 24">
            <path d="M12 3 21 20H3z"></path>
            <path d="M12 9v5"></path>
            <path d="M12 17h.01"></path>
        </svg>
    """,

    "model": """
        <svg viewBox="0 0 24 24">
            <circle cx="12" cy="5" r="2"></circle>
            <circle cx="5" cy="18" r="2"></circle>
            <circle cx="19" cy="18" r="2"></circle>
            <path d="M11 7 6 16"></path>
            <path d="m13 7 5 9"></path>
            <path d="M7 18h10"></path>
        </svg>
    """,
}


# ============================================================
# FUNÇÕES
# ============================================================

def imagem_base64(caminho: Path) -> str:
    """
    Converte a imagem do hero para Base64.
    """

    if not caminho.exists():
        return ""

    with open(caminho, "rb") as arquivo:
        return base64.b64encode(
            arquivo.read()
        ).decode("utf-8")


def svg_icon(nome: str) -> str:
    """
    Retorna um ícone SVG dentro de um container.
    """

    return (
        '<div class="home-vector-icon">'
        f'{ICONS[nome]}'
        '</div>'
    )


def metric_card(
    titulo,
    valor,
    icone,
    cor,
    soft,
):
    """
    Card utilizado nos indicadores principais.
    """

    html = (
        f'<div class="home-metric-card" '
        f'style="--accent:{cor}; --soft:{soft};">'
        '<div class="home-metric-icon">'
        f'{svg_icon(icone)}'
        '</div>'
        f'<div class="home-metric-value">{valor}</div>'
        f'<div class="home-metric-label">{titulo}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def solution_card(
    titulo,
    texto,
    icone,
    cor,
    soft,
):
    """
    Card utilizado na apresentação das áreas da solução.
    """

    html = (
        f'<div class="solution-card" '
        f'style="--accent:{cor}; --soft:{soft};">'
        '<div class="solution-icon">'
        f'{svg_icon(icone)}'
        '</div>'
        f'<div class="solution-title">{titulo}</div>'
        f'<div class="solution-text">{texto}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ============================================================
# CARREGAMENTO DO HERO
# ============================================================

hero_base64 = imagem_base64(HERO_PATH)


# Caso a imagem não seja encontrada, a página continua funcionando.
# A mensagem abaixo facilita identificar problemas de caminho.

if not HERO_PATH.exists():

    st.error(
        "Imagem do hero não encontrada. "
        f"Verifique se o arquivo está em: {HERO_PATH}"
    )


# ============================================================
# CSS DA PÁGINA
# ============================================================

st.markdown(
    f"""
<style>

/* ======================================================
   SVG
   ====================================================== */

.home-vector-icon {{
    display: flex;
    align-items: center;
    justify-content: center;

    width: 100%;
    height: 100%;
}}

.home-vector-icon svg {{
    width: 100%;
    height: 100%;

    fill: none;

    stroke: currentColor;
    stroke-width: 1.7;

    stroke-linecap: round;
    stroke-linejoin: round;
}}


/* ======================================================
   HERO
   ====================================================== */

.home-hero {{
    position: relative;

    overflow: hidden;

    min-height: 365px;

    border-radius: 26px;

    background-image:

        linear-gradient(
            90deg,
            rgba(3, 48, 78, 0.98) 0%,
            rgba(3, 52, 82, 0.93) 27%,
            rgba(4, 64, 92, 0.70) 44%,
            rgba(4, 71, 99, 0.18) 59%,
            rgba(4, 71, 99, 0.00) 72%
        ),

        url("data:image/png;base64,{hero_base64}");

    background-size: cover;

    background-position:
        center center;

    background-repeat:
        no-repeat;

    border:
        1px solid
        rgba(255, 255, 255, 0.12);

    box-shadow:
        0 18px 45px
        rgba(4, 55, 87, 0.13);
}}


.home-hero-content {{
    position: relative;

    z-index: 2;

    width: 54%;

    max-width: 720px;

    padding:
        3.2rem
        3rem
        3rem
        3rem;
}}


.home-hero-eyebrow {{
    color: #69D4D0;

    font-size: 0.76rem;

    font-weight: 800;

    letter-spacing: 0.18em;

    text-transform: uppercase;

    margin-bottom: 1.1rem;
}}


.home-hero-title {{
    color: #FFFFFF;

    font-size:
        clamp(
            2.4rem,
            3.7vw,
            3.75rem
        );

    line-height: 1.04;

    font-weight: 800;

    letter-spacing: -0.045em;
}}


.home-hero-title span {{
    color: #69D4D0;
}}


.home-hero-description {{
    max-width: 590px;

    margin-top: 1.25rem;

    color:
        rgba(
            255,
            255,
            255,
            0.90
        );

    font-size: 1rem;

    line-height: 1.65;
}}


.home-hero-accent {{
    width: 70px;

    height: 4px;

    margin-top: 1.5rem;

    border-radius: 999px;

    background:
        linear-gradient(
            90deg,
            #69D4D0 0%,
            #F2B544 100%
        );
}}


/* ======================================================
   MÉTRICAS
   ====================================================== */

.home-metric-card {{
    position: relative;

    overflow: hidden;

    min-height: 145px;

    padding:
        1.15rem
        1.2rem;

    background: #FFFFFF;

    border:
        1px solid #DDEAF0;

    border-top:
        4px solid var(--accent);

    border-radius: 17px;

    box-shadow:
        0 6px 20px
        rgba(4, 55, 87, 0.035);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}}


.home-metric-card:hover {{
    transform:
        translateY(-2px);

    box-shadow:
        0 10px 25px
        rgba(4, 55, 87, 0.07);
}}


.home-metric-icon {{
    width: 38px;
    height: 38px;

    padding: 8px;

    border-radius: 11px;

    color: var(--accent);

    background: var(--soft);
}}


.home-metric-value {{
    margin-top: 0.75rem;

    color: #073B63;

    font-size: 1.65rem;

    font-weight: 800;

    line-height: 1;
}}


.home-metric-label {{
    margin-top: 0.4rem;

    color: #687F90;

    font-size: 0.76rem;

    font-weight: 600;
}}


/* ======================================================
   SEÇÃO SOBRE A SOLUÇÃO
   ====================================================== */

.home-section-label {{
    color: #18A6A6;

    font-size: 0.72rem;

    font-weight: 800;

    letter-spacing: 0.15em;

    text-transform: uppercase;

    margin-bottom: 0.35rem;
}}


.home-section-title {{
    color: #073B63;

    font-size: 1.65rem;

    font-weight: 800;

    letter-spacing: -0.03em;

    margin-bottom: 0.8rem;
}}


.home-section-description {{
    max-width: 980px;

    color: #526D80;

    font-size: 0.94rem;

    line-height: 1.7;
}}


.home-section-description strong {{
    color: #073B63;
}}


/* ======================================================
   CARDS DA SOLUÇÃO
   ====================================================== */

.solution-card {{
    position: relative;

    min-height: 205px;

    height: 100%;

    padding:
        1.35rem
        1.35rem;

    background:
        linear-gradient(
            145deg,
            var(--soft) 0%,
            #FFFFFF 65%
        );

    border:
        1px solid #DDEAF0;

    border-top:
        4px solid var(--accent);

    border-radius: 18px;

    box-shadow:
        0 7px 22px
        rgba(4, 55, 87, 0.035);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}}


.solution-card:hover {{
    transform:
        translateY(-2px);

    box-shadow:
        0 11px 27px
        rgba(4, 55, 87, 0.07);
}}


.solution-icon {{
    width: 44px;
    height: 44px;

    padding: 10px;

    border-radius: 13px;

    color: var(--accent);

    background: var(--soft);

    margin-bottom: 0.9rem;
}}


.solution-title {{
    color: #073B63;

    font-size: 1rem;

    font-weight: 800;

    margin-bottom: 0.55rem;
}}


.solution-text {{
    color: #617A8D;

    font-size: 0.82rem;

    line-height: 1.58;
}}


/* ======================================================
   RESPONSIVIDADE
   ====================================================== */

@media (max-width: 900px) {{

    .home-hero {{
        min-height: 410px;

        background-position:
            62% center;
    }}


    .home-hero-content {{
        width: 68%;

        padding:
            2.7rem
            2rem;
    }}

}}


@media (max-width: 650px) {{

    .home-hero {{
        min-height: 455px;

        background-position:
            65% center;
    }}


    .home-hero::after {{
        content: "";

        position: absolute;

        inset: 0;

        background:
            rgba(
                3,
                48,
                78,
                0.27
            );
    }}


    .home-hero-content {{
        width: 100%;

        padding:
            2.3rem
            1.5rem;
    }}


    .home-hero-title {{
        font-size: 2.3rem;
    }}

}}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

# IMPORTANTE:
# O HTML é construído sem indentação para evitar que
# o Markdown do Streamlit interprete o conteúdo como código.

hero_html = (
    '<div class="home-hero">'
    '<div class="home-hero-content">'
    '<div class="home-hero-eyebrow">'
    'DATATHON • PASSOS MÁGICOS'
    '</div>'
    '<div class="home-hero-title">'
    'Dados que ajudam a<br>'
    '<span>transformar trajetórias.</span>'
    '</div>'
    '<div class="home-hero-description">'
    'Uma solução de Data Analytics desenvolvida para '
    'apoiar a identificação antecipada de alunos com '
    'maior probabilidade de defasagem educacional.'
    '</div>'
    '<div class="home-hero-accent"></div>'
    '</div>'
    '</div>'
)

st.markdown(
    hero_html,
    unsafe_allow_html=True,
)


st.write("")


# ============================================================
# INDICADORES PRINCIPAIS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    metric_card(
        titulo="Registros analisados",
        valor="3.030",
        icone="database",
        cor="#42A5D9",
        soft="#EDF7FC",
    )


with col2:

    metric_card(
        titulo="Período analisado",
        valor="2022 – 2024",
        icone="calendar",
        cor="#45B98C",
        soft="#EDF9F3",
    )


with col3:

    metric_card(
        titulo="Indicadores PEDE",
        valor="8",
        icone="chart",
        cor="#F2B544",
        soft="#FFF8E8",
    )


with col4:

    metric_card(
        titulo="Modelos preditivos",
        valor="2",
        icone="network",
        cor="#8B73C7",
        soft="#F4F0FB",
    )


st.write("")
st.write("")


# ============================================================
# SOBRE A SOLUÇÃO
# ============================================================

sobre_html = (
    '<div class="home-section-label">'
    'VISÃO DA SOLUÇÃO'
    '</div>'
    '<div class="home-section-title">'
    'Da análise dos dados à aplicação prática'
    '</div>'
    '<div class="home-section-description">'
    'A aplicação utiliza indicadores educacionais da '
    '<strong>Passos Mágicos</strong> para disponibilizar '
    'uma ferramenta de apoio à avaliação de risco de defasagem.'
    '<br><br>'
    'A proposta é transformar os resultados das análises e dos '
    'modelos preditivos desenvolvidos no Datathon em uma interface '
    'acessível, permitindo explorar os dados, acompanhar os '
    'principais indicadores e realizar avaliações de risco.'
    '</div>'
)

st.markdown(
    sobre_html,
    unsafe_allow_html=True,
)


st.write("")
st.write("")


# ============================================================
# CARDS DA SOLUÇÃO
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    solution_card(
        titulo="Panorama educacional",
        icone="dashboard",
        cor="#18A6A6",
        soft="#E7F8F7",
        texto=(
            "Explore os principais indicadores e resultados "
            "encontrados durante a análise dos dados de "
            "2022, 2023 e 2024."
        ),
    )


with col2:

    solution_card(
        titulo="Avaliação de risco",
        icone="risk",
        cor="#F47C6C",
        soft="#FFF1EE",
        texto=(
            "Utilize os indicadores disponíveis para estimar "
            "a probabilidade de defasagem de forma simples "
            "e interativa."
        ),
    )


with col3:

    solution_card(
        titulo="Machine Learning",
        icone="model",
        cor="#8B73C7",
        soft="#F4F0FB",
        texto=(
            "Consulte informações sobre os modelos, "
            "variáveis utilizadas, validação temporal, "
            "desempenho e limitações."
        ),
    )


st.write("")


# ============================================================
# RODAPÉ
# ============================================================

st.caption(
    "Datathon FIAP • Passos Mágicos • "
    "Data Analytics & Machine Learning"
)