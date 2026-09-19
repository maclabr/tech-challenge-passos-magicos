"""Regras estáveis de qualidade para o painel PEDE harmonizado."""

import sys
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_prep import (  # noqa: E402
    RAW_XLSX_PATH,
    build_painel,
    build_painel_com_alvo,
    padronizar_nomes_e_categorias,
)


INDICADORES = ["ian", "ida", "ieg", "iaa", "ips", "ipp", "ipv"]


def _painel_com_alvo() -> pd.DataFrame:
    return build_painel_com_alvo(build_painel(RAW_XLSX_PATH, verbose=False))


def test_grao_e_chave_do_painel_sao_validos():
    painel = _painel_com_alvo()

    assert not painel.duplicated(["ra", "ano"]).any()
    assert painel[["ra", "ano", "fase_num", "fase_ideal_num", "defasagem_calculada"]].notna().all().all()
    assert set(painel["ano"].unique()) == {2022, 2023, 2024}


def test_defasagem_calculada_reconcilia_com_a_fornecida():
    painel = _painel_com_alvo()
    comparavel = painel.dropna(subset=["defasagem_calculada", "defasagem_fornecida"])

    # Toleramos ocorrências pontuais da fonte, mas uma queda relevante indica
    # quebra no parsing de Fase ou Fase Ideal.
    assert (comparavel["defasagem_calculada"] == comparavel["defasagem_fornecida"]).mean() >= 0.995


def test_faixas_dos_indicadores_e_ausencia_estrutural():
    painel = _painel_com_alvo()

    for indicador in INDICADORES:
        valores = painel[indicador].dropna()
        assert valores.ge(0).all(), f"{indicador} contém valor negativo"
        # IAA/IPV possuem arredondamentos residuais acima de 10 na fonte.
        assert valores.le(10.01).all(), f"{indicador} excede o limite tolerado"

    assert painel.loc[painel["ano"] == 2022, "ipp"].isna().all()
    assert painel.loc[painel["ano"] == 2023, "ipp"].notna().mean() > 0.5


def test_alvo_temporal_nao_observa_o_ultimo_ano_nem_usa_valores_invalidos():
    painel = _painel_com_alvo()

    assert painel.loc[painel["ano"] == 2024, "alvo_risco_defasagem_prox_ano"].isna().all()
    valores_observados = painel["alvo_risco_defasagem_prox_ano"].dropna()
    assert set(valores_observados.unique()).issubset({0.0, 1.0})
    assert painel.loc[painel["ano"] == 2022, "alvo_risco_defasagem_prox_ano"].notna().mean() > 0.5
    assert painel.loc[painel["ano"] == 2023, "alvo_risco_defasagem_prox_ano"].notna().mean() > 0.5


def test_alvo_usa_exatamente_o_mesmo_ra_no_ano_seguinte():
    painel = pd.DataFrame(
        {
            "ra": [1, 1, 1, 2, 2],
            "ano": [2022, 2023, 2024, 2022, 2024],
            "defasagem_calculada": [0, -1, 0, 0, -1],
        }
    )
    resultado = build_painel_com_alvo(painel)

    assert resultado.loc[(resultado["ra"] == 1) & (resultado["ano"] == 2022), "alvo_risco_defasagem_prox_ano"].item() == 1
    assert resultado.loc[(resultado["ra"] == 1) & (resultado["ano"] == 2023), "alvo_risco_defasagem_prox_ano"].item() == 0
    assert resultado.loc[(resultado["ra"] == 1) & (resultado["ano"] == 2024), "alvo_risco_defasagem_prox_ano"].isna().item()
    assert resultado.loc[(resultado["ra"] == 2) & (resultado["ano"] == 2022), "alvo_risco_defasagem_prox_ano"].isna().item()


def test_csv_processado_e_reproducao_exata_da_transformacao():
    reconstruido = padronizar_nomes_e_categorias(_painel_com_alvo())
    salvo = pd.read_csv(RAW_XLSX_PATH.parent.parent / "processed" / "pede_painel_consolidado.csv")

    assert_frame_equal(reconstruido.reset_index(drop=True), salvo.reset_index(drop=True), check_dtype=False, check_exact=False)
