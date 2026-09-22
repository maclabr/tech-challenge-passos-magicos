import pandas as pd
import streamlit as st

from utils import charts
from utils.data_loader import carregar_dados
from utils.styles import aplicar_estilo


# ============================================================
# CONFIGURAÇÃO
# ============================================================

aplicar_estilo()
df = carregar_dados()


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def formatar_inteiro(valor):
    return f"{int(valor):,}".replace(",", ".")


def formatar_decimal(valor, casas=2):
    if pd.isna(valor):
        return "—"
    return f"{valor:.{casas}f}".replace(".", ",")


def formatar_percentual(valor):
    if pd.isna(valor):
        return "—"
    return f"{valor:.1f}%".replace(".", ",")


def classificar_defasagem(valor):
    if pd.isna(valor):
        return "Sem informação"
    if valor < 0:
        return "Com defasagem"
    return "Sem defasagem"


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="page-label">PANORAMA EDUCACIONAL</div>',
    unsafe_allow_html=True,
)

st.title("Indicadores e evolução dos alunos")

st.markdown(
    """
<div class="page-description">
Explore os principais indicadores educacionais e acompanhe
a evolução dos alunos atendidos pela Passos Mágicos entre
2022 e 2024.
</div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# ============================================================
# FILTROS
# ============================================================

with st.container(border=True):
    st.markdown(
        '<div class="card-title">Filtros</div>',
        unsafe_allow_html=True,
    )

    filtro1, filtro2 = st.columns(2)

    anos_disponiveis = sorted(
        df["ANO"].dropna().astype(int).unique().tolist()
    )

    with filtro1:
        ano_selecionado = st.selectbox(
            "Ano",
            options=["Todos"] + anos_disponiveis,
        )

    fases_disponiveis = sorted(
        df["FASE"].dropna().unique().tolist()
    )

    with filtro2:
        fase_selecionada = st.selectbox(
            "Fase",
            options=["Todas"] + fases_disponiveis,
        )


# ============================================================
# APLICAÇÃO DOS FILTROS
# ============================================================

df_filtrado = df.copy()

if ano_selecionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["ANO"] == ano_selecionado
    ]

if fase_selecionada != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["FASE"] == fase_selecionada
    ]

if df_filtrado.empty:
    st.warning(
        "Não há registros para a combinação de filtros selecionada."
    )
    st.stop()


# ============================================================
# FILTROS ATIVOS
# ============================================================

st.write("")

filtros_ativos = []

if ano_selecionado != "Todos":
    filtros_ativos.append(f"Ano: {ano_selecionado}")

if fase_selecionada != "Todas":
    filtros_ativos.append(f"Fase: {fase_selecionada}")

if filtros_ativos:
    st.caption("Filtros ativos • " + " | ".join(filtros_ativos))
else:
    st.caption("Exibindo todos os registros disponíveis.")


# ============================================================
# VISÃO GERAL
# ============================================================

total_registros = len(df_filtrado)
total_alunos = df_filtrado["RA"].nunique()

defasagem_valida = pd.to_numeric(
    df_filtrado["DEFASAGEM_FORNECIDA"],
    errors="coerce",
).dropna()

if len(defasagem_valida) > 0:
    percentual_defasagem = (defasagem_valida < 0).mean() * 100
else:
    percentual_defasagem = float("nan")

inde_medio = pd.to_numeric(
    df_filtrado["INDE"],
    errors="coerce",
).mean()

st.subheader("Visão geral")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Registros", formatar_inteiro(total_registros))

with kpi2:
    st.metric("Alunos únicos", formatar_inteiro(total_alunos))

with kpi3:
    st.metric(
        "Com defasagem",
        formatar_percentual(percentual_defasagem),
    )

with kpi4:
    st.metric("INDE médio", formatar_decimal(inde_medio))


# ============================================================
# DEFASAGEM EDUCACIONAL
# ============================================================

st.write("")
st.write("")

st.subheader("Defasagem educacional")

st.caption(
    "Situação de defasagem dos registros disponíveis "
    "no recorte selecionado."
)

df_defasagem = df_filtrado.copy()

df_defasagem["DEFASAGEM_FORNECIDA"] = pd.to_numeric(
    df_defasagem["DEFASAGEM_FORNECIDA"],
    errors="coerce",
)

df_defasagem["SITUACAO_DEFASAGEM"] = df_defasagem[
    "DEFASAGEM_FORNECIDA"
].apply(classificar_defasagem)

total_com_defasagem = (
    df_defasagem["DEFASAGEM_FORNECIDA"] < 0
).sum()

total_sem_defasagem = (
    df_defasagem["DEFASAGEM_FORNECIDA"] >= 0
).sum()

total_sem_informacao = (
    df_defasagem["DEFASAGEM_FORNECIDA"].isna().sum()
)

d1, d2, d3 = st.columns(3)

with d1:
    st.metric(
        "Com defasagem",
        formatar_inteiro(total_com_defasagem),
    )

with d2:
    st.metric(
        "Sem defasagem",
        formatar_inteiro(total_sem_defasagem),
    )

with d3:
    st.metric(
        "Sem informação",
        formatar_inteiro(total_sem_informacao),
    )

st.write("")

def_col1, def_col2 = st.columns([1.35, 1])


# ============================================================
# EVOLUÇÃO DA DEFASAGEM
# ============================================================

with def_col1:
    with st.container(border=True):

        if ano_selecionado == "Todos":
            st.markdown(
                '<div class="card-title">Evolução da defasagem</div>',
                unsafe_allow_html=True,
            )

            st.caption(
                "Percentual de registros com defasagem em cada ano."
            )

            df_evolucao = df.copy()

            if fase_selecionada != "Todas":
                df_evolucao = df_evolucao[
                    df_evolucao["FASE"] == fase_selecionada
                ]

            df_evolucao["DEFASAGEM_FORNECIDA"] = pd.to_numeric(
                df_evolucao["DEFASAGEM_FORNECIDA"],
                errors="coerce",
            )

            df_evolucao = (
                df_evolucao
                .dropna(
                    subset=[
                        "ANO",
                        "DEFASAGEM_FORNECIDA",
                    ]
                )
                .copy()
            )

            df_evolucao["COM_DEFASAGEM"] = (
                df_evolucao["DEFASAGEM_FORNECIDA"] < 0
            )

            evolucao_defasagem = (
                df_evolucao
                .groupby("ANO")["COM_DEFASAGEM"]
                .mean()
                .mul(100)
                .reset_index(name="Percentual")
            )

            evolucao_defasagem["ANO"] = (
                evolucao_defasagem["ANO"]
                .astype(int)
                .astype(str)
            )

            # Gráfico construído diretamente com Altair para evitar
            # dependência da função auxiliar grafico_linha.
            import altair as alt

            chart = (
                alt.Chart(evolucao_defasagem)
                .mark_line(
                    color=charts.TEAL,
                    strokeWidth=3,
                    point=alt.OverlayMarkDef(
                        filled=True,
                        size=90,
                        color=charts.TEAL,
                    ),
                )
                .encode(
                    x=alt.X(
                        "ANO:O",
                        title="Ano",
                        axis=alt.Axis(labelAngle=0),
                    ),
                    y=alt.Y(
                        "Percentual:Q",
                        title="Com defasagem (%)",
                        scale=alt.Scale(domain=[0, 100]),
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "ANO:O",
                            title="Ano",
                        ),
                        alt.Tooltip(
                            "Percentual:Q",
                            title="Com defasagem (%)",
                            format=".1f",
                        ),
                    ],
                )
                .properties(height=350)
                .configure_view(stroke=None)
                .configure_axis(
                    labelColor="#527087",
                    titleColor="#143A59",
                    domainColor="#DDEAF0",
                    tickColor="#DDEAF0",
                    gridColor="#E8F0F4",
                    gridOpacity=0.75,
                    labelFontSize=12,
                    titleFontSize=12,
                    titleFontWeight=500,
                    labelPadding=8,
                    titlePadding=12,
                )
            )

            st.altair_chart(
                chart,
                use_container_width=True,
            )

        else:
            st.markdown(
                (
                    '<div class="card-title">'
                    f'Defasagem em {ano_selecionado}'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )

            st.caption(
                "Distribuição da situação no período selecionado."
            )

            distribuicao_ano = (
                df_defasagem["SITUACAO_DEFASAGEM"]
                .value_counts()
                .rename_axis("Situação")
                .reset_index(name="Registros")
            )

            ordem_situacao = [
                "Com defasagem",
                "Sem defasagem",
                "Sem informação",
            ]

            chart = charts.grafico_barras_categorias(
                dados=distribuicao_ano,
                campo_x="Situação",
                campo_y="Registros",
                dominio=ordem_situacao,
                cores=[
                    charts.NAVY,
                    charts.TEAL,
                    charts.LIGHT_TEAL,
                ],
                titulo_x="Situação",
                titulo_y="Registros",
                altura=350,
            )

            st.altair_chart(
                chart,
                use_container_width=True,
            )


# ============================================================
# SITUAÇÃO NO RECORTE
# ============================================================

with def_col2:
    with st.container(border=True):

        st.markdown(
            (
                '<div class="card-title">'
                'Situação no recorte selecionado'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

        st.caption(
            "Quantidade de registros conforme a situação."
        )

        distribuicao = (
            df_defasagem["SITUACAO_DEFASAGEM"]
            .value_counts()
            .rename_axis("Situação")
            .reset_index(name="Registros")
        )

        ordem_situacao = [
            "Com defasagem",
            "Sem defasagem",
            "Sem informação",
        ]

        chart = charts.grafico_barras_categorias(
            dados=distribuicao,
            campo_x="Situação",
            campo_y="Registros",
            dominio=ordem_situacao,
            cores=[
                charts.NAVY,
                charts.TEAL,
                charts.LIGHT_TEAL,
            ],
            titulo_x="Situação",
            titulo_y="Registros",
            altura=350,
        )

        st.altair_chart(
            chart,
            use_container_width=True,
        )


with st.expander("Como interpretar esta análise?"):
    st.markdown(
        """
A visualização utiliza a variável
**DEFASAGEM_FORNECIDA** existente na base consolidada.

- Valores **negativos** são classificados como registros
  com defasagem.
- Valores **iguais ou superiores a zero** são apresentados
  como sem defasagem.
- Valores ausentes são mantidos como **sem informação**.

A comparação anual é descritiva e considera os registros
disponíveis em cada período. Ela não representa
necessariamente os mesmos estudantes ao longo dos anos.
        """
    )


# ============================================================
# INDICADORES PEDE
# ============================================================

st.write("")
st.write("")

st.subheader("Indicadores PEDE")

st.caption(
    "Comparação dos principais indicadores utilizados no "
    "acompanhamento educacional."
)

indicadores_pede = [
    "IAN",
    "IDA",
    "IEG",
    "IAA",
    "IPS",
    "IPP",
    "IPV",
]

df_indicadores = df_filtrado.copy()

for indicador in indicadores_pede:
    if indicador in df_indicadores.columns:
        df_indicadores[indicador] = pd.to_numeric(
            df_indicadores[indicador],
            errors="coerce",
        )

medias_indicadores = []

for indicador in indicadores_pede:
    if indicador not in df_indicadores.columns:
        continue

    serie = df_indicadores[indicador].dropna()

    if not serie.empty:
        medias_indicadores.append(
            {
                "Indicador": indicador,
                "Média": serie.mean(),
                "Registros válidos": len(serie),
            }
        )

df_medias_indicadores = pd.DataFrame(
    medias_indicadores
)

if not df_medias_indicadores.empty:
    maior = (
        df_medias_indicadores
        .sort_values("Média", ascending=False)
        .iloc[0]
    )

    menor = (
        df_medias_indicadores
        .sort_values("Média")
        .iloc[0]
    )

    p1, p2, p3 = st.columns(3)

    with p1:
        st.metric(
            "Maior média",
            (
                f"{maior['Indicador']} • "
                f"{formatar_decimal(maior['Média'])}"
            ),
        )

    with p2:
        st.metric(
            "Menor média",
            (
                f"{menor['Indicador']} • "
                f"{formatar_decimal(menor['Média'])}"
            ),
        )

    with p3:
        st.metric(
            "Indicadores disponíveis",
            f"{len(df_medias_indicadores)} de 7",
        )

st.write("")

pede1, pede2 = st.columns([1, 1.4])

with pede1:
    with st.container(border=True):

        st.markdown(
            '<div class="card-title">Média dos indicadores</div>',
            unsafe_allow_html=True,
        )

        st.caption("Média no recorte selecionado.")

        if not df_medias_indicadores.empty:
            chart = charts.grafico_barras(
                dados=df_medias_indicadores,
                campo_x="Indicador",
                campo_y="Média",
                titulo_x="Indicador",
                titulo_y="Média",
                ordem=indicadores_pede,
                cor=charts.BLUE,
                formato_tooltip=".2f",
                altura=370,
            )

            st.altair_chart(
                chart,
                use_container_width=True,
            )


with pede2:
    with st.container(border=True):

        st.markdown(
            '<div class="card-title">Evolução dos indicadores</div>',
            unsafe_allow_html=True,
        )

        if ano_selecionado == "Todos":
            st.caption(
                "Média anual dos indicadores disponíveis."
            )

            df_temporal = df.copy()

            if fase_selecionada != "Todas":
                df_temporal = df_temporal[
                    df_temporal["FASE"] == fase_selecionada
                ]

            existentes = []

            for indicador in indicadores_pede:
                if indicador in df_temporal.columns:
                    df_temporal[indicador] = pd.to_numeric(
                        df_temporal[indicador],
                        errors="coerce",
                    )
                    existentes.append(indicador)

            if existentes:
                evolucao = (
                    df_temporal
                    .groupby("ANO")[existentes]
                    .mean()
                    .reset_index()
                )

                evolucao["ANO"] = (
                    evolucao["ANO"]
                    .astype(int)
                    .astype(str)
                )

                chart = charts.grafico_linhas(
                    dados=evolucao,
                    campo_x="ANO",
                    campos_y=existentes,
                    titulo_x="Ano",
                    titulo_y="Média",
                    altura=370,
                )

                st.altair_chart(
                    chart,
                    use_container_width=True,
                )

        else:
            st.caption(
                f"Comparação dos indicadores em {ano_selecionado}."
            )

            if not df_medias_indicadores.empty:
                chart = charts.grafico_barras(
                    dados=df_medias_indicadores,
                    campo_x="Indicador",
                    campo_y="Média",
                    titulo_x="Indicador",
                    titulo_y="Média",
                    ordem=indicadores_pede,
                    cor=charts.TEAL,
                    formato_tooltip=".2f",
                    altura=370,
                )

                st.altair_chart(
                    chart,
                    use_container_width=True,
                )


with st.expander("Disponibilidade dos indicadores"):
    st.markdown(
        """
As médias são calculadas somente sobre valores
efetivamente disponíveis. Dados ausentes não são
substituídos por zero.
        """
    )

    if not df_medias_indicadores.empty:
        cobertura = df_medias_indicadores.copy()

        cobertura["Média"] = cobertura[
            "Média"
        ].map(formatar_decimal)

        cobertura = cobertura.rename(
            columns={
                "Registros válidos":
                    "Observações disponíveis",
            }
        )

        st.dataframe(
            cobertura,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# DESEMPENHO ACADÊMICO
# ============================================================

st.write("")
st.write("")

st.subheader("Desempenho acadêmico")

st.caption(
    "Comparação das notas de Matemática, Português e Inglês "
    "conforme a disponibilidade dos dados."
)

disciplinas = {
    "Matemática": "NOTA_MATEMATICA",
    "Português": "NOTA_PORTUGUES",
    "Inglês": "NOTA_INGLES",
}

df_notas = df_filtrado.copy()

for coluna in disciplinas.values():
    if coluna in df_notas.columns:
        df_notas[coluna] = pd.to_numeric(
            df_notas[coluna],
            errors="coerce",
        )

resumo_notas = []

for disciplina, coluna in disciplinas.items():
    if coluna not in df_notas.columns:
        continue

    notas = df_notas[coluna].dropna()

    if not notas.empty:
        resumo_notas.append(
            {
                "Disciplina": disciplina,
                "Média": notas.mean(),
                "Observações": len(notas),
            }
        )

df_resumo_notas = pd.DataFrame(
    resumo_notas
)

n1, n2, n3 = st.columns(3)

for coluna_card, disciplina in zip(
    [n1, n2, n3],
    disciplinas.keys(),
):
    with coluna_card:
        linha = df_resumo_notas[
            df_resumo_notas["Disciplina"]
            == disciplina
        ]

        if not linha.empty:
            valor = formatar_decimal(
                linha["Média"].iloc[0]
            )
        else:
            valor = "—"

        st.metric(
            f"Média • {disciplina}",
            valor,
        )

st.write("")

nota_col1, nota_col2 = st.columns([1, 1.4])

with nota_col1:
    with st.container(border=True):

        st.markdown(
            '<div class="card-title">Média por disciplina</div>',
            unsafe_allow_html=True,
        )

        st.caption(
            "Comparação no recorte selecionado."
        )

        if not df_resumo_notas.empty:
            chart = charts.grafico_barras(
                dados=df_resumo_notas,
                campo_x="Disciplina",
                campo_y="Média",
                titulo_x="Disciplina",
                titulo_y="Média",
                ordem=[
                    "Matemática",
                    "Português",
                    "Inglês",
                ],
                cor=charts.BLUE,
                formato_tooltip=".2f",
                altura=370,
            )

            st.altair_chart(
                chart,
                use_container_width=True,
            )


with nota_col2:
    with st.container(border=True):

        st.markdown(
            '<div class="card-title">Evolução do desempenho</div>',
            unsafe_allow_html=True,
        )

        if ano_selecionado == "Todos":
            st.caption(
                "Média anual das notas disponíveis."
            )

            df_notas_temporal = df.copy()

            if fase_selecionada != "Todas":
                df_notas_temporal = df_notas_temporal[
                    df_notas_temporal["FASE"]
                    == fase_selecionada
                ]

            colunas_notas = []

            for disciplina, coluna in disciplinas.items():
                if coluna in df_notas_temporal.columns:
                    df_notas_temporal[coluna] = pd.to_numeric(
                        df_notas_temporal[coluna],
                        errors="coerce",
                    )
                    colunas_notas.append(coluna)

            if colunas_notas:
                evolucao_notas = (
                    df_notas_temporal
                    .groupby("ANO")[colunas_notas]
                    .mean()
                    .reset_index()
                )

                evolucao_notas = evolucao_notas.rename(
                    columns={
                        coluna: disciplina
                        for disciplina, coluna
                        in disciplinas.items()
                    }
                )

                evolucao_notas["ANO"] = (
                    evolucao_notas["ANO"]
                    .astype(int)
                    .astype(str)
                )

                chart = charts.grafico_linhas(
                    dados=evolucao_notas,
                    campo_x="ANO",
                    campos_y=list(
                        disciplinas.keys()
                    ),
                    titulo_x="Ano",
                    titulo_y="Média",
                    altura=370,
                )

                st.altair_chart(
                    chart,
                    use_container_width=True,
                )

        else:
            st.caption(
                f"Comparação das disciplinas em {ano_selecionado}."
            )

            if not df_resumo_notas.empty:
                chart = charts.grafico_barras(
                    dados=df_resumo_notas,
                    campo_x="Disciplina",
                    campo_y="Média",
                    titulo_x="Disciplina",
                    titulo_y="Média",
                    ordem=[
                        "Matemática",
                        "Português",
                        "Inglês",
                    ],
                    cor=charts.TEAL,
                    formato_tooltip=".2f",
                    altura=370,
                )

                st.altair_chart(
                    chart,
                    use_container_width=True,
                )


with st.expander("Disponibilidade das notas"):
    st.markdown(
        """
As médias consideram somente as notas efetivamente
disponíveis. Valores ausentes não são substituídos por zero.
        """
    )

    if not df_resumo_notas.empty:
        tabela_notas = df_resumo_notas.copy()

        tabela_notas["Média"] = tabela_notas[
            "Média"
        ].map(formatar_decimal)

        tabela_notas = tabela_notas.rename(
            columns={
                "Observações":
                    "Observações disponíveis",
            }
        )

        st.dataframe(
            tabela_notas,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# TRAJETÓRIA LONGITUDINAL
# ============================================================

st.write("")
st.write("")

st.subheader("Trajetória dos alunos")

st.caption(
    "Análise longitudinal dos estudantes com informações "
    "comparáveis entre 2022 e 2024, acompanhando o mesmo RA."
)

df_trajetoria = df[
    [
        "RA",
        "ANO",
        "PEDRA",
    ]
].copy()

df_trajetoria["ANO"] = pd.to_numeric(
    df_trajetoria["ANO"],
    errors="coerce",
)

df_trajetoria["PEDRA_PADRAO"] = (
    df_trajetoria["PEDRA"]
    .astype("string")
    .str.strip()
    .str.upper()
)

ordem_pedras = {
    "QUARTZO": 1,
    "AGATA": 2,
    "AMETISTA": 3,
    "TOPAZIO": 4,
}

nomes_pedras = {
    "QUARTZO": "Quartzo",
    "AGATA": "Ágata",
    "AMETISTA": "Ametista",
    "TOPAZIO": "Topázio",
}

df_trajetoria = df_trajetoria[
    df_trajetoria["PEDRA_PADRAO"].isin(
        ordem_pedras.keys()
    )
].copy()

pedras_2022 = (
    df_trajetoria[
        df_trajetoria["ANO"] == 2022
    ][
        [
            "RA",
            "PEDRA_PADRAO",
        ]
    ]
    .drop_duplicates(subset=["RA"])
    .rename(
        columns={
            "PEDRA_PADRAO": "PEDRA_2022"
        }
    )
)

pedras_2024 = (
    df_trajetoria[
        df_trajetoria["ANO"] == 2024
    ][
        [
            "RA",
            "PEDRA_PADRAO",
        ]
    ]
    .drop_duplicates(subset=["RA"])
    .rename(
        columns={
            "PEDRA_PADRAO": "PEDRA_2024"
        }
    )
)

comparacao_pedras = pedras_2022.merge(
    pedras_2024,
    on="RA",
    how="inner",
)

comparacao_pedras["ORDEM_2022"] = (
    comparacao_pedras["PEDRA_2022"]
    .map(ordem_pedras)
)

comparacao_pedras["ORDEM_2024"] = (
    comparacao_pedras["PEDRA_2024"]
    .map(ordem_pedras)
)


def classificar_trajetoria(linha):
    if linha["ORDEM_2024"] > linha["ORDEM_2022"]:
        return "Melhorou"

    if linha["ORDEM_2024"] < linha["ORDEM_2022"]:
        return "Piorou"

    return "Manteve"


if not comparacao_pedras.empty:
    comparacao_pedras["TRAJETORIA"] = (
        comparacao_pedras.apply(
            classificar_trajetoria,
            axis=1,
        )
    )

total_comparavel = len(
    comparacao_pedras
)

if total_comparavel > 0:
    quantidade_melhorou = (
        comparacao_pedras["TRAJETORIA"]
        .eq("Melhorou")
        .sum()
    )

    quantidade_manteve = (
        comparacao_pedras["TRAJETORIA"]
        .eq("Manteve")
        .sum()
    )

    quantidade_piorou = (
        comparacao_pedras["TRAJETORIA"]
        .eq("Piorou")
        .sum()
    )

    percentual_melhorou = (
        quantidade_melhorou
        / total_comparavel
        * 100
    )

    percentual_manteve = (
        quantidade_manteve
        / total_comparavel
        * 100
    )

    percentual_piorou = (
        quantidade_piorou
        / total_comparavel
        * 100
    )

else:
    quantidade_melhorou = 0
    quantidade_manteve = 0
    quantidade_piorou = 0

    percentual_melhorou = float("nan")
    percentual_manteve = float("nan")
    percentual_piorou = float("nan")


t1, t2, t3, t4 = st.columns(4)

with t1:
    st.metric(
        "Alunos comparáveis",
        formatar_inteiro(total_comparavel),
    )

with t2:
    st.metric(
        "Melhoraram",
        formatar_percentual(
            percentual_melhorou
        ),
    )

with t3:
    st.metric(
        "Mantiveram",
        formatar_percentual(
            percentual_manteve
        ),
    )

with t4:
    st.metric(
        "Pioraram",
        formatar_percentual(
            percentual_piorou
        ),
    )

st.write("")

traj1, traj2 = st.columns([1, 1.4])


# ============================================================
# EVOLUÇÃO DA CLASSIFICAÇÃO
# ============================================================

with traj1:
    with st.container(border=True):

        st.markdown(
            (
                '<div class="card-title">'
                'Evolução da classificação'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

        st.caption(
            "Mudança da classificação Pedra entre 2022 e 2024."
        )

        if total_comparavel > 0:
            distribuicao_trajetoria = pd.DataFrame(
                {
                    "Trajetória": [
                        "Melhorou",
                        "Manteve",
                        "Piorou",
                    ],
                    "Alunos": [
                        quantidade_melhorou,
                        quantidade_manteve,
                        quantidade_piorou,
                    ],
                }
            )

            chart = charts.grafico_barras_categorias(
                dados=distribuicao_trajetoria,
                campo_x="Trajetória",
                campo_y="Alunos",
                dominio=[
                    "Melhorou",
                    "Manteve",
                    "Piorou",
                ],
                cores=[
                    charts.TEAL,
                    charts.NAVY,
                    charts.LIGHT_TEAL,
                ],
                titulo_x="Trajetória",
                titulo_y="Alunos",
                altura=380,
            )

            st.altair_chart(
                chart,
                use_container_width=True,
            )
        else:
            st.info(
                "Não há estudantes com classificação Pedra "
                "disponível simultaneamente em 2022 e 2024."
            )


# ============================================================
# DISTRIBUIÇÃO DAS PEDRAS
# ============================================================

with traj2:
    with st.container(border=True):

        st.markdown(
            (
                '<div class="card-title">'
                'Distribuição das Pedras'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

        st.caption(
            "Classificação dos mesmos estudantes em 2022 e 2024."
        )

        if total_comparavel > 0:
            ordem_exibicao = [
                "Quartzo",
                "Ágata",
                "Ametista",
                "Topázio",
            ]

            base_2022 = (
                comparacao_pedras["PEDRA_2022"]
                .map(nomes_pedras)
                .value_counts()
                .reindex(
                    ordem_exibicao,
                    fill_value=0,
                )
            )

            base_2024 = (
                comparacao_pedras["PEDRA_2024"]
                .map(nomes_pedras)
                .value_counts()
                .reindex(
                    ordem_exibicao,
                    fill_value=0,
                )
            )

            distribuicao_pedras = pd.DataFrame(
                {
                    "Pedra":
                        ordem_exibicao * 2,
                    "Ano":
                        ["2022"] * 4
                        + ["2024"] * 4,
                    "Alunos":
                        base_2022.tolist()
                        + base_2024.tolist(),
                }
            )

            # Gráfico construído diretamente com Altair para manter
            # a ordem conceitual das Pedras e evitar incompatibilidades
            # entre versões das funções auxiliares de charts.py.
            import altair as alt

            chart = (
                alt.Chart(distribuicao_pedras)
                .mark_bar(
                    cornerRadiusTopLeft=4,
                    cornerRadiusTopRight=4,
                )
                .encode(
                    x=alt.X(
                        "Pedra:N",
                        title="Pedra",
                        sort=ordem_exibicao,
                        axis=alt.Axis(labelAngle=0),
                    ),
                    xOffset=alt.XOffset(
                        "Ano:N",
                        sort=["2022", "2024"],
                    ),
                    y=alt.Y(
                        "Alunos:Q",
                        title="Alunos",
                        scale=alt.Scale(zero=True),
                    ),
                    color=alt.Color(
                        "Ano:N",
                        title=None,
                        sort=["2022", "2024"],
                        scale=alt.Scale(
                            domain=["2022", "2024"],
                            range=[charts.NAVY, charts.TEAL],
                        ),
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "Pedra:N",
                            title="Pedra",
                        ),
                        alt.Tooltip(
                            "Ano:N",
                            title="Ano",
                        ),
                        alt.Tooltip(
                            "Alunos:Q",
                            title="Alunos",
                            format=",.0f",
                        ),
                    ],
                )
                .properties(height=380)
                .configure_view(stroke=None)
                .configure_axis(
                    labelColor="#527087",
                    titleColor="#143A59",
                    domainColor="#DDEAF0",
                    tickColor="#DDEAF0",
                    gridColor="#E8F0F4",
                    gridOpacity=0.75,
                    labelFontSize=12,
                    titleFontSize=12,
                    titleFontWeight=500,
                    labelPadding=8,
                    titlePadding=12,
                )
                .configure_legend(
                    labelColor="#527087",
                    titleColor="#143A59",
                    labelFontSize=12,
                    titleFontSize=12,
                    orient="bottom",
                    padding=8,
                )
            )

            st.altair_chart(
                chart,
                use_container_width=True,
            )


# ============================================================
# TRANSIÇÕES
# ============================================================

with st.expander("Detalhamento das transições"):

    if total_comparavel > 0:
        tabela_transicoes = comparacao_pedras.copy()

        tabela_transicoes["PEDRA_2022"] = (
            tabela_transicoes["PEDRA_2022"]
            .map(nomes_pedras)
        )

        tabela_transicoes["PEDRA_2024"] = (
            tabela_transicoes["PEDRA_2024"]
            .map(nomes_pedras)
        )

        tabela_transicoes = (
            tabela_transicoes
            .groupby(
                [
                    "PEDRA_2022",
                    "PEDRA_2024",
                ]
            )
            .size()
            .reset_index(name="Alunos")
            .rename(
                columns={
                    "PEDRA_2022":
                        "Pedra em 2022",
                    "PEDRA_2024":
                        "Pedra em 2024",
                }
            )
            .sort_values(
                "Alunos",
                ascending=False,
            )
        )

        st.dataframe(
            tabela_transicoes,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# METODOLOGIA LONGITUDINAL
# ============================================================

with st.expander("Sobre a análise longitudinal"):

    st.markdown(
        """
Esta seção acompanha o mesmo estudante por meio do
identificador **RA**.

A comparação considera somente estudantes com classificação
**Pedra** disponível simultaneamente em **2022 e 2024**.

A hierarquia utilizada é:

**Quartzo → Ágata → Ametista → Topázio**

Assim:

- avanço para uma classificação superior = **Melhorou**;
- permanência na mesma classificação = **Manteve**;
- mudança para uma classificação inferior = **Piorou**.

Diferentemente das análises agregadas anteriores, esta seção
acompanha uma população comparável de estudantes.

Os resultados são descritivos e, isoladamente, não estabelecem
uma relação causal entre a participação no programa e a evolução
observada.
        """
    )
