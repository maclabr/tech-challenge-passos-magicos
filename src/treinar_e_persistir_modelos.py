"""Treina os pipelines de produção (risco futuro e incidência) e persiste em models/.

Uso: python -m src.treinar_e_persistir_modelos
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import joblib
import pandas as pd

from src.modeling import ALVO_INCIDENCIA, ALVO_RISCO_FUTURO, FEATURES_NUMERICAS, RANDOM_STATE, treinar_pipeline_final

CAMINHO_PAINEL = Path("data/processed/pede_painel_consolidado.csv")
DIRETORIO_MODELOS = Path("models")

# Métricas do teste temporal auditado (2022 -> 2023/2024), documentadas no notebook 03.
# NÃO são as métricas do modelo de produção retreinado aqui com mais dado (treino +
# validação combinados) — servem só como referência de expectativa de desempenho.
METRICAS_REFERENCIA = {
    ALVO_RISCO_FUTURO: {
        "accuracy": 0.725,
        "f1_macro": 0.713,
        "roc_auc": 0.831,
    },
    ALVO_INCIDENCIA: {
        "accuracy": 0.676,
        "f1_macro": 0.534,
        "roc_auc": 0.693,
    },
}

NOMES_ARQUIVO = {
    ALVO_RISCO_FUTURO: "pipeline_risco_futuro",
    ALVO_INCIDENCIA: "pipeline_incidencia_nova_defasagem",
}


def main() -> None:
    DIRETORIO_MODELOS.mkdir(parents=True, exist_ok=True)
    painel = pd.read_csv(CAMINHO_PAINEL)

    for tipo_alvo in (ALVO_RISCO_FUTURO, ALVO_INCIDENCIA):
        pipeline_calibrado, pipeline_explicativo = treinar_pipeline_final(painel, tipo_alvo)
        nome_base = NOMES_ARQUIVO[tipo_alvo]

        joblib.dump(pipeline_calibrado, DIRETORIO_MODELOS / f"{nome_base}.joblib")
        joblib.dump(pipeline_explicativo, DIRETORIO_MODELOS / f"{nome_base}_explicativo.joblib")
        print(f"Pipelines salvos para {tipo_alvo!r}.")

    metadados = {
        "features_numericas": list(FEATURES_NUMERICAS),
        "random_state": RANDOM_STATE,
        "data_treino": date.today().isoformat(),
        "metricas_referencia": {
            "nota": (
                "Métricas da validação temporal auditada (treino 2022 -> teste 2023/2024), "
                "documentadas no notebook 03. Não são métricas do modelo de produção "
                "persistido aqui, que é retreinado em todo o histórico rotulado disponível."
            ),
            "por_alvo": METRICAS_REFERENCIA,
        },
    }
    with open(DIRETORIO_MODELOS / "metadados.json", "w", encoding="utf-8") as arquivo:
        json.dump(metadados, arquivo, ensure_ascii=False, indent=2)
    print("Metadados salvos em models/metadados.json.")


if __name__ == "__main__":
    main()
