import yfinance as yf
import pandas as pd


def get_stock_data(ticker, period="1y"):
    """
    Download historical stock market data from Yahoo Finance.
    """

    data = yf.download(
        ticker,
        period=period,
        auto_adjust=False,
        progress=False
    )

    if data.empty:
        return data

    # Convert Yahoo Finance MultiIndex columns
    # into normal single-level columns.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Remove duplicate columns if any exist
    data = data.loc[:, ~data.columns.duplicated()]

    return data