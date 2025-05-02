# core/indicators.py

import numpy as np
import pandas as pd

def calculate_ema(prices, period=10):
    return pd.Series(prices).ewm(span=period, adjust=False).mean().values

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_bb(prices, period=20):
    ma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper = ma + 2 * std
    lower = ma - 2 * std
    return upper, lower

def calculate_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    macd = ema_fast - ema_slow
    signal_line = pd.Series(macd).ewm(span=signal, adjust=False).mean()
    hist = macd - signal_line
    return macd, signal_line, hist

def calculate_indicators(df):
    df['ema_20'] = calculate_ema(df['close'], 20)
    df['ema_50'] = calculate_ema(df['close'], 50)
    df['ema200'] = calculate_ema(df['close'], 200)

    # Alias untuk strategi yang pakai format berbeda
    df['ema20'] = df['ema_20']
    df['ema50'] = df['ema_50']
    df['ma_200'] = df['ema200']

    df['rsi'] = calculate_rsi(df['close'], 14)

    upper, lower = calculate_bb(df['close'], 20)
    df['upper_band'] = upper
    df['lower_band'] = lower
    df['upper_bb'] = upper
    df['lower_bb'] = lower

    macd, signal, hist = calculate_macd(df['close'])
    df['macd'] = macd
    df['macd_signal'] = signal
    df['macd_histogram'] = hist
    df['macd_hist'] = hist

    return df