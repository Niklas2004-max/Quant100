import streamlit as st
from core.data import load_data, from_csv
from core.backtest import run_backtest
from core.plotting import plot_chart

st.set_page_config(page_title="Quant Tool", layout="wide")
st.title("Quant Tool - Backtesting & Analyse")

# --- Datenquelle auswählen ---
source = st.radio("Datenquelle auswählen", ("Yahoo Finance", "CSV-Datei"))

if source == "Yahoo Finance":
    ticker = st.text_input("Ticker eingeben (z.B. AAPL)", "AAPL")
    if st.button("Daten laden"):
        try:
            data = load_data(ticker)
            st.success(f"Daten für {ticker} geladen!")
            st.dataframe(data.tail(10))
        except Exception as e:
            st.error(f"Fehler beim Laden der Daten: {e}")

elif source == "CSV-Datei":
    uploaded_file = st.file_uploader("CSV hochladen", type=["csv"])
    if uploaded_file is not None:
        try:
            data = from_csv(uploaded_file)
            st.success("CSV-Daten geladen!")
            st.dataframe(data.head())
        except Exception as e:
            st.error(f"Fehler beim Laden der CSV: {e}")

# --- Backtest starten ---
if 'data' in locals():
    if st.button("Backtest starten"):
        try:
            results = run_backtest(data)
            st.subheader("Backtest Ergebnisse")
            st.write(results)

            st.subheader("Equity Curve")
            plot_chart(data)  # Dummy-Funktion, kannst du erweitern
        except Exception as e:
            st.error(f"Fehler beim Backtest: {e}")
