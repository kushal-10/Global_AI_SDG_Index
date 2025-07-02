import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# ——— Load data ———
df = pd.read_csv(
    os.path.join("src_zh", "results", "results_expanded.csv"),
    index_col=0
)

palette = px.colors.qualitative.Vivid

def plot_passage_stage_comparison(
    df,
    stage1_col: str,
    stage2_col: str,
    stage1_label: str,
    stage2_label: str,
    title: str,
    width1: float = 0.8,
    width2: float = 0.3,
    log_y: bool = True
):
    """
    Overlay two passage‐count columns by country.

    Parameters
    ----------
    df
        Original DataFrame with a 'Country' column plus your two stages.
    stage1_col, stage2_col
        Column names in df to compare.
    stage1_label, stage2_label
        Legend labels for the two bars.
    title
        Plot title.
    width1, width2
        Relative bar widths for stage1 and stage2.
    log_y
        Whether to use a log scale on the Y axis.
    """
    # 1) Sum up each stage by country
    agg = (
        df
        .groupby("Country", as_index=False)[[stage1_col, stage2_col]]
        .sum()
    )
    countries = agg["Country"]
    vals1     = agg[stage1_col]
    vals2     = agg[stage2_col]

    # 2) Build overlayed bar traces
    fig = go.Figure([
        go.Bar(
            x=countries,
            y=vals1,
            name=stage1_label,
            marker=dict(color=palette[1], opacity=0.8),
            width=width1
        ),
        go.Bar(
            x=countries,
            y=vals2,
            name=stage2_label,
            marker=dict(color=palette[3], opacity=1),
            width=width2
        )
    ])

    # 3) Layout tweaks
    fig.update_layout(
        title=title,
        barmode="overlay",
        xaxis_tickangle=-45,
        yaxis_type="log" if log_y else "linear",
        yaxis=dict(title="Number of Passages" + (" (log scale)" if log_y else "")),
        legend=dict(title=""),
    )

    fig.show()
    return fig

if __name__ == "__main__":
    # plot_passage_stage_comparison(
    #     df,
    #     stage1_col="Total Passages",
    #     stage2_col="Passages after Filter 2",
    #     stage1_label="Total Passages",
    #     stage2_label="Passages passed through the Filter",
    #     title="Passages by Country: Total Passages vs Passages passing through the Filter"
    # )

    # # Filter 1 vs Filter 2
    # plot_passage_stage_comparison(
    #     df,
    #     stage1_col="Passages after Filter 1",
    #     stage2_col="Passages after Filter 2",
    #     stage1_label="After Filter 1",
    #     stage2_label="After Filter 2",
    #     title="Passages by Country: After Filter 1 vs After Filter 2"
    # )
    #
    # Filter 2 vs Classification
    plot_passage_stage_comparison(
        df,
        stage1_col="Passages after Filter 2",
        stage2_col="Passages after Classification into SDGs",
        stage1_label="Passages that mention AI related Keywords",
        stage2_label="Passages that use AI towards SDG development",
        title="Passages by Country: Passages that use AI towards SDG development vs Passages that mention AI related Keywords",
        log_y=False
    )
