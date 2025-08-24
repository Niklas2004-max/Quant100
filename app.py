import streamlit as st
from core.data import load_data
from core.backtest import run_backtest
from core.plotting import plot_chart  # optional, muss in core/ existieren

st.set_page_config(page_title="Quant Tool", layout="wide")
st.title("Quant Tool - Backtesting & Analyse")

# --- Datenquelle ---
ticker = st.text_input("Ticker eingeben (z.B. AAPL)", "AAPL")

if st.button("Daten laden"):
    try:
        data = load_data(ticker)
        st.success(f"Daten für {ticker} geladen!")
        st.dataframe(data.tail(10))
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {e}")

# --- Backtest starten ---
if 'data' in locals():
    if st.button("Backtest starten"):
        try:
            results = run_backtest(data)
            st.subheader("Backtest Ergebnisse")
            st.write(results)

            # Optional: Equity Curve plotten, falls plot_chart existiert
            if 'plot_chart' in globals():
                plot_chart(data)
        except Exception as e:
            st.error(f"Fehler beim Backtest: {e}")
