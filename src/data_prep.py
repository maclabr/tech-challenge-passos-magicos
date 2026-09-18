"""
Funções de preparação de dados do Datathon Passos Mágicos (Fase 5).

O arquivo bruto (data/raw/base_bronze.xlsx) tem 3 abas — PEDE2022, PEDE2023 e
PEDE2024 — uma por edição da Pesquisa Extensiva do Desenvolvimento Educacional
(PEDE). Cada aba tem um conjunto DIFERENTE de nomes de coluna: os nomes mudam
de ano para ano, alguns indicadores (ex.: IPP) só passaram a existir a partir
de 2023, e o formato da coluna de Fase muda a cada ano. O dicionário de dados
oficial documenta um schema mais antigo (sufixos _2020/_2021/_2022) que NÃO
bate exatamente com as abas reais deste arquivo — por isso as funções abaixo
foram escritas a partir da inspeção direta das colunas de cada aba (ver
`inspecionar_abas`), não do dicionário.

As funções deste módulo harmonizam as três abas em um único painel longo (1
linha por aluno-ano), pronto para ser consumido por notebooks e, mais adiante,
por um pipeline de modelagem scikit-learn.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_STATE = 42

RAW_XLSX_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "base_bronze.xlsx"
SHEET_NAMES = ("PEDE2022", "PEDE2023", "PEDE2024")

# Faixas oficiais de Pedra por INDE (documento interno Passos Mágicos).
# Os limites são inclusivos nas duas pontas e se tocam entre faixas
# vizinhas (ex.: 5,506 é o teto de Quartzo E o piso de Ágata); a ordem da
# tupla resolve o empate de fronteira a favor da faixa mais baixa.
FAIXAS_PEDRA_POR_INDE = (
    (2.405, 5.506, "Quartzo"),
    (5.506, 6.868, "Ágata"),
    (6.868, 8.230, "Ametista"),
    (8.230, 9.294, "Topázio"),
)

# PEDE2022 usa "Menina"/"Menino"; PEDE2023-24 usam "Feminino"/"Masculino".
_MAPA_GENERO = {
    "Menina": "Feminino",
    "Menino": "Masculino",
    "Feminino": "Feminino",
    "Masculino": "Masculino",
}

# "Agata" (sem acento) aparece em 2023/2024, "Ágata" nas colunas históricas
# de 2022. "INCLUIR" aparece em Pedra 2024 para alunos cuja classificação
# ainda não foi fechada — não é uma categoria de Pedra válida, então vira
# ausente (NaN) em vez de ser tratada como uma 5ª pedra.
_MAPA_PEDRA = {
    "Agata": "Ágata",
    "Ágata": "Ágata",
    "Quartzo": "Quartzo",
    "Ametista": "Ametista",
    "Topázio": "Topázio",
    "INCLUIR": np.nan,
}

_PADRAO_PRIMEIRO_NUMERO = re.compile(r"(\d+)")
_PADRAO_CARACTER_NAO_ALFANUMERICO = re.compile(r"[^A-Za-z0-9 ]+")
_PADRAO_ESPACOS_REPETIDOS = re.compile(r"\s+")

# Colunas de texto/categóricas normalizadas por `padronizar_nomes_e_categorias`
# (já com o nome de destino, em maiúsculo).
_COLUNAS_CATEGORICAS_PARA_NORMALIZAR = ("GENERO", "PEDRA", "TURMA", "INSTITUICAO_ENSINO", "INDICADO", "ATINGIU_PV")

# Renomeios que não são um simples uppercase: tiram o sufixo "_num" ao
# padronizar (fase_num -> FASE, fase_ideal_num -> FASE_IDEAL).
_RENOMEIO_COLUNA_ESPECIAL = {"fase_num": "FASE", "fase_ideal_num": "FASE_IDEAL"}


def carregar_abas_brutas(raw_path: Path | str = RAW_XLSX_PATH) -> dict[str, pd.DataFrame]:
    """Lê as 3 abas do PEDE (2022, 2023, 2024) do Excel bruto e retorna {aba: DataFrame}, sem nenhuma transformação."""
    planilha = pd.ExcelFile(raw_path)
    faltando = [aba for aba in SHEET_NAMES if aba not in planilha.sheet_names]
    if faltando:
        raise ValueError(f"Abas esperadas ausentes no arquivo: {faltando}. Abas encontradas: {planilha.sheet_names}")
    return {aba: planilha.parse(aba) for aba in SHEET_NAMES}


def inspecionar_abas(abas: dict[str, pd.DataFrame], verbose: bool = True) -> pd.DataFrame:
    """
    Monta (e, se `verbose`, imprime) um resumo de shape e colunas de cada aba bruta.

    Este é o PRIMEIRO passo antes de qualquer harmonização: como o dicionário
    de dados oficial documenta um schema mais antigo que não bate com o
    arquivo real, a harmonização em `_harmonizar_ano` foi escrita a partir do
    que esta função reporta, não do dicionário.
    """
    linhas_resumo = []
    for aba, df in abas.items():
        linhas_resumo.append({"aba": aba, "n_linhas": len(df), "n_colunas": df.shape[1], "colunas": list(df.columns)})
        if verbose:
            print("=" * 80)
            print(f"{aba}: {df.shape[0]} linhas x {df.shape[1]} colunas")
            print(list(df.columns))
    return pd.DataFrame(linhas_resumo)


def _extrair_numero_fase(valor) -> float:
    """
    Extrai o nível numérico de uma célula de Fase ou Fase Ideal.

    O formato muda por ano e por coluna:
      - PEDE2022 / "Fase":         já vem como int (0-7).
      - PEDE2022 / "Fase ideal":   texto "ALFA  (2º e 3º ano)", "Fase 4 (9º ano)", ...
      - PEDE2023 / "Fase":         texto "ALFA", "FASE 1", ..., "FASE 8".
      - PEDE2023-24 / "Fase Ideal": texto "ALFA (1° e 2° ano)", "Fase 4 (9° ano)", ...
      - PEDE2024 / "Fase":         turma embutida no valor: "1A", "2B", ...,
                                    ou só o número sem letra ("9"), ou "ALFA".

    Em todos os casos "ALFA" (com ou sem sufixo) equivale ao nível 0. Nos
    demais casos, o primeiro grupo de dígitos da string é o nível de fase —
    em "Fase 4 (9º ano)" o primeiro número é sempre o nível da fase (o "4"),
    nunca o ano escolar entre parênteses, porque este último aparece depois
    na string.
    """
    if pd.isna(valor):
        return np.nan
    texto = str(valor).strip()
    if texto.upper().startswith("ALFA"):
        return 0.0
    encontrado = _PADRAO_PRIMEIRO_NUMERO.search(texto)
    return float(encontrado.group(1)) if encontrado else np.nan


def _extrair_numero_ra(valor) -> int:
    """Extrai o número inteiro do RA (ex.: "RA-1" -> 1), reaproveitando o mesmo padrão de `_extrair_numero_fase`."""
    encontrado = _PADRAO_PRIMEIRO_NUMERO.search(str(valor))
    if not encontrado:
        raise ValueError(f"RA sem número reconhecível: {valor!r}")
    return int(encontrado.group(1))


def _extrair_ano_nascimento(df: pd.DataFrame, ano: int) -> pd.Series:
    """
    Harmoniza o ano de nascimento a partir da coluna disponível em cada ano.

    PEDE2022 tem "Ano nasc" (int, direto). PEDE2023/2024 têm "Data de Nasc":
    em 2023 a coluna vem com tipos misturados (strings "m/d/yyyy" e objetos
    datetime já convertidos pelo Excel), em 2024 já vem como datetime puro —
    em ambos os casos `pd.to_datetime` normaliza e extraímos só o ano.
    """
    if ano == 2022:
        return pd.to_numeric(df["Ano nasc"], errors="coerce")
    return pd.to_datetime(df["Data de Nasc"], errors="coerce").dt.year


def _coluna_numerica_segura(df: pd.DataFrame, coluna: str) -> pd.Series:
    """Converte `df[coluna]` para numérico, ou devolve uma série de NaN (mesmo index) se a coluna não existir na aba."""
    if coluna not in df.columns:
        return pd.Series(np.nan, index=df.index, dtype=float)
    return pd.to_numeric(df[coluna], errors="coerce")


def _harmonizar_ano(df: pd.DataFrame, ano: int) -> pd.DataFrame:
    """
    Harmoniza uma única aba (um ano) para o esquema padronizado em
    snake_case usado no painel longo.

    Os nomes das colunas de origem mudam ano a ano — inclusive o indicador
    "atual" muda de nome: em 2022 o INDE do próprio ano está em "INDE 22",
    mas em 2023/2024 ele está em "INDE 2023"/"INDE 2024" (as colunas
    "INDE 23"/"Pedra 23" que aparecem em PEDE2023 são um campo legado vazio,
    não o valor do ano — confirmado na inspeção: 0 valores não nulos). Por
    isso o mapeamento de colunas é resolvido explicitamente por ano abaixo,
    em vez de tentar adivinhar um padrão único de nome.
    """
    if ano == 2022:
        col_fase, col_fase_ideal = "Fase", "Fase ideal"
        col_defasagem_fornecida = "Defas"
        col_inde, col_pedra = "INDE 22", "Pedra 22"
        col_mat, col_por, col_ing = "Matem", "Portug", "Inglês"
    elif ano in (2023, 2024):
        col_fase, col_fase_ideal = "Fase", "Fase Ideal"
        col_defasagem_fornecida = "Defasagem"
        col_inde, col_pedra = f"INDE {ano}", f"Pedra {ano}"
        col_mat, col_por, col_ing = "Mat", "Por", "Ing"
    else:
        raise ValueError(f"Ano não suportado: {ano}. Esperado um de (2022, 2023, 2024).")

    harmonizado = pd.DataFrame(
        {
            "ra": df["RA"].map(_extrair_numero_ra),
            "ano": ano,
            "fase_num": df[col_fase].map(_extrair_numero_fase),
            "fase_ideal_num": df[col_fase_ideal].map(_extrair_numero_fase),
            "defasagem_fornecida": _coluna_numerica_segura(df, col_defasagem_fornecida),
            "inde": _coluna_numerica_segura(df, col_inde),
            "pedra": df[col_pedra].replace(_MAPA_PEDRA) if col_pedra in df.columns else np.nan,
            "ian": _coluna_numerica_segura(df, "IAN"),
            "ida": _coluna_numerica_segura(df, "IDA"),
            "ieg": _coluna_numerica_segura(df, "IEG"),
            "iaa": _coluna_numerica_segura(df, "IAA"),
            "ips": _coluna_numerica_segura(df, "IPS"),
            "ipp": _coluna_numerica_segura(df, "IPP"),  # só existe a partir de 2023
            "ipv": _coluna_numerica_segura(df, "IPV"),
            "nota_matematica": _coluna_numerica_segura(df, col_mat),
            "nota_portugues": _coluna_numerica_segura(df, col_por),
            "nota_ingles": _coluna_numerica_segura(df, col_ing),
            "indicado": df["Indicado"] if "Indicado" in df.columns else np.nan,
            "atingiu_pv": df["Atingiu PV"] if "Atingiu PV" in df.columns else np.nan,
            "turma": df["Turma"] if "Turma" in df.columns else np.nan,
            "genero": df["Gênero"].replace(_MAPA_GENERO) if "Gênero" in df.columns else np.nan,
            "ano_ingresso": _coluna_numerica_segura(df, "Ano ingresso"),
            "instituicao_ensino": df["Instituição de ensino"] if "Instituição de ensino" in df.columns else np.nan,
            "ano_nascimento": _extrair_ano_nascimento(df, ano),
        }
    )
    harmonizado["defasagem_calculada"] = harmonizado["fase_num"] - harmonizado["fase_ideal_num"]
    # Idade derivada do ano de nascimento (e não da coluna "Idade" bruta):
    # a coluna "Idade" de PEDE2023 tem artefatos de data do Excel (ex.: idade
    # 8 virou o timestamp "1900-01-08"), então derivar de ano_nascimento é
    # mais robusto e fica consistente entre os três anos.
    harmonizado["idade_anos"] = harmonizado["ano"] - harmonizado["ano_nascimento"]
    return harmonizado


def build_painel(raw_path: Path | str = RAW_XLSX_PATH, verbose: bool = True) -> pd.DataFrame:
    """
    Lê as 3 abas do PEDE, harmoniza cada ano para o esquema comum em
    snake_case (ver `_harmonizar_ano`) e empilha tudo em um painel longo:
    1 linha por aluno-ano, com a coluna `ano` identificando 2022/2023/2024.
    """
    abas = carregar_abas_brutas(raw_path)
    if verbose:
        inspecionar_abas(abas, verbose=True)
    anos_harmonizados = [_harmonizar_ano(df, int(aba.replace("PEDE", ""))) for aba, df in abas.items()]
    painel = pd.concat(anos_harmonizados, ignore_index=True)
    return painel.sort_values(["ra", "ano"]).reset_index(drop=True)


def build_painel_com_alvo(painel: pd.DataFrame) -> pd.DataFrame:
    """
    Cria a coluna `alvo_risco_defasagem_prox_ano`:
      - 1 se o aluno está defasado (defasagem_calculada < 0, ou seja, fase
        efetiva abaixo da fase ideal) no ano SEGUINTE ao da linha;
      - 0 se não está defasado no ano seguinte;
      - NA se o aluno não tem registro no ano seguinte (ex.: toda linha com
        ano == 2024 fica NA, porque não existe PEDE2025 nesta base; também
        fica NA quando o aluno saiu da associação e não respondeu a PEDE
        do ano seguinte).

    O alvo deliberadamente vem do ano seguinte ao das features de cada linha
    (join em ra + ano-1) para não vazar informação do próprio ano da linha.

    Usamos `defasagem_calculada` (não `defasagem_fornecida`) como base do
    alvo porque está disponível para 100% das linhas — deriva só de Fase e
    Fase Ideal, que estão sempre preenchidas — enquanto a coluna fornecida
    pela Passos Mágicos pode ter ausências pontuais. A seção de QA do
    notebook mostra o quão próximas as duas são.
    """
    defasagem_ano_seguinte = painel[["ra", "ano", "defasagem_calculada"]].copy()
    defasagem_ano_seguinte["ano"] -= 1
    defasagem_ano_seguinte = defasagem_ano_seguinte.rename(columns={"defasagem_calculada": "_defasagem_ano_seguinte"})

    painel_com_alvo = painel.merge(defasagem_ano_seguinte, on=["ra", "ano"], how="left")
    painel_com_alvo["alvo_risco_defasagem_prox_ano"] = np.where(
        painel_com_alvo["_defasagem_ano_seguinte"].isna(),
        np.nan,
        (painel_com_alvo["_defasagem_ano_seguinte"] < 0).astype(float),
    )
    return painel_com_alvo.drop(columns=["_defasagem_ano_seguinte"])


def calcular_pedra_por_inde(inde: pd.Series) -> pd.Series:
    """Recalcula a Pedra a partir do INDE usando as faixas oficiais em `FAIXAS_PEDRA_POR_INDE` (documento interno PM)."""

    def _classificar(valor: float) -> float | str:
        if pd.isna(valor):
            return np.nan
        for minimo, maximo, nome in FAIXAS_PEDRA_POR_INDE:
            if minimo <= valor <= maximo:
                return nome
        return np.nan

    return inde.map(_classificar)


def _normalizar_texto_categorico(valor):
    """Remove acentos e caracteres especiais de um valor de categoria, converte para maiúsculo e preserva espaços entre palavras (NaN passa direto)."""
    if pd.isna(valor):
        return valor
    sem_acento = unicodedata.normalize("NFKD", str(valor)).encode("ascii", "ignore").decode("ascii")
    sem_especiais = _PADRAO_CARACTER_NAO_ALFANUMERICO.sub("", sem_acento)
    return _PADRAO_ESPACOS_REPETIDOS.sub(" ", sem_especiais).strip().upper()


def padronizar_nomes_e_categorias(painel: pd.DataFrame) -> pd.DataFrame:
    """
    Último passo de padronização antes de salvar o CSV consolidado. Faz só
    duas coisas:

    1. Renomeia todas as colunas para maiúsculo. `fase_num` e
       `fase_ideal_num` viram `FASE` e `FASE_IDEAL` (tirando o sufixo
       "_num", não só maiusculizando) — os demais nomes são um uppercase
       direto do snake_case (ex.: `ida` -> `IDA`, `genero` -> `GENERO`).
    2. Nas colunas de texto/categóricas (`GENERO`, `PEDRA`, `TURMA`,
       `INSTITUICAO_ENSINO`, `INDICADO`, `ATINGIU_PV`, já com o nome pós
       renomeio), remove acentos e caracteres especiais e converte para
       maiúsculo, preservando os espaços entre palavras.

    Deliberadamente NÃO arredonda nenhuma coluna numérica, NÃO troca o
    separador decimal (continua ponto) e NÃO preenche valores ausentes —
    ver a célula de decisão no notebook 01, logo antes do salvamento do CSV.
    """
    renomeado = painel.rename(
        columns={coluna: _RENOMEIO_COLUNA_ESPECIAL.get(coluna, coluna.upper()) for coluna in painel.columns}
    )
    for coluna in _COLUNAS_CATEGORICAS_PARA_NORMALIZAR:
        if coluna in renomeado.columns:
            renomeado[coluna] = renomeado[coluna].map(_normalizar_texto_categorico)
    return renomeado
