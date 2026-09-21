"""App Streamlit — avaliação manual de risco de defasagem (PEDE, Passos Mágicos).

Formulário de um aluno por vez, com valores digitados manualmente. Não há busca por
RA, autocomplete ou qualquer tela que exponha identificador individual (ver regra 6
do contrato de dados em docs/contrato_de_dados.md).
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.modeling import ALVO_INCIDENCIA, ALVO_RISCO_FUTURO, FEATURES_NUMERICAS, explicar_previsao  # noqa: E402

MODELOS_DIR = REPO_ROOT / "models"
ANO_ATUAL = datetime.date.today().year

CAMINHOS_MODELO = {
    ALVO_RISCO_FUTURO: {
        "calibrado": MODELOS_DIR / "pipeline_risco_futuro.joblib",
        "explicativo": MODELOS_DIR / "pipeline_risco_futuro_explicativo.joblib",
    },
    ALVO_INCIDENCIA: {
        "calibrado": MODELOS_DIR / "pipeline_incidencia_nova_defasagem.joblib",
        "explicativo": MODELOS_DIR / "pipeline_incidencia_nova_defasagem_explicativo.joblib",
    },
}

TITULOS = {
    ALVO_RISCO_FUTURO: "Risco futuro de defasagem",
    ALVO_INCIDENCIA: "Incidência de nova defasagem",
}

# Faixas baseadas no contrato de dados (docs/contrato_de_dados.md, seção 3): indicadores
# PEDE e notas aproximadamente 0-10; fase observada no painel vai até 9.
FEATURE_CONFIG = {
    "FASE": {"rotulo": "Fase atual", "minimo": 0, "maximo": 9, "passo": 1, "padrao": 2},
    "FASE_IDEAL": {"rotulo": "Fase ideal para a idade/série", "minimo": 0, "maximo": 8, "passo": 1, "padrao": 2},
    "IAN": {"rotulo": "IAN — Indicador de Adequação de Nível", "minimo": 0.0, "maximo": 10.0, "passo": 0.1, "padrao": 5.0},
    "IDA": {"rotulo": "IDA — Indicador de Aprendizagem", "minimo": 0.0, "maximo": 10.0, "passo": 0.1, "padrao": 5.0},
    "IEG": {"rotulo": "IEG — Indicador de Engajamento", "minimo": 0.0, "maximo": 10.0, "passo": 0.1, "padrao": 5.0},
    "IAA": {"rotulo": "IAA — Indicador de Autoavaliação", "minimo": 0.0, "maximo": 10.0, "passo": 0.1, "padrao": 5.0},
    "IPS": {"rotulo": "IPS — Indicador Psicossocial", "minimo": 0.0, "maximo": 10.0, "passo": 0.1, "padrao": 5.0},
    "IPV": {"rotulo": "IPV — Indicador de Ponto de Virada", "minimo": 0.0, "maximo": 10.0, "passo": 0.1, "padrao": 5.0},
    "NOTA_MATEMATICA": {"rotulo": "Nota de matemática", "minimo": 0.0, "maximo": 10.0, "passo": 0.1, "padrao": 5.0},
    "NOTA_PORTUGUES": {"rotulo": "Nota de português", "minimo": 0.0, "maximo": 10.0, "passo": 0.1, "padrao": 5.0},
    "NOTA_INGLES": {"rotulo": "Nota de inglês", "minimo": 0.0, "maximo": 10.0, "passo": 0.1, "padrao": 5.0},
    "IDADE_ANOS": {"rotulo": "Idade (anos)", "minimo": 6, "maximo": 22, "passo": 1, "padrao": 12},
    "ANO_INGRESSO": {"rotulo": "Ano de ingresso no programa", "minimo": 2015, "maximo": ANO_ATUAL, "passo": 1, "padrao": 2022},
}

FEATURES_FORMULARIO = tuple(feature for feature in FEATURES_NUMERICAS if feature != "DEFASAGEM_CALCULADA")


@st.cache_resource
def carregar_modelos(tipo_alvo: str):
    caminhos = CAMINHOS_MODELO[tipo_alvo]
    pipeline_calibrado = joblib.load(caminhos["calibrado"])
    pipeline_explicativo = joblib.load(caminhos["explicativo"])
    return pipeline_calibrado, pipeline_explicativo


@st.cache_resource
def carregar_metadados() -> dict:
    with open(MODELOS_DIR / "metadados.json", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def campo_numerico(tipo_alvo: str, feature: str) -> float:
    """Renderiza número + checkbox 'não sei'; ausência vira NaN de verdade, nunca 0.0."""
    config = FEATURE_CONFIG[feature]
    chave_base = f"{tipo_alvo}_{feature}"
    with st.container(horizontal=True, vertical_alignment="bottom"):
        nao_informado = st.checkbox(
            "Não sei",
            key=f"na_{chave_base}",
            help="Marque quando este indicador não estiver disponível para o aluno.",
        )
        valor = st.number_input(
            config["rotulo"],
            min_value=config["minimo"],
            max_value=config["maximo"],
            value=config["padrao"],
            step=config["passo"],
            key=f"valor_{chave_base}",
            disabled=nao_informado,
        )
    return np.nan if nao_informado else valor


def renderizar_formulario(tipo_alvo: str) -> None:
    pipeline_calibrado, pipeline_explicativo = carregar_modelos(tipo_alvo)
    metadados = carregar_metadados()
    metricas_ref = metadados["metricas_referencia"]["por_alvo"][tipo_alvo]

    st.caption(
        "Preencha os indicadores do aluno manualmente. Campos sem informação disponível "
        "devem ser marcados como **Não sei** — não preencha com zero, pois zero é um valor "
        "real do indicador, diferente de indisponibilidade de medição."
    )

    with st.form(f"formulario_{tipo_alvo}", border=False):
        valores = {feature: campo_numerico(tipo_alvo, feature) for feature in FEATURES_FORMULARIO}

        fase, fase_ideal = valores["FASE"], valores["FASE_IDEAL"]
        if np.isnan(fase) or np.isnan(fase_ideal):
            defasagem = np.nan
            st.caption("Defasagem calculada: indisponível (informe fase e fase ideal)")
        else:
            defasagem = fase - fase_ideal
            st.caption(f"Defasagem calculada automaticamente (fase − fase ideal): **{defasagem:g}**")

        enviado = st.form_submit_button("Calcular", icon=":material/calculate:", type="primary")

    if enviado:
        linha = {**valores, "DEFASAGEM_CALCULADA": defasagem}
        x_linha = pd.DataFrame([linha])[list(FEATURES_NUMERICAS)]
        probabilidade = float(pipeline_calibrado.predict_proba(x_linha)[0, 1])
        explicacao = explicar_previsao(pipeline_explicativo, x_linha, top_n=3)
        st.session_state[f"resultado_{tipo_alvo}"] = {"probabilidade": probabilidade, "explicacao": explicacao}

    resultado = st.session_state.get(f"resultado_{tipo_alvo}")
    if resultado:
        st.divider()
        st.metric("Probabilidade calibrada", f"{resultado['probabilidade'] * 100:.1f}%")

        limiar = st.slider(
            "Limiar de decisão",
            min_value=0.1,
            max_value=0.9,
            value=0.5,
            step=0.05,
            key=f"limiar_{tipo_alvo}",
            help=(
                "Decisão de negócio ainda pendente com a Passos Mágicos (contrato de dados, "
                "seção 7) — ajuste livremente para ver como a classificação muda."
            ),
        )
        if resultado["probabilidade"] >= limiar:
            st.warning(f"Classificação com o limiar atual ({limiar:.0%}): **em risco**")
        else:
            st.success(f"Classificação com o limiar atual ({limiar:.0%}): **não em risco**")

        st.markdown("**Indicadores que mais pesaram nesta previsão:**")
        if resultado["explicacao"]:
            for item in resultado["explicacao"]:
                icone = ":material/trending_up:" if item["contribuicao"] > 0 else ":material/trending_down:"
                st.markdown(f"- {icone} **{item['feature']}** {item['direcao']}")
        else:
            st.caption("Nenhum indicador teve peso relevante nesta previsão.")

    with st.expander("Referência de desempenho do modelo (validação temporal)"):
        st.caption(metadados["metricas_referencia"]["nota"])
        st.write(
            f"Acurácia: {metricas_ref['accuracy']:.3f} · "
            f"F1 macro: {metricas_ref['f1_macro']:.3f} · "
            f"ROC AUC: {metricas_ref['roc_auc']:.3f}"
        )


def renderizar_limitacoes() -> None:
    with st.expander("Limitações do modelo", icon=":material/info:"):
        st.markdown(
            "- A validação foi feita com treino em 2022 e teste em 2023/2024, com amostras "
            "de poucas centenas de alunos por ano — o resultado pode não generalizar para "
            "públicos muito diferentes do atendido pela Passos Mágicos nesse período.\n"
            "- O modelo ainda não tem monitoramento de deriva de dados. Quando uma nova PEDE "
            "entrar, a distribuição dos indicadores de entrada deveria ser comparada com a do "
            "treino antes de confiar nas previsões, e retreinamento periódico é esperado como "
            "próximo passo.\n"
            "- A probabilidade exibida é uma estimativa estatística, não um diagnóstico "
            "individual do aluno."
        )


def main() -> None:
    st.set_page_config(page_title="Risco de defasagem — Passos Mágicos", page_icon=":material/school:")
    st.title("Avaliação de risco de defasagem")
    st.caption(
        "Ferramenta de apoio à decisão a partir de indicadores PEDE digitados manualmente. "
        "Nenhum dado de aluno real é armazenado, buscado ou exibido nesta tela."
    )

    aba_risco, aba_incidencia = st.tabs([TITULOS[ALVO_RISCO_FUTURO], TITULOS[ALVO_INCIDENCIA]])
    with aba_risco:
        renderizar_formulario(ALVO_RISCO_FUTURO)
    with aba_incidencia:
        renderizar_formulario(ALVO_INCIDENCIA)

    renderizar_limitacoes()


main()
