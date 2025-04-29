import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def run_live_backtest(df):
    """
    Fungsi live backtest:
    - Ambil 20 bar terakhir
    - Buat signal BUY/SELL berdasarkan perubahan close
    - Buat chart harga Close
    - Return list of dict: datetime, open, high, low, close, volume
    """
    if df.empty or 'close' not in df.columns:
        return None

    df = df.tail(20).copy()

    # === Persiapan Data Tabel ===
    result = []
    for i in range(len(df)):
        result.append({
            "datetime": df['timestamp'].iloc[i].strftime("%Y-%m-%d %H:%M"),
            "open": round(df['open'].iloc[i], 2),
            "high": round(df['high'].iloc[i], 2),
            "low": round(df['low'].iloc[i], 2),
            "close": round(df['close'].iloc[i], 2),
            "volume": round(df['volume'].iloc[i], 2),
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