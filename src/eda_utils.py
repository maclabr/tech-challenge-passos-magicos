"""
Funções auxiliares da análise exploratória (Fase 5, notebook 02).

Reúne aqui só a lógica que se repete em mais de uma pergunta de negócio,
filtrar alunos com histórico em vários anos, e montar pares de anos
consecutivos por aluno, para não duplicar o mesmo `groupby`/`merge` em
cada célula do notebook. Trabalha sobre o painel já padronizado (colunas em
maiúsculo: `RA`, `ANO`, etc.), o formato salvo em
`data/processed/pede_painel_consolidado.csv`.
"""

from __future__ import annotations

import pandas as pd


def filtrar_alunos_com_todos_os_anos(painel: pd.DataFrame, anos: tuple[int, ...] | None = None) -> pd.DataFrame:
    """
    Restringe `painel` às linhas dos alunos (RA) que têm registro em TODOS
    os anos pedidos (por padrão, todos os anos presentes em `painel`).

    A maioria dos alunos NÃO tem histórico nos 3 anos da base (só 468 de
    1.661 RAs aparecem em 2022+2023+2024, os demais entraram, saíram ou
    faltaram a alguma edição da PEDE). Qualquer pergunta sobre evolução ou
    comportamento ao longo do tempo só pode ser respondida para quem tem
    esse histórico completo, e este filtro deixa explícito que o resultado
    vale para esse subconjunto menor, não para a base toda.
    """
    if anos is None:
        anos = tuple(sorted(painel["ANO"].unique()))
    anos_pedidos = set(anos)
    tem_todos_os_anos = painel.groupby("RA")["ANO"].agg(lambda anos_do_aluno: anos_pedidos.issubset(set(anos_do_aluno)))
    ras_com_historico_completo = tem_todos_os_anos[tem_todos_os_anos].index
    return painel[painel["RA"].isin(ras_com_historico_completo) & painel["ANO"].isin(anos_pedidos)].copy()


def construir_pares_anos_consecutivos(painel: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    """
    Para cada aluno (RA) com registro em dois anos consecutivos (N e N+1),
    monta uma linha com `RA`, `ANO` (o ano N, ano de referência do par) e
    as colunas de `colunas` duplicadas com sufixo `_N` (valor no ano N) e
    `_N1` (valor no ano seguinte).

    Usa o mesmo truque de `build_painel_com_alvo` (em `src/data_prep.py`):
    subtrai 1 do "ano seguinte" antes do merge para casar cada linha com a
    linha do ano anterior do mesmo aluno. É um join interno, alunos sem o
    ano seguinte na base (evasão) ou sem o ano anterior (ingresso) não geram
    par, então o número de pares é sempre menor que o número de linhas do
    painel, nunca precisa ser tratado como erro.
    """
    colunas_com_chave = ["RA", "ANO", *colunas]
    ano_atual = painel[colunas_com_chave].copy()
    ano_seguinte = painel[colunas_com_chave].copy()
    ano_seguinte["ANO"] -= 1
    return ano_atual.merge(ano_seguinte, on=["RA", "ANO"], suffixes=("_N", "_N1"))
