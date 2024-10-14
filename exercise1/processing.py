import numpy as np
import pandas as pd


# Function to calculate the required metrics
def calculate_metrics(portfolio_returns, benchmark_returns, risk_free_rate=0.01):
    """
    Calculate risk and performance metrics for the portfolio.
    """
    # Join the portfolio and benchmark returns
    data = pd.DataFrame(
        {"portfolio": portfolio_returns, "benchmark": benchmark_returns}
    ).dropna()

    # Cumulative Returns
    cumulative_returns = (1 + data["portfolio"]).cumprod() - 1

    # Annualized Returns
    annual_returns = (
        data["portfolio"].mean() * 252
    )  # Assuming 252 trading days in a year

    # Annual Volatility
    annual_volatility = data["portfolio"].std() * np.sqrt(252)

    # Maximum Drawdown
    cumulative_max = (1 + data["portfolio"]).cummax()
    max_drawdown = ((cumulative_max - (1 + data["portfolio"])) / cumulative_max).max()

    # Sharpe Ratio
    sharpe_ratio = (annual_returns - risk_free_rate) / annual_volatility

    # Sortino Ratio (only considering negative volatility)
    downside_std = data["portfolio"][data["portfolio"] < 0].std() * np.sqrt(252)
    sortino_ratio = (
        (annual_returns - risk_free_rate) / downside_std
        if downside_std != 0
        else np.nan
    )

    # Beta (portfolio sensitivity to the benchmark)
    covariance_matrix = data.cov()
    beta = (
        covariance_matrix.loc["portfolio", "benchmark"]
        / covariance_matrix.loc["benchmark", "benchmark"]
    )

    # Alpha (portfolio's excess return over the benchmark)
    benchmark_annual_returns = data["benchmark"].mean() * 252
    alpha = annual_returns - beta * benchmark_annual_returns

    # Value at Risk (VaR 95%)
    var_95 = np.percentile(data["portfolio"], 5)

    # Tracking Error
    tracking_error = np.std(data["portfolio"] - data["benchmark"]) * np.sqrt(252)

    # Information Ratio
    information_ratio = (
        (annual_returns - benchmark_annual_returns) / tracking_error
        if tracking_error != 0
        else np.nan
    )

    # Hit Ratio (percentage of periods where portfolio outperformed the benchmark)
    hit_ratio = (data["portfolio"] > data["benchmark"]).mean()

    # Rolling Hit Ratio (calculated over a rolling window of 20 periods, for example)
    rolling_hit_ratio = (
        data["portfolio"]
        .rolling(window=20)
        .apply(lambda x: (x > data["benchmark"].rolling(window=20).mean()).mean())
        .mean()
    )

    return {
        "Cumulative Returns": cumulative_returns.iloc[-1],
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
        "Hit Ratio": hit_ratio,
        "Rolling Hit Ratio": rolling_hit_ratio,
    }
