# Contrato de dados PEDE 2022–2024

## 1. Finalidade e fonte de verdade

Este contrato rege as análises e o primeiro modelo do Tech Challenge 5. A fonte canônica é `data/raw/base_bronze.xlsx`, fornecida para o Datathon, com as abas `PEDE2022`, `PEDE2023` e `PEDE2024`. A fonte transformada é `data/processed/pede_painel_consolidado.csv`, produzida pelo notebook `01_limpeza_e_preparacao.ipynb` e por `src/data_prep.py`.

O dicionário PDF é referência para o significado dos indicadores, mas **não** é contrato de schema: ele documenta uma versão histórica (2020, 2021 e 2023), enquanto a fonte canônica desta entrega cobre 2022–2024 e possui nomes de colunas diferentes.

A base antiga compactada é uma fonte potencial de enriquecimento futuro. Ela não integra o MVP: seus CSVs relacionais e arquivos `merged_data.csv` só poderão ser usados depois de documentar chaves, cardinalidades, período de cobertura e testes contra explosão de joins.

## 2. Grão, chave e período

| Item | Regra |
|---|---|
| Grão | Uma linha por estudante anônimo (`RA`) e ano PEDE (`ANO`) |
| Chave candidata | `RA`, `ANO` |
| Período coberto | 2022, 2023 e 2024 |
| Identificador | `RA` é pseudônimo técnico; não é exibido em análises ou no app |
| Atualização | Uma nova aba/ano requer inspeção e mapeamento explícito em `src/data_prep.py` |

## 3. Dicionário harmonizado

| Campo | Tipo | Definição e regra |
|---|---|---|
| `RA`, `ANO` | inteiro | Chave do painel; obrigatórios e únicos em conjunto |
| `FASE`, `FASE_IDEAL` | numérico | Nível efetivo e nível esperado. `ALFA = 0`; demais valores são extraídos do primeiro nível informado |
| `DEFASAGEM_CALCULADA` | numérico | `FASE - FASE_IDEAL`; negativo significa defasagem |
| `DEFASAGEM_FORNECIDA` | numérico | Campo original. Mantido para reconciliação, sem sobrescrever a calculada |
| `IAN`, `IDA`, `IEG`, `IAA`, `IPS`, `IPP`, `IPV` | numérico | Indicadores PEDE; valores esperados aproximadamente no intervalo 0–10. `IPP` não consta na aba PEDE2022 recebida |
| `INDE` | numérico | Índice global fornecido; não deve ser recalculado sem fórmula/ponderações oficiais |
| `PEDRA` | categórico | Classificação fornecida: `QUARTZO`, `AGATA`, `AMETISTA`, `TOPAZIO`; mantida como informação de origem |
| `NOTA_*` | numérico | Notas de Matemática, Português e Inglês; ausências são preservadas |
| `TURMA`, `GENERO`, `INSTITUICAO_ENSINO` | categórico | Atributos de contexto; texto normalizado para maiúsculas sem acentos |
| `ANO_INGRESSO`, `ANO_NASCIMENTO`, `IDADE_ANOS` | numérico | Contexto longitudinal; `IDADE_ANOS = ANO - ANO_NASCIMENTO` |
| `ALVO_RISCO_DEFASAGEM_PROX_ANO` | binário/ausente | 1 se o estudante aparece no ano seguinte com `DEFASAGEM_CALCULADA < 0`; 0 se aparece sem defasagem; ausente sem observação no ano seguinte |

## 4. Regras de qualidade e tratamento

1. Não eliminar linhas nem preencher ausências automaticamente na camada processada.
2. Exigir unicidade de `RA + ANO`, anos permitidos e presença de `FASE`, `FASE_IDEAL` e `DEFASAGEM_CALCULADA`.
3. Reconciliar `DEFASAGEM_FORNECIDA` e `DEFASAGEM_CALCULADA`; divergências devem ser reportadas, não corrigidas silenciosamente.
4. A Pedra recalculada pela fórmula do INDE (`calcular_pedra_por_inde`) é usada apenas como comparação de QA pontual dentro do notebook 01 (variável `pedra_recalculada`, não persistida), não é um campo mantido no painel processado. Caso vire um campo oficial `PEDRA_CALCULADA` no futuro, esta regra deve ser atualizada. A divergência entre a Pedra fornecida e a recalculada exige validação da Passos Mágicos.
5. Tratar ausências estruturais por ano como indisponibilidade de medição, não como zero. Em particular, excluir `IPP` de comparações que incluam 2022 ou usar uma estratégia de disponibilidade explicitamente validada no modelo. A ausência na aba recebida não prova que o indicador não tenha sido coletado pela Associação.
6. Não expor nome, data de nascimento integral, `RA` ou qualquer identificador individual em visualizações, logs, apresentação ou aplicativo.

## 5. Definições analíticas

- **Defasado:** `DEFASAGEM_CALCULADA < 0`.
- **Em fase ou adiantado:** `DEFASAGEM_CALCULADA >= 0`.
- **Risco futuro:** estado de defasagem no próximo ano observado. É o alvo disponível hoje.
- **Incidência de nova defasagem:** risco futuro entre estudantes não defasados no ano atual. Este é o alvo mais fiel à expressão “entrar em risco” e deve ser avaliado separadamente.
- **Coorte longitudinal:** somente estudantes presentes nos dois anos comparados. Resultados não representam automaticamente todos os atendidos, pois há entradas e saídas entre as PEDEs.

## 6. Uso no modelo e validação

O modelo não poderá usar dados de anos posteriores à predição. A avaliação será temporal: dados de 2022 para prever 2023 e dados de 2023 para avaliar a generalização para 2024. Uma divisão aleatória não é aceitável como avaliação principal.

O `INDE` é composto pelos indicadores PEDE; análises de associação entre seus componentes e INDE são descritivas, não evidência independente de causalidade. Da mesma forma, diferenças entre anos ou coortes não demonstram, isoladamente, impacto causal do programa.

## 7. Responsáveis por decisão pendente

| Decisão | Situação atual | Necessidade |
|---|---|---|
| Faixas de Pedra | Divergem do INDE em parcela relevante do painel | Confirmar regra vigente e tratamento de fronteiras com a Passos Mágicos |
| Risco do modelo | Há alvo de estado futuro e alvo de incidência possível | Validar qual fluxo operacional o app deverá apoiar |
| Ausência de PEDE | Pode refletir evasão, ingresso ou não resposta | Não interpretar como não risco; solicitar definição operacional se for necessário modelar retenção |
