import numpy as np
import plotly.graph_objects as go
import streamlit as st
import pandas as pd


def placeholder_chart():
    # Create a placeholder chart
    dates = pd.date_range(start="2023-01-01", periods=12, freq="M")
    placeholder_performance = np.zeros(len(dates))

    # Create Plotly figure
    fig = go.Figure()

    # Add a line that remains at zero
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=placeholder_performance,
            mode="lines",
            name="Performance",
            line=dict(color="grey", width=2, dash="dash"),
        )
    )

    # Add annotation to inform the user
    fig.add_annotation(
        text="Add assets to generate the chart",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=True,
        font=dict(size=16, color="grey"),
    )

    # Update layout to match the clean style
    fig.update_layout(
        # title="Performance",
        xaxis_title="Date",
        yaxis_title="Performance (%)",
        template="simple_white",
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
    )

    # Update the x-axis to show date formatting
    fig.update_xaxes(
        tickformat="%b %Y",
        showgrid=False,
    )

    # Update y-axis for percentages
    fig.update_yaxes(
        ticksuffix="%",
        showgrid=True,
        gridcolor="lightgrey",
    )

    # Display chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)


# def plot_performance_chart(user_assets, selected_filter):
#     spx_ticker = "^GSPC"  # S&P 500 Index
#
#     selected_period = filter_periods[selected_filter]
#     spx_prices = get_historical_data(spx_ticker, selected_period)
#     benchmark_prices = sum(
#         [get_historical_data(ticker, selected_period) for ticker in user_assets]
#     ) / len(user_assets)
#
#     # Calculate performance for SPX and Benchmark
#     spx_performance = calculate_performance(spx_prices)
#     benchmark_performance = calculate_performance(benchmark_prices)
#
#     # Create Plotly figure
#     fig = go.Figure()
#
#     # Add SPX performance line
#     fig.add_trace(
#         go.Scatter(
#             x=spx_performance.index,
#             y=spx_performance.values,
#             mode="lines",
#             name="SPX",
#             line=dict(color="orange", width=2),
#         )
#     )
#
#     # Add Benchmark performance line
#     fig.add_trace(
#         go.Scatter(
#             x=benchmark_performance.index,
#             y=benchmark_performance.values,
#             mode="lines",
#             name="Benchmark",
#             line=dict(color="black", width=2),
#         )
#     )
#
#     # Update layout to match the clean style
#     fig.update_layout(
#         xaxis_title="Date",
#         yaxis_title="Performance (%)",
#         template="simple_white",
#         showlegend=True,
#         margin=dict(l=20, r=20, t=40, b=20),
#         height=400,
#     )
#
#     # Update the x-axis to show date formatting
#     fig.update_xaxes(
#         tickformat=("%b %Y" if selected_filter not in ["1D", "1W"] else "%H:%M"),
#         showgrid=False,
#     )
#
#     # Update y-axis for percentages
#     fig.update_yaxes(
#         ticksuffix="%",
#         showgrid=True,
#         gridcolor="lightgrey",
#     )
#
#     # Display chart in Streamlit
#     st.plotly_chart(fig, use_container_width=True)
