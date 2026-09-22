import altair as alt


# ============================================================
# IDENTIDADE VISUAL
# ============================================================

NAVY = "#073B63"
BLUE = "#0B5F82"
TEAL = "#18A6A6"
LIGHT_TEAL = "#69D4D0"

# Cores de apoio da identidade visual
SKY = "#42A5D9"
GREEN = "#45B98C"
AMBER = "#F2B544"
CORAL = "#F47C6C"
PURPLE = "#8B73C7"

TEXT = "#143A59"
MUTED = "#527087"
GRID = "#E8F0F4"
BORDER = "#DDEAF0"

SOFT_BLUE = "#8FBFD0"
SOFT_TEAL = "#A7DDDA"


# ============================================================
# CONFIGURAÇÃO BASE
# ============================================================

def aplicar_tema(chart):
    """
    Aplica o padrão visual da aplicação aos gráficos Altair.
    """

    return (
        chart
        .configure_view(
            stroke=None
        )
        .configure_axis(
            labelColor=MUTED,
            titleColor=TEXT,
            domainColor=BORDER,
            tickColor=BORDER,
            gridColor=GRID,
            gridOpacity=0.75,
            labelFontSize=12,
            titleFontSize=12,
            titleFontWeight=500,
            labelPadding=8,
            titlePadding=12,
        )
        .configure_legend(
            labelColor=MUTED,
            titleColor=TEXT,
            labelFontSize=12,
            titleFontSize=12,
            orient="bottom",
            padding=8,
        )
    )


# ============================================================
# BARRAS SIMPLES
# ============================================================

