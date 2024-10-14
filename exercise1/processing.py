import numpy as np
import pandas as pd
import streamlit as st

from query import fetch_historical_data


# Function to calculate the required metrics
@st.cache_data(show_spinner=True)
def calculate_metrics(
    portfolio_returns, benchmark_returns, risk_free_rate=0.0, window=20
):
    """
    Calculates various performance and risk metrics for the portfolio.
    """

    # Risk Metrics
    var_95 = portfolio_returns.quantile(0.05) * 100
    annual_volatility = portfolio_returns.std() * np.sqrt(252) * 100
    max_drawdown = (portfolio_returns / portfolio_returns.cummax() - 1).min() * 100
    tracking_error = np.std(portfolio_returns - benchmark_returns) * np.sqrt(252) * 100
    information_ratio = (
        (portfolio_returns - benchmark_returns).mean()
        / (portfolio_returns - benchmark_returns).std()
        * np.sqrt(252)
    )

    common_index = portfolio_returns.index.intersection(benchmark_returns.index)
    portfolio_returns = portfolio_returns.reindex(common_index)
    benchmark_returns = benchmark_returns.reindex(common_index)

    # # Calculate Rolling Hit Ratio (corrected)
    # def compare_windows(x):
    #     # Ensure both windows have the same length
    #     if len(x) == window:
    #         return (x > benchmark_returns[x.index].shift(1)).mean()  # Removed .values
    #     else:
    #         return np.nan  # Return NaN for incomplete windows
    #
    # rolling_hit_ratio = (
    #     portfolio_returns.rolling(window=window)
    #     .apply(compare_windows, raw=True)  # Use raw=True for efficiency
    #     .fillna(method="bfill")
    #     * 100
    # )
    # rolling_hit_ratio = rolling_hit_ratio.iloc[-1]

    portfolio_cummax = (1 + portfolio_returns).cumprod()
    benchmark_cummax = (1 + benchmark_returns).cumprod()
    relative_drawdown = (portfolio_cummax / benchmark_cummax - 1).min() * 100

    # Performance Metrics
    cumulative_returns = (1 + portfolio_returns).cumprod() - 1
    cumulative_returns = cumulative_returns.iloc[-1] * 100
    annual_returns = (
        (1 + portfolio_returns).cumprod().iloc[-1] ** (252 / len(portfolio_returns)) - 1
    ) * 100
    sharpe_ratio = (annual_returns / 100 - risk_free_rate) / (annual_volatility / 100)

    # Sortino Ratio
    downside_returns = portfolio_returns[portfolio_returns < 0]
    downside_std = downside_returns.std() * np.sqrt(252)
    sortino_ratio = (annual_returns / 100 - risk_free_rate) / (downside_std)

    # Alpha and Beta
    covariance_matrix = np.cov(portfolio_returns, benchmark_returns)
    beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
    alpha = (
        annual_returns / 100 - risk_free_rate - beta * (benchmark_returns.mean() * 252)
    )
    alpha = alpha * 100

    # Turnover Rate (example calculation - you'll need to adapt this)
    turnover_data = (
        np.random.rand(len(portfolio_returns)) * 0.2
    )  # Random turnover between 0% and 20%
    turnover_rate = np.mean(turnover_data) * 100

    return {
        "Cumulative Returns": cumulative_returns,
        "Annual Returns": annual_returns,
        "Annual Volatility": annual_volatility,
        "Max Drawdown": max_drawdown,
        "Sharpe Ratio": sharpe_ratio,
        "Sortino Ratio": sortino_ratio,
        "Beta": beta,
        "Alpha": alpha,
        "VaR 95%": var_95,
        "Tracking Error": tracking_error,
        "Information Ratio": information_ratio,
        # "Hit Ratio": hit_ratio,
        # "Rolling Hit Ratio": rolling_hit_ratio,
        "Relative Drawdown": relative_drawdown,
        "Turnover Rate": turnover_rate,
    }


# Calculate performance from price data
def calculate_performance(prices):
    return (prices / prices.iloc[0] - 1) * 100  # Return percentage performance


# Calculate the weighted returns for the portfolio
@st.cache_data(show_spinner=True)
def calculate_weighted_returns(assets, allocations, period):
    asset_returns = pd.DataFrame()
    for asset, allocation in zip(assets, allocations):
        data = fetch_historical_data(asset, period)
        asset_returns[asset] = data.pct_change() * allocation
    portfolio_returns = asset_returns.sum(axis=1)
    return portfolio_returns.dropna()
