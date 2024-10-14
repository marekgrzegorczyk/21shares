import ccxt
import pandas as pd
import streamlit as st


exchange = ccxt.binance()


# Added st.cache_data decorator to fetch_binance_ohlcv function to cache the data and improve the performance of the application.
# show_spinner parameter is set to True to display a spinner while the data is being fetched.
@st.cache_data(show_spinner=True)
def fetch_binance_ohlcv(  # Renamed fetch_ohlcv to fetch_binance_ohlcv to be more precise what exchange is used.
    coin: str, timeframe: str = "1m", limit: int = 100
) -> pd.DataFrame:

    try:
        # Added try-except block to handle exceptions when fetching data.
        ohlcv = exchange.fetch_ohlcv(coin, timeframe=timeframe, limit=limit)
        data = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
        return data

    except Exception as e:
        error_message = f"Error fetching data: {str(e)}"
        # Return dataframe with the error message
        error_df = pd.DataFrame({"error": [error_message]})
        return error_df
