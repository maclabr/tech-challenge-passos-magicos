"""Contratos dos conjuntos temporais usados pelos modelos de risco."""

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.modeling import (  # noqa: E402
    ALVO_INCIDENCIA,
    ALVO_RISCO_FUTURO,
    FEATURES_NUMERICAS,
    preparar_dataset_modelagem,
    separar_treino_teste_temporal,
)


def _painel_minimo() -> pd.DataFrame:
    linhas = []
    for ano, alvo, defasagem in [(2022, 0, 0), (2022, 1, -1), (2023, 0, 0), (2023, 1, -1)]:
        linha = {coluna: 1.0 for coluna in FEATURES_NUMERICAS}
        linha.update({"ANO": ano, "ALVO_RISCO_DEFASAGEM_PROX_ANO": alvo, "DEFASAGEM_CALCULADA": defasagem})
        linhas.append(linha)
    return pd.DataFrame(linhas)


def test_risco_futuro_usa_todos_os_registros_rotulados_sem_id():
    x, y, anos = preparar_dataset_modelagem(_painel_minimo(), ALVO_RISCO_FUTURO)

    assert list(x.columns) == list(FEATURES_NUMERICAS)
    assert len(x) == len(y) == len(anos) == 4
    assert set(y) == {0, 1}


def test_incidencia_restringe_a_quem_nao_estava_defasado():
    x, y, anos = preparar_dataset_modelagem(_painel_minimo(), ALVO_INCIDENCIA)

    assert len(x) == 2
    assert (x["DEFASAGEM_CALCULADA"] >= 0).all()
    assert set(anos) == {2022, 2023}


def test_separacao_temporal_nao_mistura_os_anos():
    x, y, anos = preparar_dataset_modelagem(_painel_minimo(), ALVO_RISCO_FUTURO)
    x_treino, x_teste, y_treino, y_teste = separar_treino_teste_temporal(x, y, anos)

    assert len(x_treino) == len(y_treino) == 2
    assert len(x_teste) == len(y_teste) == 2
