import matplotlib.pyplot as plt

def plot_price_signals(df):
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Adj Close'], label='Adj Close')
    if 'SMA_fast' in df.columns and 'SMA_slow' in df.columns:
        ax.plot(df.index, df['SMA_fast'], label='SMA fast')
        ax.plot(df.index, df['SMA_slow'], label='SMA slow')
    ax.legend()
    ax.set_title('Preis & Signale')
    return fig

def plot_equity(df):
    fig, ax = plt.subplots()
    ax.plot(df.index, df['equity'], label='Equity')
    ax.legend()
    ax.set_title('Equity Curve')
    return fig

def plot_drawdown(df):
    eq = df['equity']
    roll_max = eq.cummax()
    dd = eq/roll_max - 1.0
    fig, ax = plt.subplots()
    ax.plot(df.index, dd, label='Drawdown')
    ax.legend()
    ax.set_title('Drawdown')
    return fig
