import streamlit as st

from utils.styles import aplicar_estilo


# ============================================================
# ESTILO
# ============================================================

aplicar_estilo()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero-banner"><div class="hero-eyebrow">DATATHON • PASSOS MÁGICOS</div><div class="hero-title">Dados que ajudam a<br><span>transformar trajetórias.</span></div><div class="hero-description">Uma solução de Data Analytics desenvolvida para apoiar a identificação antecipada de alunos com maior probabilidade de defasagem educacional.</div><div class="hero-accent"></div></div>
    """,
    unsafe_allow_html=True,
)


st.write("")


# ============================================================
# INDICADORES
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        label="Registros analisados",
        value="3.030",
    )


with col2:

    st.metric(
        label="Período analisado",
        value="2022 – 2024",
    )


with col3:

    st.metric(
        label="Indicadores PEDE",
        value="8",
    )


with col4:

    st.metric(
        label="Modelos preditivos",
        value="2",
    )


st.write("")
st.write("")


# ============================================================
# SOBRE A SOLUÇÃO
# ============================================================

st.subheader(
    "Sobre a solução"
)


st.markdown(
    """
A aplicação utiliza indicadores educacionais da
**Passos Mágicos** para disponibilizar uma ferramenta
de apoio à avaliação de risco de defasagem.

A proposta é transformar os resultados das análises e
dos modelos preditivos desenvolvidos no Datathon em uma
interface acessível, permitindo explorar os dados e
realizar avaliações de risco.
    """
)


st.write("")


# ============================================================
# CARDS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    with st.container(border=True):

        st.markdown(
            '<div class="card-title">Panorama educacional</div>',
            unsafe_allow_html=True,
        )

        st.write(
            """
Explore os principais indicadores e resultados
encontrados durante a análise dos dados de
2022, 2023 e 2024.
            """
        )


with col2:

    with st.container(border=True):

        st.markdown(
            '<div class="card-title">Avaliação de risco</div>',
            unsafe_allow_html=True,
        )

        st.write(
            """
Utilize os indicadores disponíveis para estimar
a probabilidade de defasagem de forma simples
e interativa.
            """
        )


with col3:

    with st.container(border=True):

        st.markdown(
            '<div class="card-title">Machine Learning</div>',
            unsafe_allow_html=True,
        )

        st.write(
            """
Consulte informações sobre os modelos,
variáveis utilizadas, validação temporal,
desempenho e limitações.
            """
        )