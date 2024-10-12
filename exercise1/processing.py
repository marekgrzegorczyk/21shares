import numpy as np
import pandas as pd


def calculate_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    # Calculate daily returns from price data
    return prices.pct_change().dropna()


def calculate_weighted_returns(daily_returns: pd.DataFrame,
                               weights: np.ndarray) -> pd.Series:
    # Calculate portfolio weighted returns based on asset weights
    return daily_returns.mul(weights, axis=1).sum(axis=1)


def calculate_cumulative_returns(prices: pd.DataFrame,
                                 weights: np.ndarray) -> pd.Series:
    # Calculate the cumulative returns of a portfolio.
    daily_returns = calculate_daily_returns(prices)
    weighted_returns = calculate_weighted_returns(daily_returns, weights)
    return (1 + weighted_returns).cumprod() - 1


def calculate_var_95(weighted_returns: pd.Series) -> float:
    # Calculate the 95% Value at Risk (VaR) for the portfolio.
    return np.percentile(weighted_returns, 5)


def calculate_annual_volatility(weighted_returns: pd.Series) -> float:
    # Calculate the annualized volatility of the portfolio.
    return weighted_returns.std() * np.sqrt(252)


def calculate_max_drawdown(cumulative_returns: pd.Series) -> float:
    # Calculate the maximum drawdown for the portfolio.
    rolling_max = cumulative_returns.cummax()
    drawdown = cumulative_returns - rolling_max
    return drawdown.min()


def calculate_risk_metrics(prices: pd.DataFrame, weights: np.ndarray) -> dict:
    # Calculate risk metrics for a portfolio including VaR, annual volatility, and max drawdown.

    daily_returns = calculate_daily_returns(prices)
    weighted_returns = calculate_weighted_returns(daily_returns, weights)

    cumulative_returns = (1 + weighted_returns).cumprod()

    return {
        "VaR 95%": calculate_var_95(weighted_returns),
        "Annual Volatility": calculate_annual_volatility(weighted_returns),
        "Max Drawdown": calculate_max_drawdown(cumulative_returns)
    }


import pandas as pd


def filter_data_by_time_period(data, time_filter):
    # Filters the data based on the selected time filter.

    if time_filter == '1D':
        return data.tail(1)  # Last day
    elif time_filter == '1W':
        return data.last('7D')  # Last week
    elif time_filter == '1M':
        return data.last('1M')  # Last month
    elif time_filter == '6M':
        return data.last('6M')  # Last 6 months
    elif time_filter == 'YTD':
        start_of_year = pd.Timestamp.now().replace(month=1, day=1)
        return data.loc[start_of_year:]
    elif time_filter == '1Y':
        return data.last('1Y')  # Last year
    elif time_filter == 'Max':
        return data  # Full data range
    else:
        return data  # Default to full data if unknown filter
