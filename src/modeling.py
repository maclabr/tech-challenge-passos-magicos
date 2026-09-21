"""Dados, pipelines e métricas para os modelos temporais de risco de defasagem."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42
ALVO_RISCO_FUTURO = "risco_futuro"
ALVO_INCIDENCIA = "incidencia_nova_defasagem"
TIPOS_ALVO = (ALVO_RISCO_FUTURO, ALVO_INCIDENCIA)

# Apenas sinais conhecidos no ano de predição e disponíveis em 2022 e 2023.
# INDE e Pedra ficam fora: o primeiro é composto dos indicadores e a segunda
# tem divergência de regra documentada. IPP não existe na aba PEDE2022.
FEATURES_NUMERICAS = (
    "FASE", "FASE_IDEAL", "DEFASAGEM_CALCULADA", "IAN", "IDA", "IEG",
    "IAA", "IPS", "IPV", "NOTA_MATEMATICA", "NOTA_PORTUGUES",
    "NOTA_INGLES", "IDADE_ANOS", "ANO_INGRESSO",
)


def preparar_dataset_modelagem(painel: pd.DataFrame, tipo_alvo: str) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Retorna X, y e ano para o alvo solicitado, sem RA nem dados futuros."""
    if tipo_alvo not in TIPOS_ALVO:
        raise ValueError(f"tipo_alvo deve ser um de {TIPOS_ALVO}; recebido: {tipo_alvo!r}")
    faltantes = set((*FEATURES_NUMERICAS, "ANO", "ALVO_RISCO_DEFASAGEM_PROX_ANO")) - set(painel.columns)
    if faltantes:
        raise ValueError(f"Colunas ausentes para modelagem: {sorted(faltantes)}")

    dados = painel.dropna(subset=["ALVO_RISCO_DEFASAGEM_PROX_ANO"]).copy()
    if tipo_alvo == ALVO_INCIDENCIA:
        dados = dados.loc[dados["DEFASAGEM_CALCULADA"] >= 0].copy()

    x = dados.loc[:, FEATURES_NUMERICAS].copy()
    y = dados["ALVO_RISCO_DEFASAGEM_PROX_ANO"].astype(int)
    anos = dados["ANO"].astype(int)
    return x, y, anos


def criar_pipeline_logistico() -> Pipeline:
    """Pipeline determinístico com imputação treinada somente no conjunto de treino."""
    return Pipeline(
        steps=[
            ("imputador", SimpleImputer(strategy="median", add_indicator=True)),
            ("escala", StandardScaler()),
            ("modelo", LogisticRegression(class_weight="balanced", max_iter=2_000, random_state=RANDOM_STATE)),
        ]
    )


def criar_pipeline_random_forest() -> Pipeline:
    """Pipeline de árvores; reaproveita a imputação mediana, mas dispensa escala."""
    return Pipeline(
        steps=[
            ("imputador", SimpleImputer(strategy="median", add_indicator=True)),
            ("modelo", RandomForestClassifier(class_weight="balanced", random_state=RANDOM_STATE)),
        ]
    )


def criar_pipeline_gradient_boosting() -> Pipeline:
    """HistGradientBoostingClassifier aceita NaN nativamente; pipeline de 1 passo por consistência de interface."""
    return Pipeline(
        steps=[
            ("modelo", HistGradientBoostingClassifier(random_state=RANDOM_STATE)),
        ]
    )


def criar_baseline() -> DummyClassifier:
    """Baseline que prevê a classe mais frequente do treino."""
    return DummyClassifier(strategy="prior", random_state=RANDOM_STATE)


def separar_treino_teste_temporal(x: pd.DataFrame, y: pd.Series, anos: pd.Series, ano_treino: int = 2022, ano_teste: int = 2023):
    """Separa coortes por ano; falha se a separação não possuir as duas classes."""
    treino = anos.eq(ano_treino)
    teste = anos.eq(ano_teste)
    if not treino.any() or not teste.any():
        raise ValueError("Os anos de treino e teste precisam ter linhas rotuladas.")
    if y.loc[treino].nunique() < 2 or y.loc[teste].nunique() < 2:
        raise ValueError("Treino e teste precisam conter as duas classes para avaliação.")
    return x.loc[treino], x.loc[teste], y.loc[treino], y.loc[teste]


def calcular_metricas_operacionais(y_verdadeiro: pd.Series, probabilidades: np.ndarray, limiar: float = 0.5) -> dict[str, float]:
    """Métricas de discriminação, calibração e operação para um limiar explícito."""
    previsoes = (np.asarray(probabilidades) >= limiar).astype(int)
    return {
        "n": int(len(y_verdadeiro)),
        "prevalencia": float(y_verdadeiro.mean()),
        "limiar": float(limiar),
        "taxa_alerta": float(previsoes.mean()),
        "accuracy": accuracy_score(y_verdadeiro, previsoes),
        "precision": precision_score(y_verdadeiro, previsoes, zero_division=0),
        "recall": recall_score(y_verdadeiro, previsoes, zero_division=0),
        "f1": f1_score(y_verdadeiro, previsoes, zero_division=0),
        "f1_macro": f1_score(y_verdadeiro, previsoes, average="macro", zero_division=0),
        "roc_auc": roc_auc_score(y_verdadeiro, probabilidades),
        "pr_auc": average_precision_score(y_verdadeiro, probabilidades),
        "brier": brier_score_loss(y_verdadeiro, probabilidades),
        "falsos_negativos": int(((y_verdadeiro.to_numpy() == 1) & (previsoes == 0)).sum()),
        "falsos_positivos": int(((y_verdadeiro.to_numpy() == 0) & (previsoes == 1)).sum()),
    }