def grafico_barras(
    dados,
    campo_x,
    campo_y,
    titulo_x=None,
    titulo_y=None,
    ordem=None,
    cor=BLUE,
    formato_tooltip=".2f",
    altura=340,
):
    """
    Gráfico de barras vertical para uma única série.
    """

    chart = (
        alt.Chart(dados)
        .mark_bar(
            color=cor,
            cornerRadiusTopLeft=6,
            cornerRadiusTopRight=6,
        )
        .encode(
            x=alt.X(
                f"{campo_x}:N",
                title=titulo_x,
                sort=ordem,
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y(
                f"{campo_y}:Q",
                title=titulo_y,
                scale=alt.Scale(zero=True),
            ),
            tooltip=[
                alt.Tooltip(
                    f"{campo_x}:N",
                    title=titulo_x or campo_x,
                ),
                alt.Tooltip(
                    f"{campo_y}:Q",
                    title=titulo_y or campo_y,
                    format=formato_tooltip,
                ),
            ],
        )
        .properties(
            height=altura
        )
    )

    return aplicar_tema(chart)


# ============================================================
# BARRAS POR CATEGORIA
# ============================================================

def grafico_barras_categorias(
    dados,
    campo_x,
    campo_y,
    dominio,
    cores,
    titulo_x=None,
    titulo_y=None,
    formato_tooltip=",.0f",
    altura=340,
):
    """
    Gráfico de barras com uma cor definida por categoria.
    """

    chart = (
        alt.Chart(dados)
        .mark_bar(
            cornerRadiusTopLeft=6,
            cornerRadiusTopRight=6,
        )
        .encode(
            x=alt.X(
                f"{campo_x}:N",
                title=titulo_x,
                sort=dominio,
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y(
                f"{campo_y}:Q",
                title=titulo_y,
                scale=alt.Scale(zero=True),
            ),
            color=alt.Color(
                f"{campo_x}:N",
                scale=alt.Scale(
                    domain=dominio,
                    range=cores,
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip(
                    f"{campo_x}:N",
                    title=titulo_x or campo_x,
                ),
                alt.Tooltip(
                    f"{campo_y}:Q",
                    title=titulo_y or campo_y,
                    format=formato_tooltip,
                ),
            ],
        )
        .properties(
            height=altura
        )
    )

    return aplicar_tema(chart)


# ============================================================
# LINHA SIMPLES
# ============================================================

def grafico_linha(
    dados,
    campo_x,
    campo_y,
    titulo_x=None,
    titulo_y=None,
    cor=TEAL,
    formato_tooltip=".1f",
    dominio_y=None,
    altura=340,
):
    """
    Gráfico temporal para uma única série.
    """

    if dominio_y is not None:
        escala_y = alt.Scale(
            domain=dominio_y
        )
    else:
        escala_y = alt.Scale(
            zero=False
        )

    chart = (
        alt.Chart(dados)
        .mark_line(
            color=cor,
            strokeWidth=3,
            point=alt.OverlayMarkDef(
                filled=True,
                size=90,
                color=cor,
            ),
        )
        .encode(
            x=alt.X(
                f"{campo_x}:O",
                title=titulo_x,
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y(
                f"{campo_y}:Q",
                title=titulo_y,
                scale=escala_y,
            ),
            tooltip=[
                alt.Tooltip(
                    f"{campo_x}:O",
                    title=titulo_x or campo_x,
                ),
                alt.Tooltip(
                    f"{campo_y}:Q",
                    title=titulo_y or campo_y,
                    format=formato_tooltip,
                ),
            ],
        )
        .properties(
            height=altura
        )
    )

    return aplicar_tema(chart)


# ============================================================
# LINHAS MÚLTIPLAS
# ============================================================

def grafico_linhas(
    dados,
    campo_x,
    campos_y,
    titulo_x=None,
    titulo_y=None,
    altura=340,
):
    """
    Gráfico temporal com múltiplas séries.
    """

    dados_longos = dados.melt(
        id_vars=[campo_x],
        value_vars=campos_y,
        var_name="Série",
        value_name="Valor",
    )

    dados_longos = dados_longos.dropna(
        subset=["Valor"]
    )

    chart = (
        alt.Chart(dados_longos)
        .mark_line(
            strokeWidth=2.6,
            point=alt.OverlayMarkDef(
                filled=True,
                size=65,
            ),
        )
        .encode(
            x=alt.X(
                f"{campo_x}:O",
                title=titulo_x,
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y(
                "Valor:Q",
                title=titulo_y,
                scale=alt.Scale(zero=False),
            ),
            color=alt.Color(
                "Série:N",
                title=None,
                scale=alt.Scale(
                    range=[
                        NAVY,
                        TEAL,
                        BLUE,
                        LIGHT_TEAL,
                        "#397C9D",
                        "#5DB8B5",
                        "#87AFC1",
                    ]
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    f"{campo_x}:O",
                    title=titulo_x or campo_x,
                ),
                alt.Tooltip(
                    "Série:N",
                    title="Indicador",
                ),
                alt.Tooltip(
                    "Valor:Q",
                    title="Média",
                    format=".2f",
                ),
            ],
        )
        .properties(
            height=altura
        )
    )

    return aplicar_tema(chart)


# ============================================================
# BARRAS AGRUPADAS
# ============================================================

def grafico_barras_agrupadas(
    dados,
    campo_categoria,
    campo_grupo,
    campo_valor,
    ordem=None,
    dominio_grupo=None,
    cores=None,
    titulo_x=None,
    titulo_y=None,
    formato_tooltip=",.0f",
    altura=340,
):
    """
    Gráfico de barras agrupadas para comparação entre períodos.
    """

    if cores is None:
        cores = [
            NAVY,
            TEAL,
            LIGHT_TEAL,
        ]

    if dominio_grupo is not None:

        escala_cor = alt.Scale(
            domain=dominio_grupo,
            range=cores,
        )

    else:

        escala_cor = alt.Scale(
            range=cores,
        )

    chart = (
        alt.Chart(dados)
        .mark_bar(
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4,
        )
        .encode(
            x=alt.X(
                f"{campo_categoria}:N",
                title=titulo_x,
                sort=ordem,
                axis=alt.Axis(labelAngle=0),
            ),
            xOffset=alt.XOffset(
                f"{campo_grupo}:N"
            ),
            y=alt.Y(
                f"{campo_valor}:Q",
                title=titulo_y,
                scale=alt.Scale(zero=True),
            ),
            color=alt.Color(
                f"{campo_grupo}:N",
                title=None,
                scale=escala_cor,
            ),
            tooltip=[
                alt.Tooltip(
                    f"{campo_categoria}:N",
                    title=titulo_x or campo_categoria,
                ),
                alt.Tooltip(
                    f"{campo_grupo}:N",
                    title="Período",
                ),
                alt.Tooltip(
                    f"{campo_valor}:Q",
                    title=titulo_y or campo_valor,
                    format=formato_tooltip,
                ),
            ],
        )
        .properties(
            height=altura
        )
    )

    return aplicar_tema(chart)