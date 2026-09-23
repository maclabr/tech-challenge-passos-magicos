"""Contratos dos conjuntos temporais usados pelos modelos de risco."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.pipeline import Pipeline

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.modeling import (  # noqa: E402
    ALVO_INCIDENCIA,
    ALVO_RISCO_FUTURO,
    FEATURES_NUMERICAS,
    RANDOM_STATE,
    aplicar_calibracao,
    buscar_hiperparametros_logistico,
    calcular_metricas_operacionais,
    criar_baseline,
    criar_pipeline_gradient_boosting,
    criar_pipeline_logistico,
    criar_pipeline_random_forest,
    preparar_dataset_modelagem,
    selecionar_modelo_por_cv,
    separar_treino_teste_temporal,
)

# 3 linhas por combinação (ano, alvo, defasagem), o mínimo para que a classe
# minoritária do treino (2022) sustente o piso de 3 folds de
# `selecionar_modelo_por_cv` sem erro.
_REPETICOES_POR_COMBO = 3


def _painel_minimo() -> pd.DataFrame:
    linhas = []
    for ano, alvo, defasagem in [(2022, 0, 0), (2022, 1, -1), (2023, 0, 0), (2023, 1, -1)]:
        for _ in range(_REPETICOES_POR_COMBO):
            linha = {coluna: 1.0 for coluna in FEATURES_NUMERICAS}
            linha.update({"ANO": ano, "ALVO_RISCO_DEFASAGEM_PROX_ANO": alvo, "DEFASAGEM_CALCULADA": defasagem})
            linhas.append(linha)
    return pd.DataFrame(linhas)


def _dataset_sintetico_separavel(n_por_classe: int = 15) -> tuple[pd.DataFrame, pd.Series]:
    """Duas classes bem separadas por uma única feature, cenário simples e determinístico para CV."""
    rng = np.random.default_rng(RANDOM_STATE)
    x = pd.DataFrame(
        {
            "IAN": np.concatenate(
                [rng.normal(2.0, 0.3, n_por_classe), rng.normal(8.0, 0.3, n_por_classe)]
            ),
            "IDA": rng.normal(5.0, 1.0, 2 * n_por_classe),
        }
    )
    y = pd.Series([0] * n_por_classe + [1] * n_por_classe)
    return x, y


def test_risco_futuro_usa_todos_os_registros_rotulados_sem_id():
    x, y, anos = preparar_dataset_modelagem(_painel_minimo(), ALVO_RISCO_FUTURO)

    assert list(x.columns) == list(FEATURES_NUMERICAS)
    assert len(x) == len(y) == len(anos) == 4 * _REPETICOES_POR_COMBO
    assert set(y) == {0, 1}


def test_incidencia_restringe_a_quem_nao_estava_defasado():
    x, y, anos = preparar_dataset_modelagem(_painel_minimo(), ALVO_INCIDENCIA)

    assert len(x) == 2 * _REPETICOES_POR_COMBO
    assert (x["DEFASAGEM_CALCULADA"] >= 0).all()
    assert set(anos) == {2022, 2023}


def test_separacao_temporal_nao_mistura_os_anos():
    x, y, anos = preparar_dataset_modelagem(_painel_minimo(), ALVO_RISCO_FUTURO)
    x_treino, x_teste, y_treino, y_teste = separar_treino_teste_temporal(x, y, anos)

    assert len(x_treino) == len(y_treino) == 2 * _REPETICOES_POR_COMBO
    assert len(x_teste) == len(y_teste) == 2 * _REPETICOES_POR_COMBO


def test_pipeline_random_forest_tem_imputador_e_random_state():
    pipeline = criar_pipeline_random_forest()

    assert isinstance(pipeline, Pipeline)
    assert "imputador" in pipeline.named_steps
    modelo = pipeline.named_steps["modelo"]
    assert isinstance(modelo, RandomForestClassifier)
    assert modelo.random_state == RANDOM_STATE
    assert modelo.class_weight == "balanced"


def test_pipeline_gradient_boosting_dispensa_imputador_mas_usa_random_state():
    pipeline = criar_pipeline_gradient_boosting()

    assert isinstance(pipeline, Pipeline)
    assert len(pipeline.steps) == 1
    modelo = pipeline.named_steps["modelo"]
    assert isinstance(modelo, HistGradientBoostingClassifier)
    assert modelo.random_state == RANDOM_STATE


def test_calcular_metricas_operacionais_inclui_accuracy_e_f1_macro():
    y_verdadeiro = pd.Series([0, 0, 1, 1])
    probabilidades = np.array([0.1, 0.4, 0.6, 0.9])

    metricas = calcular_metricas_operacionais(y_verdadeiro, probabilidades)

    assert metricas["accuracy"] == 1.0
    assert 0.0 <= metricas["f1_macro"] <= 1.0
    # chaves antigas continuam presentes, não substituídas
    for chave in ("precision", "recall", "f1", "roc_auc", "pr_auc", "brier", "falsos_negativos", "falsos_positivos"):
        assert chave in metricas


def test_selecionar_modelo_por_cv_escolhe_o_modelo_que_separa_as_classes():
    x, y = _dataset_sintetico_separavel()
    candidatos = {
        "baseline": criar_baseline(),
        "logistica": criar_pipeline_logistico(),
    }

    tabela, vencedor = selecionar_modelo_por_cv(x, y, candidatos, cv=5)

    assert vencedor == "logistica"
    assert list(tabela.columns) == ["modelo", "media_cv", "desvio_cv"]
    assert tabela.iloc[0]["modelo"] == vencedor
    assert tabela["media_cv"].is_monotonic_decreasing


def test_selecionar_modelo_por_cv_reduz_cv_quando_classe_minoritaria_e_pequena(capsys):
    x = pd.DataFrame({"IAN": [1.0, 1.2, 0.9, 9.0, 9.5, 8.7]})
    y = pd.Series([0, 0, 0, 1, 1, 1])
    candidatos = {"baseline": criar_baseline()}

    tabela, vencedor = selecionar_modelo_por_cv(x, y, candidatos, cv=5)

    saida = capsys.readouterr().out
    assert "reduzido" in saida
    assert vencedor == "baseline"
    assert len(tabela) == 1


def test_buscar_hiperparametros_logistico_retorna_c_da_grade_e_tabela_ordenada():
    x, y = _dataset_sintetico_separavel()
    grade_c = (0.01, 0.1, 1, 10, 100)

    tabela, melhor_c = buscar_hiperparametros_logistico(x, y, cv=5, grade_c=grade_c)

    assert melhor_c in grade_c
    assert sorted(tabela["C"]) == sorted(grade_c)
    assert len(tabela) == len(grade_c)
    assert tabela["media_cv"].is_monotonic_decreasing
    assert tabela.iloc[0]["C"] == melhor_c


def test_aplicar_calibracao_retorna_classificador_calibrado_ajustado():
    x, y = _dataset_sintetico_separavel()
    pipeline_vencedor = criar_pipeline_logistico()

    calibrado = aplicar_calibracao(pipeline_vencedor, x, y)

    assert isinstance(calibrado, CalibratedClassifierCV)
    assert calibrado.method == "sigmoid"
    probabilidades = calibrado.predict_proba(x)[:, 1]
    assert probabilidades.shape[0] == len(y)
    assert ((probabilidades >= 0) & (probabilidades <= 1)).all()
