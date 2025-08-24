import pandas as pd
import numpy as np

def backtest(price_df: pd.DataFrame, position_col='position', fee_bps=1.0, slippage_bps=0.0):
    df = price_df.copy()
    if 'Adj Close' not in df.columns:
        raise ValueError("Adj Close Spalte fehlt")
    price = df['Adj Close']
    ret = price.pct_change().fillna(0)
    pos = df[position_col].fillna(0).clip(0,1)
    # round-trip costs when position changes
    trade_chg = pos.diff().abs().fillna(pos.abs())
    fees = trade_chg * (fee_bps/10000.0)
    slip = trade_chg * (slippage_bps/10000.0)
    strat_ret = pos * ret - fees - slip
    equity = (1 + strat_ret).cumprod()
    df['returns'] = strat_ret
    df['equity'] = equity
    return df
