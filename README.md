# Datathon Passos Mágicos — Tech Challenge Fase 5

Projeto da Pós-Tech FIAP (Tech Challenge, Fase 5): análise dos dados PEDE 2022-2024 da
Associação Passos Mágicos e construção de um modelo preditivo de risco de defasagem escolar
para os alunos atendidos pela associação.

## Estrutura do repositório

```
.
├── app/            # Aplicação (dashboard/interface) para consumo do modelo
├── data/
│   ├── raw/        # Dados brutos (base original PEDE)
│   └── processed/  # Dados tratados/consolidados, prontos para análise e modelagem
├── models/         # Modelos treinados (artefatos .joblib)
├── notebooks/       # Notebooks de exploração, limpeza e modelagem
├── src/            # Código-fonte (preparação de dados, features, treino, etc.)
├── tests/          # Testes automatizados
└── requirements.txt
```

## Como rodar

1. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Explore o pipeline de limpeza e preparação dos dados no notebook:
   `notebooks/01_limpeza_e_preparacao.ipynb`

## Status

Projeto em andamento — este README será expandido com os resultados da análise exploratória
e do modelo preditivo à medida que o desafio avança.
