import streamlit as st

from utils.styles import aplicar_estilo


aplicar_estilo()


st.markdown(
    '<div class="page-label">SOLUÇÃO PREDITIVA</div>',
    unsafe_allow_html=True,
)


st.title(
    "Avaliação de risco de defasagem"
)


st.markdown(
    """
<div class="page-description">
Utilize os indicadores educacionais disponíveis
para estimar a probabilidade de risco utilizando
os modelos treinados no projeto.
</div>
    """,
    unsafe_allow_html=True,
)