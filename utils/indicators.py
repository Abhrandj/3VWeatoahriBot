import pandas as pd
import numpy as np
import time

# ====== FUNGSI INDIKATOR ======
def calculate_ema(prices, period=10):
    return pd.Series(prices).ewm(span=period, adjust=False).mean().values

def calculate_rsi(prices, period=14):
    prices = pd.Series(prices)
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.values

def calculate_bb(prices, period=20):
    prices = pd.Series(prices)
    ma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper = ma + 2 * std
    lower = ma - 2 * std
    return upper.values, lower.values

def calculate_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    macd = ema_fast - ema_slow
    signal_line = calculate_ema(macd, signal)
    histogram = macd - signal_line
    return macd, signal_line, histogram

# ====== ENGINE BACKTEST ======
def apply_indicators(df):
    df['EMA_20'] = calculate_ema(df['close'], 20)
    df['RSI_14'] = calculate_rsi(df['close'], 14)
    df['BB_upper'], df['BB_lower'] = calculate_bb(df['close'], 20)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = calculate_macd(df['close'])
    return df

def run_backtest(csv_path):
    start_time = time.time()

    # Load CSV data
    df = pd.read_csv(csv_path)

    # Apply indicators to the dataframe
    df = apply_indicators(df)

    initial_balance = 1000
    balance = initial_balance
    position = None
    entry_price = 0
    trade_log = []

    for i in range(1, len(df)):
        price = df['close'][i]
        rsi = df['RSI_14'][i]
        ema = df['EMA_20'][i]
        macd = df['MACD'][i]
        macd_signal = df['MACD_signal'][i]

        if np.isnan(rsi) or np.isnan(ema) or np.isnan(macd) or np.isnan(macd_signal):
            continue  # skip if any indicator is NaN

        if position is None:
            if rsi < 30 and price > ema:
                position = 'long'
                entry_price = price
                trade_log.append(f"Buy at {price}")
        elif position == 'long':
            if rsi > 70 or price < ema or macd < macd_signal:
                pnl = (price - entry_price)
                balance += pnl
                trade_log.append(f"Sell at {price} | PnL: {pnl:.2f}")
                position = None

    final_pnl = balance - initial_balance
    end_time = time.time()
    duration = end_time - start_time

    return {
        "initial_balance": initial_balance,
        "final_balance": round(balance, 2),
        "profit": round(final_pnl, 2),
        "trades": trade_log,
        "duration": round(duration, 2)
    }