import os
import pandas as pd
import plotly.graph_objects as go

# ——— Load data ———
df = pd.read_csv(
    os.path.join("src_zh", "results", "results_expanded.csv"),
    index_col=0
)

def plot_passage_stage_comparison(
    df: pd.DataFrame,
    stage1_col: str,
    stage2_col: str,
    stage1_label: str,
    stage2_label: str,
    title: str,
    normalize: bool = False,
    normalize_by: str = "Total Passages",
    width1: float = 0.8,
    width2: float = 0.3,
    log_y: bool = True
):
    """
    Overlay two passage‐count columns by country, optionally normalizing
    each by the total passages for that country.

    Parameters
    ----------
    df
        DataFrame containing 'Country', the two stage cols, and normalize_by col.
    stage1_col, stage2_col
        Column names to compare (e.g. "Passages after Filter 1").
    stage1_label, stage2_label
        What shows up in the legend.
    title
        Plot title.
    normalize
        If True, divides each stage's total by the normalize_by column.
    normalize_by
        Column to normalize against (must exist in df).
    width1, width2
        Bar widths for the two traces.
    log_y
        Whether to use a log‐scale Y axis (ignored if normalize=True).
    """
    # 1) pick which columns to sum
    cols = [stage1_col, stage2_col]
    if normalize:
        cols.append(normalize_by)

    # 2) aggregate sums by country
    agg = (
        df
        .groupby("Country", as_index=False)[cols]
        .sum()
    )

    # 3) extract x + y values
    countries = agg["Country"]
    if normalize:
        total = agg[normalize_by]
        y1 = agg[stage1_col] / total
        y2 = agg[stage2_col] / total
        ylabel = f"Fraction of {normalize_by}"
        # on a fraction/percent scale we usually go linear
        axis_type = "linear"
    else:
        y1 = agg[stage1_col]
        y2 = agg[stage2_col]
        ylabel = "Number of Passages" + (" (log scale)" if log_y else "")
        axis_type = "log" if log_y else "linear"

    # 4) build the overlaid bars
    fig = go.Figure([
        go.Bar(
            x=countries,
            y=y1,
            name=stage1_label,
            marker=dict(opacity=0.8),
            width=width1
        ),
        go.Bar(
            x=countries,
            y=y2,
            name=stage2_label,
            marker=dict(opacity=1.0),
            width=width2
        )
    ])

    # 5) layout tweaks
    fig.update_layout(
        title=title,
        barmode="overlay",
        xaxis_tickangle=-45,
        yaxis_type=axis_type,
        yaxis=dict(title=ylabel, tickformat=".2f" if normalize else ".0f"),
        legend=dict(title="")
    )

    fig.show()
    return fig

if __name__ == "__main__":
    # 1) After Filter 1 vs After Filter 2, *normalized* by total passages
    plot_passage_stage_comparison(
        df,
        stage1_col="Passages after Filter 1",
        stage2_col="Passages after Filter 2",
        stage1_label="After Filter 1",
        stage2_label="After Filter 2",
        title="Passages by Country: Filter 1 vs Filter 2 (as fraction of total)",
        normalize=True
    )

    # 2) After Filter 2 vs After Classification, *normalized*
    plot_passage_stage_comparison(
        df,
        stage1_col="Passages after Filter 2",
        stage2_col="Passages after Classification into SDGs",
        stage1_label="After Filter 2",
        stage2_label="After Classification",
        title="Passages by Country: Filter 2 vs Classification (fraction of total)",
        normalize=True
    )
