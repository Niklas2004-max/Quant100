import numpy as np
import pandas as pd
from .utils import drawdown, annualize_return, annualize_vol

def sharpe(returns, rf=0.0, periods_per_year=252):
    ex = returns - rf/periods_per_year
    vol = annualize_vol(ex, periods_per_year)
    if vol == 0:
        return 0.0
    return (annualize_return(ex, periods_per_year)) / vol

def sortino(returns, rf=0.0, periods_per_year=252):
    ex = returns - rf/periods_per_year
    neg = ex[ex<0]
    dd = neg.std(ddof=0) * (periods_per_year**0.5)
    if dd == 0:
        return 0.0
    return (annualize_return(ex, periods_per_year)) / dd

def max_drawdown(equity):
    dd = drawdown(equity)
    return dd.min()

def calmar(returns):
    eq = (1+returns).cumprod()
    mdd = abs(max_drawdown(eq))
    if mdd == 0:
        return 0.0
    return (eq.iloc[-1]**(252/len(eq)) - 1) / mdd

def summarize(trades_df, returns, equity):
    wins = trades_df[trades_df['PnL']>0]
    losses = trades_df[trades_df['PnL']<=0]
    total = len(trades_df)
    win_rate = len(wins)/total if total>0 else 0.0
    profit_factor = wins['PnL'].sum() / abs(losses['PnL'].sum()) if len(losses)>0 else np.inf
    return {
        "CAGR": (equity.iloc[-1]**(252/len(equity)) - 1) if len(equity)>1 else 0.0,
        "Sharpe": sharpe(returns),
        "Sortino": sortino(returns),
        "Volatilität": returns.std()*np.sqrt(252),
        "Max Drawdown": max_drawdown(equity),
        "Calmar": calmar(returns),
        "Trades": total,
        "Win Rate": win_rate,
        "Profit Faktor": profit_factor
    }
