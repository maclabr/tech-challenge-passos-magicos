import streamlit as st


def aplicar_estilo():
    st.markdown(
        """
<style>

/* ==========================================================
   PALETA OFICIAL
   ========================================================== */

:root {

    /* Identidade principal */
    --navy: #073B63;
    --blue: #0B5F82;
    --teal: #18A6A6;
    --light-teal: #69D4D0;

    /* Cores de apoio */
    --coral: #F47C6C;
    --coral-soft: #FFF1EE;

    --amber: #F2B544;
    --amber-soft: #FFF8E8;

    --green: #45B98C;
    --green-soft: #EDF9F3;

    --purple: #8B73C7;
    --purple-soft: #F4F0FB;

    --sky: #42A5D9;
    --sky-soft: #EDF7FC;

    /* Neutros */
    --background: #F8FBFC;
    --surface: #FFFFFF;
    --text: #143A59;
    --muted: #527087;
    --border: #DDEAF0;
}


/* ==========================================================
   PÁGINA
   ========================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 94% 4%,
            rgba(105, 212, 208, 0.11),
            transparent 23%
        ),
        radial-gradient(
            circle at 3% 43%,
            rgba(242, 181, 68, 0.045),
            transparent 19%
        ),
        radial-gradient(
            circle at 96% 83%,
            rgba(139, 115, 199, 0.045),
            transparent 19%
        ),
        #F8FBFC;
}

.block-container {
    max-width: 1380px;

    padding-top: 2.5rem;
    padding-bottom: 4rem;
    padding-left: 3rem;
    padding-right: 3rem;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #FCFCFB 0%,
            #FAFAF9 48%,
            #F7F8F8 100%
        );

    border-right: 1px solid #E3E8EA;

    box-shadow:
        8px 0 28px rgba(7, 59, 99, 0.028);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--navy);
}


/* ==========================================================
   NAVEGAÇÃO LATERAL
   ========================================================== */

/* Área que contém a navegação multipágina */
[data-testid="stSidebarNav"] {
    padding-top: 1.15rem;
}

/* Links */
[data-testid="stSidebarNav"] a {
    position: relative;
    min-height: 52px;
    margin: 0.30rem 0.70rem;
    padding: 0.62rem 0.75rem 0.62rem 3.35rem !important;
    border: 1px solid transparent;
    border-radius: 13px;
    color: #365E79 !important;
    font-weight: 650;
    transition:
        background 0.18s ease,
        border-color 0.18s ease,
        transform 0.18s ease,
        box-shadow 0.18s ease;
}

/* Texto do item */
[data-testid="stSidebarNav"] a span {
    color: inherit !important;
}

/* Hover */
[data-testid="stSidebarNav"] a:hover {
    background: #F0F8FA !important;
    border-color: #D5EBEF;
    color: #073B63 !important;
    transform: translateX(2px);
}

/* Item ativo */
[data-testid="stSidebarNav"] a[aria-current="page"] {
    color: #073B63 !important;
    font-weight: 800;
    box-shadow: 0 5px 16px rgba(7, 59, 99, 0.055);
}

/* Barra lateral do item ativo */
[data-testid="stSidebarNav"] a[aria-current="page"]::before {
    content: "";
    position: absolute;
    left: 0;
    top: 9px;
    bottom: 9px;
    width: 4px;
    border-radius: 0 8px 8px 0;
}

/* Cada página ativa usa sua própria cor semântica */

/* Visão Geral — turquesa */
[data-testid="stSidebarNav"] li:nth-child(1) a[aria-current="page"] {
    background: linear-gradient(90deg, #E5F7F6 0%, #F3FBFA 100%) !important;
    border-color: #C8EAE7;
}
[data-testid="stSidebarNav"] li:nth-child(1) a[aria-current="page"]::before {
    background: #18A6A6;
}

/* Dashboard — azul */
[data-testid="stSidebarNav"] li:nth-child(2) a[aria-current="page"] {
    background: linear-gradient(90deg, #E8F5FB 0%, #F4FAFD 100%) !important;
    border-color: #CDE8F4;
}
[data-testid="stSidebarNav"] li:nth-child(2) a[aria-current="page"]::before {
    background: #42A5D9;
}

/* Avaliação de Risco — coral */
[data-testid="stSidebarNav"] li:nth-child(3) a[aria-current="page"] {
    background: linear-gradient(90deg, #FFF0ED 0%, #FFF8F6 100%) !important;
    border-color: #F3D1CB;
}
[data-testid="stSidebarNav"] li:nth-child(3) a[aria-current="page"]::before {
    background: #F47C6C;
}

/* Modelo & Projeto — lilás */
[data-testid="stSidebarNav"] li:nth-child(4) a[aria-current="page"] {
    background: linear-gradient(90deg, #F1EDFA 0%, #F8F6FD 100%) !important;
    border-color: #DDD4F1;
}
[data-testid="stSidebarNav"] li:nth-child(4) a[aria-current="page"]::before {
    background: #8B73C7;
}

/* Base dos ícones vetoriais.
   Os SVGs são aplicados como máscaras CSS, portanto seguem a cor
   definida para cada página e continuam nítidos em qualquer escala. */
[data-testid="stSidebarNav"] a::after {
    content: "";
    position: absolute;
    left: 0.92rem;
    top: 50%;
    width: 25px;
    height: 25px;
    transform: translateY(-50%);
    background-color: #18A6A6;
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    -webkit-mask-position: center;
    mask-position: center;
    -webkit-mask-size: 22px 22px;
    mask-size: 22px 22px;
}

/* Visão Geral — casa */
[data-testid="stSidebarNav"] li:nth-child(1) a::after {
    background-color: #18A6A6;
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M12 3 3 10.2V21h6v-6h6v6h6V10.2L12 3Zm7 16h-2v-6H7v6H5v-7.84l7-5.6 7 5.6V19Z'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M12 3 3 10.2V21h6v-6h6v6h6V10.2L12 3Zm7 16h-2v-6H7v6H5v-7.84l7-5.6 7 5.6V19Z'/%3E%3C/svg%3E");
}

/* Dashboard — barras */
[data-testid="stSidebarNav"] li:nth-child(2) a::after {
    background-color: #42A5D9;
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M4 20V10h4v10H4Zm6 0V4h4v16h-4Zm6 0v-7h4v7h-4Z'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M4 20V10h4v10H4Zm6 0V4h4v16h-4Zm6 0v-7h4v7h-4Z'/%3E%3C/svg%3E");
}

/* Avaliação de Risco — alvo */
[data-testid="stSidebarNav"] li:nth-child(3) a::after {
    background-color: #F47C6C;
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M12 2a10 10 0 1 0 9.95 11H20a8 8 0 1 1-2.34-5.66l-2.12 2.12A5 5 0 1 0 17 13h-2a3 3 0 1 1-.88-2.12L11 14l1.41 1.41 3.13-3.13A5 5 0 0 0 17 13h2a7 7 0 0 0-2.05-4.95l2.12-2.12A9.96 9.96 0 0 0 12 2Z'/%3E%3Cpath fill='black' d='M17 2h5v5h-2V5.41l-7.29 7.3-1.42-1.42L18.59 4H17V2Z'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M12 2a10 10 0 1 0 9.95 11H20a8 8 0 1 1-2.34-5.66l-2.12 2.12A5 5 0 1 0 17 13h-2a3 3 0 1 1-.88-2.12L11 14l1.41 1.41 3.13-3.13A5 5 0 0 0 17 13h2a7 7 0 0 0-2.05-4.95l2.12-2.12A9.96 9.96 0 0 0 12 2Z'/%3E%3Cpath fill='black' d='M17 2h5v5h-2V5.41l-7.29 7.3-1.42-1.42L18.59 4H17V2Z'/%3E%3C/svg%3E");
}

/* Modelo & Projeto — documento */
[data-testid="stSidebarNav"] li:nth-child(4) a::after {
    background-color: #8B73C7;
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M6 2h8l5 5v15H6V2Zm2 2v16h9V8h-4V4H8Zm7 .83V6h1.17L15 4.83ZM9 11h6v2H9v-2Zm0 4h6v2H9v-2Z'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='black' d='M6 2h8l5 5v15H6V2Zm2 2v16h9V8h-4V4H8Zm7 .83V6h1.17L15 4.83ZM9 11h6v2H9v-2Zm0 4h6v2H9v-2Z'/%3E%3C/svg%3E");
}

/* O item ativo recebe um pequeno fundo suave no ícone */
[data-testid="stSidebarNav"] a[aria-current="page"]::after {
    filter: saturate(1.12);
}

/* Botão nativo de recolher a sidebar */
[data-testid="stSidebarCollapseButton"] button {
    color: #527087 !important;
    border-radius: 9px !important;
}

[data-testid="stSidebarCollapseButton"] button:hover {
    background: #EDF7FC !important;
    color: #073B63 !important;
}

/* Ajuste para sidebar recolhida / telas estreitas */
@media (max-width: 900px) {
    [data-testid="stSidebarNav"] a {
        margin-left: 0.45rem;
        margin-right: 0.45rem;
    }
}


/* ==========================================================
   HERO
   ========================================================== */

.hero-banner {

    position: relative;
    overflow: hidden;

    min-height: 290px;

    padding: 3rem 3.2rem;

    border-radius: 24px;

    background:
        radial-gradient(
            circle at 88% 25%,
            rgba(105, 212, 208, 0.34),
            transparent 27%
        ),
        radial-gradient(
            circle at 74% 105%,
            rgba(242, 181, 68, 0.12),
            transparent 25%
        ),
        linear-gradient(
            120deg,
            #063B63 0%,
            #075879 53%,
            #0B858B 100%
        );

    box-shadow:
        0 18px 45px rgba(4, 55, 87, 0.14);
}


/* Círculos decorativos */

.hero-banner::after {

    content: "";

    position: absolute;

    width: 430px;
    height: 430px;

    right: -160px;
    top: -180px;

    border-radius: 50%;

    border:
        1px solid rgba(
            255,
            255,
            255,
            0.13
        );

    box-shadow:
        0 0 0 50px rgba(255, 255, 255, 0.025),
        0 0 0 100px rgba(255, 255, 255, 0.015);
}


.hero-eyebrow {

    position: relative;
    z-index: 2;

    color: #8DE1DD;

    font-size: 0.78rem;
    font-weight: 700;

    letter-spacing: 0.18em;

    text-transform: uppercase;

    margin-bottom: 1rem;
}


.hero-title {

    position: relative;
    z-index: 2;

    max-width: 850px;

    color: #FFFFFF;

    font-size:
        clamp(
            2.6rem,
            4vw,
            4rem
        );

    line-height: 1.04;

    font-weight: 800;

    letter-spacing: -0.04em;
}


.hero-title span {
    color: #69D4D0;
}


.hero-description {

    position: relative;
    z-index: 2;

    max-width: 720px;

    margin-top: 1.3rem;

    color:
        rgba(
            255,
            255,
            255,
            0.90
        );

    font-size: 1.05rem;

    line-height: 1.65;
}


.hero-accent {

    position: relative;
    z-index: 2;

    width: 58px;
    height: 4px;

    margin-top: 1.6rem;

    background:
        linear-gradient(
            90deg,
            #69D4D0 0%,
            #F2B544 100%
        );

    border-radius: 10px;
}


/* ==========================================================
   MÉTRICAS STREAMLIT
   ========================================================== */

div[data-testid="stMetric"] {

    background:
        rgba(
            255,
            255,
            255,
            0.97
        );

    border:
        1px solid #DDEAF0;

    border-radius: 18px;

    padding:
        1.25rem
        1.3rem;

    min-height: 115px;

    box-shadow:
        0 7px 25px
        rgba(
            4,
            55,
            87,
            0.045
        );

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}


div[data-testid="stMetric"]:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 10px 30px
        rgba(
            4,
            55,
            87,
            0.07
        );
}


div[data-testid="stMetricLabel"] p {

    color: #527087;

    font-size: 0.85rem;
}


div[data-testid="stMetricValue"] {

    color: #073B63;

    font-weight: 800;
}


/* ==========================================================
   TIPOGRAFIA
   ========================================================== */

h1,
h2,
h3 {

    color: #073B63;

    letter-spacing: -0.025em;
}


p {
    color: #4F6B80;
}


/* ==========================================================
   CARDS
   ========================================================== */

.card-title {

    color: #073B63;

    font-size: 1.15rem;

    font-weight: 750;

    margin-bottom: 0.3rem;
}


div[data-testid="stVerticalBlockBorderWrapper"] {

    border-color: #DDEAF0;

    border-radius: 14px;
}


/* ==========================================================
   BOTÕES
   ========================================================== */

.stButton > button {

    border-radius: 10px;

    border:
        1px solid #BFDCE5;

    color: #07547A;

    background: #FFFFFF;

    font-weight: 600;

    transition:
        all 0.2s ease;
}


.stButton > button:hover {

    border-color: #18A6A6;

    color: #087D79;

    background: #F2FBFA;

    transform:
        translateY(-1px);
}


/* Botão primário */

button[kind="primary"] {

    border: none !important;

    background:
        linear-gradient(
            90deg,
            #0B7186 0%,
            #18A6A6 100%
        ) !important;

    color:
        #FFFFFF !important;

    box-shadow:
        0 5px 15px
        rgba(
            24,
            166,
            166,
            0.16
        );
}


button[kind="primary"]:hover {

    background:
        linear-gradient(
            90deg,
            #075F78 0%,
            #139493 100%
        ) !important;

    color:
        #FFFFFF !important;
}


/* ==========================================================
   PÁGINAS INTERNAS
   ========================================================== */

.page-label {

    color: #15949B;

    font-size: 0.76rem;

    font-weight: 700;

    letter-spacing: 0.16em;

    text-transform: uppercase;

    margin-bottom: 0.3rem;
}


.page-description {

    color: #527087;

    font-size: 1rem;

    line-height: 1.7;

    max-width: 850px;
}


/* ==========================================================
   CORES DE APOIO
   ========================================================== */

.text-navy {
    color: var(--navy);
}

.text-teal {
    color: var(--teal);
}

.text-green {
    color: var(--green);
}

.text-coral {
    color: var(--coral);
}

.text-amber {
    color: var(--amber);
}

.text-purple {
    color: var(--purple);
}

.text-sky {
    color: var(--sky);
}


/* ==========================================================
   ACENTOS DE SEÇÃO
   ========================================================== */

.section-accent {

    position: relative;

    padding-left: 15px;
}


.section-accent::before {

    content: "";

    position: absolute;

    left: 0;

    top: 0.15em;

    width: 4px;

    height: 1.05em;

    border-radius: 10px;

    background: var(--teal);
}


.section-accent.coral::before {
    background: var(--coral);
}

.section-accent.amber::before {
    background: var(--amber);
}

.section-accent.green::before {
    background: var(--green);
}

.section-accent.purple::before {
    background: var(--purple);
}

.section-accent.sky::before {
    background: var(--sky);
}


/* ==========================================================
   CARDS COLORIDOS SUAVES
   ========================================================== */

.soft-card {

    border-radius: 16px;

    padding: 1rem 1.1rem;

    border: 1px solid var(--border);

    background: #FFFFFF;
}


.soft-card.teal {

    background:
        linear-gradient(
            135deg,
            #F1FBFA 0%,
            #FFFFFF 100%
        );

    border-color: #CDECE8;
}


.soft-card.green {

    background:
        linear-gradient(
            135deg,
            #EDF9F3 0%,
            #FFFFFF 100%
        );

    border-color: #CEEBDD;
}


.soft-card.coral {

    background:
        linear-gradient(
            135deg,
            #FFF1EE 0%,
            #FFFFFF 100%
        );

    border-color: #F6D6CF;
}


.soft-card.amber {

    background:
        linear-gradient(
            135deg,
            #FFF8E8 0%,
            #FFFFFF 100%
        );

    border-color: #F3E1B4;
}


.soft-card.purple {

    background:
        linear-gradient(
            135deg,
            #F4F0FB 0%,
            #FFFFFF 100%
        );

    border-color: #DDD4F1;
}


.soft-card.sky {

    background:
        linear-gradient(
            135deg,
            #EDF7FC 0%,
            #FFFFFF 100%
        );

    border-color: #D2E9F4;
}


/* ==========================================================
   ÍCONES / BADGES COLORIDOS
   ========================================================== */

.icon-badge {

    width: 42px;
    height: 42px;

    border-radius: 50%;

    display: inline-flex;

    align-items: center;

    justify-content: center;
}


.icon-badge.teal {

    color: #087D79;

    background: #E0F7F5;
}


.icon-badge.green {

    color: #268A69;

    background: #E1F6EB;
}


.icon-badge.coral {

    color: #C75C50;

    background: #FFE4DE;
}


.icon-badge.amber {

    color: #B57B12;

    background: #FFF0C8;
}


.icon-badge.purple {

    color: #7155B2;

    background: #EAE3F8;
}


.icon-badge.sky {

    color: #247FAE;

    background: #DFF2FB;
}


/* ==========================================================
   PILLS / TAGS
   ========================================================== */

.pill {

    display: inline-block;

    padding:
        0.36rem
        0.7rem;

    margin:
        0.16rem
        0.1rem;

    border-radius: 999px;

    font-size: 0.75rem;

    font-weight: 650;
}


.pill.teal {

    background: #E7F8F7;

    color: #087D79;

    border:
        1px solid #CBEAE7;
}


.pill.green {

    background: #EDF9F3;

    color: #287A60;

    border:
        1px solid #D1ECDD;
}


.pill.coral {

    background: #FFF1EE;

    color: #B9574D;

    border:
        1px solid #F4D4CE;
}


.pill.amber {

    background: #FFF8E8;

    color: #9A6A12;

    border:
        1px solid #F0DFB7;
}


.pill.purple {

    background: #F4F0FB;

    color: #6850A4;

    border:
        1px solid #DDD4F0;
}


.pill.sky {

    background: #EDF7FC;

    color: #27789F;

    border:
        1px solid #D2E8F3;
}


/* ==========================================================
   BLOCOS DE STATUS
   ========================================================== */

.status-positive {

    background: #EDF9F3;

    border-left:
        4px solid #45B98C;

    border-radius:
        0 12px 12px 0;

    padding:
        0.9rem 1rem;
}


.status-warning {

    background: #FFF8E8;

    border-left:
        4px solid #F2B544;

    border-radius:
        0 12px 12px 0;

    padding:
        0.9rem 1rem;
}


.status-risk {

    background: #FFF1EE;

    border-left:
        4px solid #F47C6C;

    border-radius:
        0 12px 12px 0;

    padding:
        0.9rem 1rem;
}


.status-model {

    background: #F4F0FB;

    border-left:
        4px solid #8B73C7;

    border-radius:
        0 12px 12px 0;

    padding:
        0.9rem 1rem;
}


/* ==========================================================
   DIVISORES
   ========================================================== */

hr {

    border: none;

    height: 1px;

    background:
        linear-gradient(
            90deg,
            rgba(24, 166, 166, 0.35),
            rgba(242, 181, 68, 0.18),
            rgba(139, 115, 199, 0.10),
            transparent
        );

    margin:
        1.5rem 0;
}


/* ==========================================================
   TABELAS
   ========================================================== */

[data-testid="stDataFrame"] {

    border-radius: 14px;

    overflow: hidden;

    border:
        1px solid #DDEAF0;
}


/* ==========================================================
   EXPANDERS
   ========================================================== */

[data-testid="stExpander"] {

    background:
        rgba(
            255,
            255,
            255,
            0.72
        );

    border:
        1px solid #DDEAF0 !important;

    border-radius:
        12px !important;
}


/* ==========================================================
   STREAMLIT
   ========================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
        """,
        unsafe_allow_html=True,
    )