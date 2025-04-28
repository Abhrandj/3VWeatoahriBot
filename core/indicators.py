import numpy as np
import pandas as pd

# ====== INDIKATOR UNTUK REAL-TIME TRADING ======

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

def calculate_indicators(df):
    df['ema_20'] = calculate_ema(df['close'], 20)
    df['ema_50'] = calculate_ema(df['close'], 50)
    df['ma_200'] = df['close'].rolling(window=200).mean()
    df['rsi'] = calculate_rsi(df['close'], 14)
    df['upper_bb'], df['lower_bb'] = calculate_bb(df['close'], 20)
    df['macd'], df['macd_signal'], df['macd_hist'] = calculate_macd(df['close'])
    return df