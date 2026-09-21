# Tech Challenge 5 — Passos Mágicos

Projeto de Data Analytics para a Pesquisa Extensiva do Desenvolvimento Educacional (PEDE), com dados de 2022 a 2024. O objetivo é responder às perguntas do Datathon, apoiar o acompanhamento de defasagem e, na próxima etapa, construir um modelo de risco com validação temporal.

## Estrutura atual

```text
data/raw/base_bronze.xlsx             # fonte PEDE entregue para o Datathon
data/processed/pede_painel_consolidado.csv
src/data_prep.py                      # harmonização 2022–2024
src/eda_utils.py                      # funções de apoio à análise exploratória
src/modeling.py                       # pipeline de modelagem de risco com validação temporal
notebooks/01_limpeza_e_preparacao.ipynb
notebooks/02_analise_exploratoria.ipynb
notebooks/03_modelagem_risco_temporal.ipynb
docs/contrato_de_dados.md             # grão, definições, regras e pendências
docs/linhagem_de_dados.md             # fluxo de transformação e verificações automatizadas
app/                                  # app Streamlit (ainda vazio)
models/                               # pipeline treinado persistido
tests/                                # testes de preparação, qualidade e modelagem
```

## Como reproduzir

Requer Python 3.12+ (ver `runtime.txt`; `numpy==2.5.1` em `requirements.txt` não instala em Python 3.11).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
jupyter notebook notebooks/01_limpeza_e_preparacao.ipynb
```

Execute o notebook 01 antes do 02 caso `data/processed/pede_painel_consolidado.csv` ainda não exista ou a fonte bronze seja atualizada. O notebook `03_modelagem_risco_temporal.ipynb` usa a mesma fonte processada e não depende do 02, mas segue a mesma ordem lógica do pipeline.

## Decisões de dados

- A fonte canônica do MVP é a planilha PEDE 2022–2024; a base antiga só será considerada como enriquecimento futuro após modelagem relacional e validação de joins.
- O painel tem grão `RA + ANO`. `RA` é um identificador pseudonimizado e não deve aparecer em análises ou no aplicativo.
- `ALVO_RISCO_DEFASAGEM_PROX_ANO` representa estar defasado no próximo ano observado; a incidência de **nova** defasagem será tratada como problema separado.
- As categorias de Pedra fornecidas são preservadas. Sua divergência em relação às faixas de INDE está documentada como pendência de negócio.

Veja o [contrato de dados](docs/contrato_de_dados.md) para regras completas, limitações e decisões pendentes.
