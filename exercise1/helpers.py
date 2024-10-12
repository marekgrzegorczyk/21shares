import numpy as np
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf


def fetch_ticker_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


def normalize_weights(weights):
    total = sum(weights)
    return [w / total * 100 for w in weights]


def plot_performance_chart(dates, spx_data, benchmark_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=spx_data, mode='lines', name='SPX'))
    fig.add_trace(
        go.Scatter(x=dates, y=benchmark_data, mode='lines', name='Benchmark'))
    return fig


def calculate_var(returns, confidence_level=0.95):
    sorted_returns = np.sort(returns)
    var_index = int((1 - confidence_level) * len(sorted_returns))
    var = sorted_returns[var_index]
    return var


def df_in_container(data, subheader_text):
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 1], vertical_alignment="bottom")

        with col1:
            st.write(subheader_text)

        with col2:
            st.number_input(label="", value=0.1, min_value=0.1,
                            max_value=100.0,
                            step=0.1, format="%0.1f",
                            key=f"input_{subheader_text}", )

        with col3:
            st.button("\+", key=f"add_{subheader_text}")

        st.dataframe(data, hide_index=True, use_container_width=True)
