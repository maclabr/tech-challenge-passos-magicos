# Tech Challenge 5 — Passos Mágicos

Projeto desenvolvido para o **Datathon da Pós-Tech em Data Analytics da FIAP**, a partir dos dados da **Pesquisa Extensiva do Desenvolvimento Educacional (PEDE)** da Associação Passos Mágicos.

A solução combina **análise de dados, acompanhamento longitudinal e Machine Learning** para apoiar a leitura da trajetória educacional dos alunos e a identificação de situações que merecem acompanhamento.

O período analisado compreende **2022 a 2024**.

---

## Objetivo

O projeto foi estruturado para transformar os dados educacionais em uma solução analítica capaz de:

- consolidar e harmonizar os dados da PEDE entre 2022 e 2024;
- apresentar indicadores educacionais e evolução dos alunos em um dashboard interativo;
- acompanhar situações de defasagem educacional;
- estimar o risco de defasagem no período seguinte;
- estimar a incidência de nova defasagem entre alunos que ainda não estão defasados;
- apresentar fatores que contribuem para cada previsão;
- documentar metodologia, limitações e critérios utilizados na solução.

> As probabilidades produzidas pelos modelos são instrumentos de apoio à análise. Elas não substituem avaliação pedagógica ou decisão humana.

---

## Aplicação Streamlit

A aplicação foi organizada em quatro páginas.

### 1. Visão Geral

Apresenta o contexto do projeto, período analisado, volume de registros, indicadores PEDE utilizados e os principais componentes da solução.

### 2. Dashboard

Reúne análises descritivas e longitudinais dos dados educacionais, incluindo:

- panorama da base;
- situação de defasagem;
- indicadores PEDE;
- desempenho acadêmico;
- evolução da trajetória dos alunos;
- comparações entre períodos disponíveis.

### 3. Avaliação de Risco

Permite informar manualmente os indicadores de um aluno e utilizar os pipelines persistidos para estimar:

- **Risco futuro de defasagem** — probabilidade de o aluno estar defasado no próximo período observado;
- **Nova incidência de defasagem** — probabilidade de um aluno atualmente não defasado passar a apresentar defasagem no período seguinte.

A página também apresenta uma explicação dos fatores que mais contribuíram para aumentar ou reduzir a previsão.

O valor de **50%** exibido na interface é utilizado como **referência operacional de visualização**, e não como um limiar de decisão validado para uso pedagógico ou produção.

### 4. Modelo & Projeto

Documenta a solução de Machine Learning e sua metodologia, incluindo:

- definição do problema;
- variáveis utilizadas;
- estratégia preditiva;
- validação temporal;
- métricas de referência;
- explicabilidade;
- limitações e cuidados de interpretação;
- tecnologias utilizadas.

---

## Modelos preditivos

A solução utiliza dois problemas de classificação distintos.

### Risco futuro

O alvo `ALVO_RISCO_DEFASAGEM_PROX_ANO` representa a situação de defasagem no próximo ano observado.

### Nova incidência de defasagem

O segundo modelo considera a entrada em defasagem no período seguinte entre alunos elegíveis que, no período atual, não estão defasados.

A regra utilizada para a defasagem é:

```text
DEFASAGEM_CALCULADA = FASE - FASE_IDEAL
```

Assim:

- valor **negativo** → aluno defasado;
- valor **igual a zero** → aluno na fase esperada;
- valor **positivo** → aluno acima da fase esperada.

---

## Variáveis utilizadas nos modelos

Os pipelines persistidos utilizam 14 variáveis numéricas:

```text
FASE
FASE_IDEAL
DEFASAGEM_CALCULADA
IAN
IDA
IEG
IAA
IPS
IPV
NOTA_MATEMATICA
NOTA_PORTUGUES
NOTA_INGLES
IDADE_ANOS
ANO_INGRESSO
```

---

## Validação temporal e métricas de referência

A avaliação foi estruturada respeitando a ordem temporal dos dados, reduzindo o risco de utilizar informações futuras para avaliar previsões sobre períodos anteriores.

As métricas abaixo correspondem à **validação temporal auditada**, documentada no notebook de modelagem. Elas **não são métricas do pipeline final persistido**, pois os modelos disponibilizados para inferência foram posteriormente retreinados com todo o histórico rotulado disponível.

| Modelo | Accuracy | F1 Macro | ROC-AUC |
|---|---:|---:|---:|
| Risco futuro | 0,725 | 0,713 | **0,831** |
| Nova incidência de defasagem | 0,676 | 0,534 | **0,693** |

---

## Estrutura do projeto

