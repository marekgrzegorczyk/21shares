import yfinance as yf


def fetch_yfinance_data(tickers_list, start_date, end_date):
    return yf.download(tickers_list, start=start_date, end=end_date)
