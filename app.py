import streamlit as st
import pandas as pd
import numpy as np
from core.data import load_yf, from_csv
from core.strategies import sma_crossover, rsi_mean_reversion
from core.backtest import backtest
from core.metrics import summarize
from core.plotting import plot_price_signals, plot_equity, plot_drawdown

st.set_page_config(page_title="Quant Tool", layout="wide")

st.title("🧠 Minimal Quant Tool")

with st.sidebar:
    st.header("Daten")
    mode = st.radio("Quelle", ["Yahoo Finance", "CSV Upload"])
    if mode == "Yahoo Finance":
        ticker = st.text_input("Ticker", value="SPY")
        start = st.date_input("Start", value=pd.to_datetime("2015-01-01"))
        end = st.date_input("Ende", value=pd.Timestamp.today().date())
        interval = st.selectbox("Intervall", ["1d","1wk","1mo"])
    else:
        file = st.file_uploader("CSV hochladen", type=["csv"])

    st.header("Strategie")
    strat_name = st.selectbox("Typ", ["SMA Crossover","RSI Mean Reversion"])
    if strat_name == "SMA Crossover":
        fast = st.number_input("SMA fast", min_value=1, value=20)
        slow = st.number_input("SMA slow", min_value=2, value=50)
    else:
        period = st.number_input("RSI Period", min_value=2, value=14)
        oversold = st.number_input("Oversold <", min_value=1, max_value=99, value=30)
        overbought = st.number_input("Overbought >", min_value=1, max_value=99, value=70)

    st.header("Kosten & Risiko")
    fee_bps = st.number_input("Gebühren (bps)", min_value=0.0, value=1.0)
    slippage_bps = st.number_input("Slippage (bps)", min_value=0.0, value=0.0)

    run = st.button("Run Backtest")

def load_data():
    if mode == "Yahoo Finance":
        return load_yf(ticker, start=start, end=end, interval=interval)
    else:
        if file is None:
            st.stop()
        return from_csv(file)

if run:
    with st.spinner("Lade Daten & starte Backtest..."):
        df = load_data()
        if strat_name == "SMA Crossover":
            sig = sma_crossover(df, fast=int(fast), slow=int(slow))
        else:
            sig = rsi_mean_reversion(df, period=int(period), oversold=int(oversold), overbought=int(overbought))
        bt = backtest(sig, fee_bps=float(fee_bps), slippage_bps=float(slippage_bps))
        st.success("Fertig.")

        # Kennzahlen
        stats = summarize(
            trades_df=pd.DataFrame(),  # einfache Engine: Trades werden nicht einzeln geloggt
            returns=bt['returns'],
            equity=bt['equity']
        )
        st.subheader("Kennzahlen")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("CAGR", f"{stats['CAGR']:.2%}")
        c2.metric("Sharpe", f"{stats['Sharpe']:.2f}")
        c3.metric("Max DD", f"{stats['Max Drawdown']:.2%}")
        c4.metric("Volatilität", f"{stats['Volatilität']:.2%}")

        # Plots
        st.subheader("Charts")
        st.pyplot(plot_price_signals(sig))
        st.pyplot(plot_equity(bt))
        st.pyplot(plot_drawdown(bt))

        # Daten anzeigen
        st.subheader("Daten")
        st.dataframe(bt.tail(500))
