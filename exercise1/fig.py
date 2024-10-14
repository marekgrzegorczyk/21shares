import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def placeholder_chart():
    dates = pd.date_range(start="2023-01-01", periods=12, freq="M")
    placeholder_performance = np.zeros(len(dates))

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=placeholder_performance,
            mode="lines",
            name="Performance",
            line=dict(color="grey", width=2, dash="dash"),
        )
    )

    fig.add_annotation(
        text="Add assets to generate the chart",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=True,
        font=dict(size=16, color="grey"),
    )

    fig.update_layout(
        # title="Performance",
        xaxis_title="Date",
        yaxis_title="Performance (%)",
        template="simple_white",
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
    )

    fig.update_xaxes(
        tickformat="%b %Y",
        showgrid=False,
    )

    fig.update_yaxes(
        ticksuffix="%",
        showgrid=True,
        gridcolor="lightgrey",
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_cumulative_returns(portfolio_returns, benchmark_returns, benchmark_name):
    """
    Generates a Plotly chart showing cumulative returns of the portfolio
    compared to the benchmark (S&P 500).
    """
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=portfolio_returns.index,
            y=(1 + portfolio_returns).cumprod() * 100,
            mode="lines",
            name="Portfolio",
            line=dict(color="black"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=benchmark_returns.index,
            y=(1 + benchmark_returns).cumprod() * 100,
            mode="lines",
            name=benchmark_name,
            line=dict(color="#ff6a1f"),
        )
    )
    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="Cumulative Return (%)",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )
    return st.plotly_chart(fig, use_container_width=True)


# @st.cache_data(show_spinner=True)
def display_metrics_table(metrics):
    """
    Display the calculated metrics in a Streamlit table, formatted
    to resemble the provided image.
    """
    # Create a list of tuples (metric_name, metric_value)
    metric_list = [
        ("startDate", "-"),  # Placeholder for start date
        ("EndDate", pd.Timestamp.today().strftime("%d/%m/%Y")),
        ("cumulativeRet", f"{metrics['Cumulative Returns']:.1f}%"),
        ("annRet", f"{metrics['Annual Returns']:.1f}%"),
        ("annVol", f"{metrics['Annual Volatility']:.1f}%"),
        ("sharpeRatio", f"{metrics['Sharpe Ratio']:.2f}"),
        ("sortinoRatio", f"{metrics['Sortino Ratio']:.2f}"),
        ("infoRatio", f"{metrics['Information Ratio']:.2f}"),
        (
            "Tracking Ratio",
            f"{metrics['Tracking Error']:.1f}%",
        ),  # Using Tracking Error here
        ("maxDrawdown", f"{metrics['Max Drawdown']:.1f}%"),
        ("VaR95 (monthly)", "-"),  # Placeholder for monthly VaR
        ("VaR95 (annually)", "-"),  # Placeholder for annual VaR
        # ("HitRatio", f"{metrics['Hit Ratio']:.0f}%"),
        ("1Y_RollingHitRatior", "-"),  # Placeholder
        ("3Y_RollingHitRatior", "-"),  # Placeholder
        ("maxRelativeDrawd", f"{metrics['Relative Drawdown']:.1f}%"),
        ("1Y", "-"),  # Placeholder
        ("3Y", "-"),  # Placeholder
        ("5Y", "-"),  # Placeholder
        ("alpha (vs SP500)", f"{metrics['Alpha']:.1f}%"),
        ("beta (vs SP500)", f"{metrics['Beta']:.1f}%"),
        ("turnover (ann)", f"{metrics['Turnover Rate']:.1f}%"),
    ]

    # Create a DataFrame for better display
    metrics_df = pd.DataFrame(metric_list, columns=["KPI", "Benchmark"])
    st.dataframe(data=metrics_df, hide_index=True, use_container_width=True, height=775)
