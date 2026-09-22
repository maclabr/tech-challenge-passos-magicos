import streamlit as st


def aplicar_estilo():
    st.markdown(
        """
<style>

:root {
    --navy: #073B63;
    --blue: #0B5F82;
    --teal: #18A6A6;
    --light-teal: #69D4D0;
    --background: #F7FAFC;
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
            circle at 90% 5%,
            rgba(24, 166, 166, 0.05),
            transparent 25%
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
    background: linear-gradient(
        180deg,
        #FFFFFF 0%,
        #F4FAFC 100%
    );

    border-right: 1px solid #DDEAF0;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #073B63;
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
            rgba(80, 205, 202, 0.32),
            transparent 28%
        ),
        linear-gradient(
            120deg,
            #063B63 0%,
            #075879 55%,
            #0B858B 100%
        );

    box-shadow:
        0 18px 45px rgba(4, 55, 87, 0.14);
}

.hero-banner::after {
    content: "";
    position: absolute;

    width: 430px;
    height: 430px;

    right: -160px;
    top: -180px;

    border-radius: 50%;

    border: 1px solid rgba(255, 255, 255, 0.13);

    box-shadow:
        0 0 0 50px rgba(255, 255, 255, 0.025),
        0 0 0 100px rgba(255, 255, 255, 0.015);
}

.hero-eyebrow {
    position: relative;
    z-index: 2;

    color: #86DDDA;

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

    font-size: clamp(2.6rem, 4vw, 4rem);
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

    color: rgba(255, 255, 255, 0.90);

    font-size: 1.05rem;
    line-height: 1.65;
}

.hero-accent {
    position: relative;
    z-index: 2;

    width: 54px;
    height: 3px;

    margin-top: 1.6rem;

    background: #69D4D0;
    border-radius: 10px;
}


/* ==========================================================
   MÉTRICAS
   ========================================================== */

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.96);

    border: 1px solid #DDEAF0;
    border-radius: 18px;

    padding: 1.25rem 1.3rem;

    min-height: 115px;

    box-shadow: 0 7px 25px rgba(4, 55, 87, 0.045);
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
}


/* ==========================================================
   BOTÕES
   ========================================================== */

.stButton > button {
    border-radius: 10px;
    border: 1px solid #BFDCE5;

    color: #07547A;
    background: #FFFFFF;

    font-weight: 600;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #18A6A6;
    color: #087D79;
    background: #F2FBFA;
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