```text
tech-challenge-passos-magicos/
│
├── app/
│   ├── assets/
│   │   └── hero_passos_magicos.png
│   ├── pages/
│   │   ├── 1_Visao_Geral.py
│   │   ├── 2_Dashboard.py
│   │   ├── 3_Avaliacao_de_Risco.py
│   │   └── 4_Modelo_e_Projeto.py
│   ├── utils/
│   │   ├── charts.py
│   │   ├── data_loader.py
│   │   └── styles.py
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   │   └── base_bronze.xlsx
│   └── processed/
│       └── pede_painel_consolidado.csv
│
├── docs/
│   ├── contrato_de_dados.md
│   └── linhagem_de_dados.md
│
├── models/
│   ├── pipeline_risco_futuro.joblib
│   ├── pipeline_risco_futuro_explicativo.joblib
│   ├── pipeline_incidencia_nova_defasagem.joblib
│   ├── pipeline_incidencia_nova_defasagem_explicativo.joblib
│   └── metadados.json
│
├── notebooks/
│   ├── 01_limpeza_e_preparacao.ipynb
│   ├── 02_analise_exploratoria.ipynb
│   └── 03_modelagem_risco_temporal.ipynb
│
├── src/
│   ├── data_prep.py
│   ├── eda_utils.py
│   ├── modeling.py
│   └── treinar_e_persistir_modelos.py
│
├── tests/
│   ├── test_data_prep.py
│   ├── test_data_quality.py
│   ├── test_inference.py
│   └── test_modeling.py
│
├── requirements.txt
├── runtime.txt
└── README.md
```

---

## Preparação dos dados

A fonte principal do projeto é a base PEDE disponibilizada para o Datathon.

O pipeline de preparação realiza a harmonização dos dados de **2022, 2023 e 2024** e gera o painel consolidado utilizado pelas análises e pela modelagem.

O grão analítico do painel é:

```text
RA + ANO
```

O `RA` é tratado como identificador pseudonimizado e não é utilizado como variável preditiva nem apresentado na aplicação de avaliação de risco.

As regras completas de preparação, definições e limitações estão documentadas em:

```text
docs/contrato_de_dados.md
docs/linhagem_de_dados.md
```

---

## Como executar o projeto

### 1. Criar o ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

O projeto está configurado para **Python 3.12**, conforme `runtime.txt`.

### 3. Executar os testes

```bash
pytest -q
```

### 4. Gerar novamente os modelos, se necessário

Os pipelines já estão persistidos em `models/`. Para refazer o treinamento:

```bash
python -m src.treinar_e_persistir_modelos
```

### 5. Executar a aplicação

```bash
streamlit run app/streamlit_app.py
```

---

## Notebooks

Os notebooks documentam as principais etapas analíticas:

```text
01_limpeza_e_preparacao.ipynb
02_analise_exploratoria.ipynb
03_modelagem_risco_temporal.ipynb
```

O notebook 01 prepara a base consolidada. O notebook 02 concentra a análise exploratória. O notebook 03 documenta a modelagem e a validação temporal.

---

## Testes automatizados

O projeto possui testes para:

- preparação dos dados;
- qualidade e consistência da base;
- regras da modelagem;
- inferência com os pipelines persistidos.

Eles podem ser executados com:

```bash
pytest -q
```

---

## Tecnologias

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib
- Seaborn
- Joblib
- OpenPyXL
- Pytest
- Jupyter Notebook

---

## Cuidados de interpretação

A solução foi desenvolvida como projeto analítico e preditivo aplicado ao contexto educacional. Alguns cuidados são importantes:

- associação estatística não implica causalidade;
- probabilidades devem ser interpretadas como apoio à análise;
- o desempenho observado na validação temporal não garante o mesmo desempenho em dados futuros;
- mudanças no perfil dos alunos, no processo educacional ou na coleta dos indicadores podem alterar o comportamento do modelo;
- qualquer uso operacional deve considerar acompanhamento de desempenho, revisão periódica e validação com especialistas do contexto educacional.

---

## Documentação complementar

Para detalhes sobre regras, transformações e decisões metodológicas, consulte:

- `docs/contrato_de_dados.md`
- `docs/linhagem_de_dados.md`
- `notebooks/03_modelagem_risco_temporal.ipynb`
- `models/metadados.json`

---

## Projeto acadêmico

**FIAP — Pós-Tech Data Analytics**  
**Tech Challenge / Datathon — Passos Mágicos**

Solução desenvolvida para fins acadêmicos, integrando preparação de dados, análise exploratória, visualização, Machine Learning, explicabilidade e disponibilização em Streamlit.
