# Minimal Quant Tool (Streamlit)

Ein schlankes, modulares Quant-Tool zum Laden von Marktdaten, Backtesting einfacher Strategien und Reporting von Kennzahlen.

## Features
- Datenquelle: Yahoo Finance (`yfinance`) **oder** CSV-Upload (Spalten: `Date, Open, High, Low, Close, Adj Close, Volume`).
- Strategien: 
  - *SMA Crossover* (fast/slow)
  - *RSI Mean Reversion* (Period, Overbought/Oversold)
- Backtesting (long-only oder long/flat), feste Positionsgröße, Slippage/Fees optional.
- Kennzahlen: CAGR, Sharpe, Sortino, Max Drawdown, Calmar, Volatilität, Trefferquote, Profitfaktor.
- Plots: Kurs + Signale, Equity Curve, Drawdown.
- Export: Trades als CSV.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Start
```bash
streamlit run app.py
```

## Hinweise
- Für iPad: in einer Cloud/Notebook-Umgebung starten (z.B. Codespaces/Colab) oder lokal auf einem Rechner.
- Ohne Internet kannst du CSV-Dateien hochladen.
