# core/live_backtest_engine.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def run_live_backtest(df):
    """
    Fungsi live backtest:
    - Ambil 20 bar terakhir
    - Buat signal BUY/SELL
    - Buat chart harga Close
    - Return list dict: datetime, signal, price
    """
    if df.empty or 'close' not in df.columns:
        return None

    df = df.tail(20).copy()

    # === Buat Signal BUY/SELL ===
    result = []
    for i in range(1, len(df)):
        signal = "BUY" if df['close'].iloc[i] > df['close'].iloc[i-1] else "SELL"
        result.append({
            "datetime": df['timestamp'].iloc[i].strftime("%Y-%m-%d %H:%M"),
            "signal": signal,
            "price": round(df['close'].iloc[i], 2)
        })

    # === Buat Chart Harga Close ===
    output_path = os.path.join("app", "static", "live_prediction_chart.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['close'], marker='o', linestyle='-', label="Close Price")
    plt.title("Live Close Price")
    plt.xlabel("Datetime")
    plt.ylabel("Price")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return result