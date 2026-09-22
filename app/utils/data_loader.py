from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "pede_painel_consolidado.csv"
)


@st.cache_data
def carregar_dados():
    """
    Carrega a base consolidada preparada nas etapas
    anteriores do projeto.

    Este módulo apenas disponibiliza os dados para
    a aplicação Streamlit.
    """

    return pd.read_csv(DATA_PATH)