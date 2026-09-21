"""Testes do pipeline de produção: treino final, calibração e explicação por instância."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.modeling import (  # noqa: E402
    ALVO_INCIDENCIA,
    ALVO_RISCO_FUTURO,
    FEATURES_NUMERICAS,
    explicar_previsao,
    treinar_pipeline_final,
)

# 3 linhas por combinação (ano, alvo, defasagem) — o mesmo piso usado em
# test_modeling.py para sustentar os 3 folds mínimos da calibração (cv=5 reduz
# até esse piso quando a classe minoritária é pequena).
_REPETICOES_POR_COMBO = 3


def _painel_minimo() -> pd.DataFrame:
    # DEFASAGEM_CALCULADA sempre >= 0 para que o filtro de ALVO_INCIDENCIA
    # (preparar_dataset_modelagem) preserve as duas classes de alvo também.
    linhas = []
    for ano, alvo in [(2022, 0), (2022, 1), (2023, 0), (2023, 1)]:
        for indice in range(_REPETICOES_POR_COMBO):
            linha = {coluna: float(indice + 1) for coluna in FEATURES_NUMERICAS}
            linha.update({"ANO": ano, "ALVO_RISCO_DEFASAGEM_PROX_ANO": alvo, "DEFASAGEM_CALCULADA": 0})
            linhas.append(linha)
    return pd.DataFrame(linhas)


def test_treinar_pipeline_final_para_risco_futuro():
    pipeline_calibrado, pipeline_explicativo = treinar_pipeline_final(_painel_minimo(), ALVO_RISCO_FUTURO)

    assert isinstance(pipeline_calibrado, CalibratedClassifierCV)
    assert isinstance(pipeline_explicativo, Pipeline)
    # ambos foram ajustados: coef_ só existe depois do fit
    modelo = pipeline_explicativo.named_steps["modelo"]
    assert hasattr(modelo, "coef_")


def test_treinar_pipeline_final_para_incidencia():
    pipeline_calibrado, pipeline_explicativo = treinar_pipeline_final(_painel_minimo(), ALVO_INCIDENCIA)

    assert isinstance(pipeline_calibrado, CalibratedClassifierCV)
    assert isinstance(pipeline_explicativo, Pipeline)
    modelo = pipeline_explicativo.named_steps["modelo"]
    assert hasattr(modelo, "coef_")


def test_predict_proba_do_pipeline_calibrado_fica_em_zero_um():
    painel = _painel_minimo()
    pipeline_calibrado, _ = treinar_pipeline_final(painel, ALVO_RISCO_FUTURO)
    x = painel.loc[:, FEATURES_NUMERICAS]

    probabilidades = pipeline_calibrado.predict_proba(x)[:, 1]

    assert ((probabilidades >= 0) & (probabilidades <= 1)).all()


def test_explicar_previsao_retorna_apenas_features_de_negocio():
    painel = _painel_minimo()
    _, pipeline_explicativo = treinar_pipeline_final(painel, ALVO_RISCO_FUTURO)
    x_uma_linha = painel.loc[[0], FEATURES_NUMERICAS]

    explicacao = explicar_previsao(pipeline_explicativo, x_uma_linha, top_n=3)

    assert len(explicacao) <= 3
    for item in explicacao:
        assert item["feature"] in FEATURES_NUMERICAS
        assert not item["feature"].startswith("missingindicator_")
        assert item["direcao"] in {"aumenta o risco", "reduz o risco"}
        assert isinstance(item["contribuicao"], float)


def test_linha_totalmente_ausente_nao_quebra_previsao_nem_explicacao():
    painel = _painel_minimo()
    pipeline_calibrado, pipeline_explicativo = treinar_pipeline_final(painel, ALVO_RISCO_FUTURO)
    x_ausente = pd.DataFrame([{coluna: np.nan for coluna in FEATURES_NUMERICAS}])

    probabilidades = pipeline_calibrado.predict_proba(x_ausente)[:, 1]
    assert ((probabilidades >= 0) & (probabilidades <= 1)).all()

    explicacao = explicar_previsao(pipeline_explicativo, x_ausente, top_n=3)
    assert len(explicacao) <= 3
    for item in explicacao:
        assert item["feature"] in FEATURES_NUMERICAS
