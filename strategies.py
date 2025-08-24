import pandas as pd
from .utils import rsi

def sma_crossover(df: pd.DataFrame, fast=20, slow=50):
    df = df.copy()
    df['SMA_fast'] = df['Adj Close'].rolling(fast).mean()
    df['SMA_slow'] = df['Adj Close'].rolling(slow).mean()
    df['signal'] = 0
    df.loc[df['SMA_fast'] > df['SMA_slow'], 'signal'] = 1
    df['position'] = df['signal'].shift(1).fillna(0)
    return df

def rsi_mean_reversion(df: pd.DataFrame, period=14, oversold=30, overbought=70):
    df = df.copy()
    df['RSI'] = rsi(df['Adj Close'], period=period)
    df['signal'] = 0
    df.loc[df['RSI'] < oversold, 'signal'] = 1
    df.loc[df['RSI'] > overbought, 'signal'] = 0
    df['position'] = df['signal'].shift(1).fillna(0)
    return df
