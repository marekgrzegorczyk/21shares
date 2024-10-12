import pandas as pd
import streamlit as st

from fig import plot_cumulative_returns
from processing import calculate_cumulative_returns, calculate_risk_metrics, \
    filter_data_by_time_period
from query import fetch_yfinance_data

# Sidebar for user inputs
st.sidebar.title('Portfolio Composition')
st.sidebar.markdown("#### Equity")
tickers_equity = st.sidebar.multiselect('Add Equity',
                                        ['AAPL', 'MSFT', 'NVDA', 'GOOGL'],
                                        key='equity')
st.sidebar.markdown("#### Fixed Income")
tickers_fixed_income = st.sidebar.multiselect('Add Fixed Income',
                                              ['TLT', 'JNK'],
                                              key='fixed_income')
st.sidebar.markdown("#### Commodities")
tickers_commodities = st.sidebar.multiselect('Add Commodities',
                                             ['GLD', 'USO', 'XAG'],
                                             key='commodities')
st.sidebar.markdown("#### Crypto")
tickers_crypto = st.sidebar.multiselect('Add Crypto',
                                        ['BTC-USD', 'ETH-USD', 'STX-USD'],
                                        key='crypto')

# Combine all tickers
tickers = tickers_equity + tickers_fixed_income + tickers_commodities + tickers_crypto

# Asset weights input
weights = st.sidebar.slider('Assign Weights (Sum = 100%)', min_value=0,
                            max_value=100, value=[50] * len(tickers), step=1)

# Date input
start_date = st.sidebar.date_input('Start Date',
                                   value=pd.to_datetime('2021-01-01'))
end_date = st.sidebar.date_input('End Date', value=pd.to_datetime('today'))

# Ensure tickers are selected
if len(tickers) > 0:
    # Fetch historical data
    data = fetch_yfinance_data(tickers, start_date, end_date)

    # Normalize weights
    weights = [w / 100 for w in weights]

    # Time filter selection
    st.title("Performance")
    time_filter = st.radio("Select Time Period",
                           ['1D', '1W', '1M', '6M', 'YTD', '1Y', 'Max'])

    # Filter data based on selected time filter
    filtered_data = filter_data_by_time_period(data['Adj Close'], time_filter)

    # Calculate portfolio cumulative returns based on filtered data
    cumulative_returns = calculate_cumulative_returns(filtered_data, weights)

    # Plot the cumulative returns chart
    st.pyplot(plot_cumulative_returns(cumulative_returns))

    # Calculate and display risk metrics
    risk_metrics = calculate_risk_metrics(filtered_data, weights)
    st.subheader('Results')
    st.write(pd.DataFrame(risk_metrics, index=[0]))
