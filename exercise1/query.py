import streamlit as st
import yfinance as yf


# Fetch asset data from yfinance
def fetch_asset_data(ticker):
    """
    Fetch asset data using the yfinance API. Returns the long name, symbol, and type of the asset.
    """
    try:
        asset = yf.Ticker(ticker)
        return (
            asset.info.get("longName"),
            asset.info.get("symbol"),
            asset.info.get("quoteType"),
        )
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None, None, None


#   Fetch benchmark data from yfinance
def fetch_benchmark_data(benchmark_ticker, period):
    """
    Fetch historical benchmark data from yfinance for the selected period.
    """
    benchmark = yf.Ticker(benchmark_ticker)
    return benchmark.history(period=period)["Close"]


# Fetch historical data from yfinance
def fetch_historical_data(ticker, period):
    asset = yf.Ticker(ticker)
    return asset.history(period=period)["Close"]