def _divisor_cv_estratificado(y_treino: pd.Series, cv: int) -> StratifiedKFold:
    """Reduz o número de folds até o maior valor que ainda funciona, com mínimo de 3.

    A classe minoritária do treino pode ser pequena (a base de incidência é bem
    menor que a de risco futuro), então `cv` é ajustado ao tamanho dela.
    """
    contagem_classes = pd.Series(y_treino).value_counts()
    menor_classe = int(contagem_classes.min())
    cv_efetivo = max(min(cv, menor_classe), 3)
    if cv_efetivo != cv:
        print(
            f"Aviso: cv reduzido de {cv} para {cv_efetivo} porque a classe minoritária do "
            f"treino tem {menor_classe} amostras."
        )
    return StratifiedKFold(n_splits=cv_efetivo, shuffle=True, random_state=RANDOM_STATE)


def selecionar_modelo_por_cv(
    x_treino: pd.DataFrame,
    y_treino: pd.Series,
    candidatos: dict[str, Pipeline],
    cv: int = 5,
    scoring: str = "average_precision",
) -> tuple[pd.DataFrame, str]:
    """Seleciona entre candidatos só por CV estratificado no treino.

    O teste temporal (2023→2024) nunca entra aqui: por convenção do projeto, ele é
    informativo, não decisório.
    """
    divisor = _divisor_cv_estratificado(y_treino, cv)
    resultados = []
    for nome, pipeline in candidatos.items():
        scores = cross_val_score(pipeline, x_treino, y_treino, cv=divisor, scoring=scoring)
        resultados.append({"modelo": nome, "media_cv": scores.mean(), "desvio_cv": scores.std()})

    tabela = pd.DataFrame(resultados).sort_values("media_cv", ascending=False).reset_index(drop=True)
    vencedor = tabela.loc[0, "modelo"]
    return tabela, vencedor


def buscar_hiperparametros_logistico(
    x_treino: pd.DataFrame,
    y_treino: pd.Series,
    cv: int = 5,
    scoring: str = "average_precision",
    grade_c: tuple[float, ...] = (0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100),
) -> tuple[pd.DataFrame, float]:
    """Busca só o `C` da regressão logística (vencedora da seleção) por CV no treino.

    Único candidato tunado por decisão de escopo: a regressão logística venceu a
    seleção nos dois problemas, então não há justificativa para tunar
    random forest/gradient boosting. O teste temporal (2023→2024) nunca entra
    aqui, pela mesma convenção de `selecionar_modelo_por_cv`.
    """
    divisor = _divisor_cv_estratificado(y_treino, cv)
    busca = GridSearchCV(
        criar_pipeline_logistico(),
        param_grid={"modelo__C": list(grade_c)},
        cv=divisor,
        scoring=scoring,
    )
    busca.fit(x_treino, y_treino)

    tabela = (
        pd.DataFrame(
            {
                "C": [float(parametros["modelo__C"]) for parametros in busca.cv_results_["params"]],
                "media_cv": busca.cv_results_["mean_test_score"],
                "desvio_cv": busca.cv_results_["std_test_score"],
            }
        )
        .sort_values("media_cv", ascending=False)
        .reset_index(drop=True)
    )
    melhor_c = float(busca.best_params_["modelo__C"])
    return tabela, melhor_c


def aplicar_calibracao(pipeline_vencedor: Pipeline, x_treino: pd.DataFrame, y_treino: pd.Series) -> CalibratedClassifierCV:
    """Calibra as probabilidades do pipeline vencedor só com dados de treino.

    `CalibratedClassifierCV` clona o estimador internamente, então não importa se
    `pipeline_vencedor` já foi ajustado antes — o ajuste de calibração usado é
    sempre o feito aqui dentro, exclusivamente em `x_treino`/`y_treino`.
    """
    calibrado = CalibratedClassifierCV(pipeline_vencedor, method="sigmoid", cv=5)
    calibrado.fit(x_treino, y_treino)
    return calibrado


def tabela_limiares(y_verdadeiro: pd.Series, probabilidades: np.ndarray, limiares: tuple[float, ...] = (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)) -> pd.DataFrame:
    """Expõe trade-offs sem escolher o limiar de produção sem regra de negócio."""
    return pd.DataFrame([calcular_metricas_operacionais(y_verdadeiro, probabilidades, limiar) for limiar in limiares])
