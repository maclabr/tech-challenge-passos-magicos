import streamlit as st


# ============================================================
# CONFIGURAÇÃO GERAL
# ============================================================

st.set_page_config(
    page_title="Passos Mágicos | Datathon",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PÁGINAS
# ============================================================

visao_geral = st.Page(
    "pages/1_Visao_Geral.py",
    title="Visão Geral",
    default=True,
)

dashboard = st.Page(
    "pages/2_Dashboard.py",
    title="Dashboard",
)

avaliacao_risco = st.Page(
    "pages/3_Avaliacao_de_Risco.py",
    title="Avaliação de Risco",
)

modelo_projeto = st.Page(
    "pages/4_Modelo_e_Projeto.py",
    title="Modelo & Projeto",
)


# ============================================================
# NAVEGAÇÃO
# ============================================================

pagina = st.navigation(
    [
        visao_geral,
        dashboard,
        avaliacao_risco,
        modelo_projeto,
    ]
)


pagina.run()