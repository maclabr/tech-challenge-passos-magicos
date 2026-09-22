import streamlit as st

from utils.styles import aplicar_estilo


aplicar_estilo()


st.markdown(
    '<div class="page-label">METODOLOGIA</div>',
    unsafe_allow_html=True,
)


st.title(
    "Modelo preditivo & projeto"
)


st.markdown(
    """
<div class="page-description">
Conheça as variáveis utilizadas, a estratégia
de validação temporal, o desempenho dos modelos
e as limitações da solução.
</div>
    """,
    unsafe_allow_html=True,
)