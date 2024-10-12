import matplotlib.pyplot as plt
import pandas as pd


def plot_cumulative_returns(cumulative_returns: pd.Series) -> None:
    """
    Plot the cumulative returns of a portfolio.

    Args:
        cumulative_returns (pd.Series): Series of cumulative returns with dates as index.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_returns, label='Cumulative Returns')
    plt.title('Portfolio Cumulative Returns')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
