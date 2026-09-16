"""
Teste de fumaça de src/data_prep.py.

Roda build_painel() e build_painel_com_alvo() contra a base real
(data/raw/base_bronze.xlsx) e confere que o shape resultante é plausível.
Não hardcoda números exatos de linhas/valores porque a base é um dado real
que pode ser atualizado — em vez disso, compara o painel contra o que as
próprias abas brutas reportam (ex.: soma de linhas) e checa invariantes
estruturais (colunas esperadas, anos esperados, ausência de vazamento).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_prep import (  # noqa: E402
    RAW_XLSX_PATH,
    build_painel,
    build_painel_com_alvo,
    carregar_abas_brutas,
)

COLUNAS_ESPERADAS = {
    "ra",
    "ano",
    "fase_num",
    "fase_ideal_num",
    "defasagem_calculada",
    "defasagem_fornecida",
    "inde",
    "pedra",
    "ian",
    "ida",
    "ieg",
    "iaa",
    "ips",
    "ipp",
    "ipv",
}


def test_build_painel_tem_shape_plausivel():
    abas = carregar_abas_brutas(RAW_XLSX_PATH)
    total_linhas_brutas = sum(len(df) for df in abas.values())

    painel = build_painel(RAW_XLSX_PATH, verbose=False)

    # Painel longo: 1 linha por aluno-ano, nenhuma linha perdida ou duplicada
    # na harmonização/empilhamento das 3 abas.
    assert len(painel) == total_linhas_brutas
    assert set(painel["ano"].unique()) == {2022, 2023, 2024}
    assert COLUNAS_ESPERADAS.issubset(painel.columns)

    # fase_num/fase_ideal_num precisam ter sido extraídos pra quase todas as
    # linhas: uma taxa baixa indicaria que _extrair_numero_fase não cobre
    # algum formato novo de Fase.
    assert painel["fase_num"].notna().mean() > 0.95
    assert painel["fase_ideal_num"].notna().mean() > 0.95

    # IPP só existe a partir de 2023: em 2022 tem que ser 100% ausente, e em
    # 2023/2024 tem que ter uma taxa de preenchimento razoável.
    ipp_2022 = painel.loc[painel["ano"] == 2022, "ipp"]
    ipp_2023 = painel.loc[painel["ano"] == 2023, "ipp"]
    assert ipp_2022.notna().sum() == 0
    assert ipp_2023.notna().mean() > 0.5


def test_build_painel_com_alvo_nao_vaza_e_tem_na_no_ultimo_ano():
    painel = build_painel(RAW_XLSX_PATH, verbose=False)
    painel_com_alvo = build_painel_com_alvo(painel)

    assert len(painel_com_alvo) == len(painel)
    assert "alvo_risco_defasagem_prox_ano" in painel_com_alvo.columns

    # 2024 é o último ano da base: como não existe PEDE2025, nenhuma linha de
    # 2024 pode ter o alvo definido (senão haveria vazamento/erro de lógica).
    alvo_2024 = painel_com_alvo.loc[painel_com_alvo["ano"] == 2024, "alvo_risco_defasagem_prox_ano"]
    assert alvo_2024.isna().all()

    # 2022 tem ano seguinte (2023) na base: uma fração razoável de alunos
    # (nem toda, por evasão/entrada) deve ter alvo definido, e ele deve ser
    # estritamente binário.
    alvo_2022 = painel_com_alvo.loc[painel_com_alvo["ano"] == 2022, "alvo_risco_defasagem_prox_ano"]
    assert alvo_2022.notna().mean() > 0.3
    assert set(alvo_2022.dropna().unique()).issubset({0.0, 1.0})
