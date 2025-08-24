import pandas as pd
import yfinance as yf
from .utils import to_datetime_index, ensure_ohlcv

def load_yf(ticker, start=None, end=None, interval='1d'):
    df = yf.download(ticker, start=start, end=end, interval=interval, auto_adjust=False, progress=False)
    df = df.rename(columns={'Adj Close':'Adj Close'})
    df = to_datetime_index(df)
    return ensure_ohlcv(df)

def from_csv(file):
    df = pd.read_csv(file)
    df = to_datetime_index(df, 'Date')
    return ensure_ohlcv(df)
