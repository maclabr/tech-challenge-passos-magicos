# Linhagem de dados — PEDE 2022–2024

## Fluxo

`data/raw/base_bronze.xlsx` (abas `PEDE2022`, `PEDE2023`, `PEDE2024`)
→ `src/data_prep.py`
→ `notebooks/01_limpeza_e_preparacao.ipynb`
→ `data/processed/pede_painel_consolidado.csv`
→ notebooks analítico e de modelagem.

## Transformações controladas

| Etapa | Implementação | Regra |
|---|---|---|
| Leitura | `carregar_abas_brutas` | Exige as três abas previstas; não altera valores |
| Harmonização | `_harmonizar_ano` | Mapeia nomes de cada ano para um esquema comum e preserva uma linha por registro bruto |
| Fase | `_extrair_numero_fase` | `ALFA` equivale a 0; outros formatos usam o primeiro número do texto |
| Defasagem | `_harmonizar_ano` | `FASE - FASE_IDEAL`; o campo original também é preservado |
| Alvo futuro | `build_painel_com_alvo` | Junta o mesmo `RA` do ano seguinte; não cria rótulo para quem não reaparece |
| Publicação | `padronizar_nomes_e_categorias` | Maiúsculas/ASCII em categorias, sem imputar, arredondar ou excluir registros |

## Verificações e evidência

| Controle | Evidência automatizada |
|---|---|
| Abas, shape e schema mínimo | `tests/test_data_prep.py` |
| Chave `RA + ANO`, domínios e faltantes estruturais | `tests/test_data_quality.py` |
| Reconciliação de defasagem | `tests/test_data_quality.py` |
| Regra temporal do alvo | `tests/test_data_quality.py` |
| Reprodutibilidade do CSV processado | `tests/test_data_quality.py` |

## Limites de linhagem

- O dicionário de dados é semântico, mas descreve um schema histórico diferente; a planilha recebida controla os nomes e a presença de colunas.
- Pedra calculada por INDE é apenas reconciliação de QA. A Pedra fornecida permanece como dado de origem.
- A ausência de uma PEDE no ano seguinte não recebe significado de evasão, melhora ou piora.
- A planilha raw contém campos que exigem revisão de autorização antes de qualquer divulgação pública.
