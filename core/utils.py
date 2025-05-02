# core/utils.py

import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from core.okx_sdk import OKXClient as CustomOKX

# === 0. Cek Mode Bot ===
def is_live_mode():
    return os.getenv("BOT_MODE", "TEST").upper() == "LIVE"

# === 1. Fetch OHLCV dari file lokal atau OKX ===
def fetch_ohlcv(symbol, interval='1m', limit=100):
    """
    Ambil data OHLCV dari CSV lokal jika ada, jika tidak dari OKX API.
    """
    local_csv = f"tests/data/{symbol.replace('-', '')}.csv"
    if os.path.exists(local_csv):
        try:
            df = pd.read_csv(local_csv)
            df = df.tail(limit)
            return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']].values.tolist()
        except Exception as e:
            print(f"[fetch_ohlcv] Gagal baca CSV lokal {local_csv}: {e}")
            return None

    okx = CustomOKX()
    try:
        candles = okx.get_kline(symbol=symbol, interval=interval, limit=limit)
        if isinstance(candles, dict) and 'data' in candles and isinstance(candles['data'], list):
            return [
                [
                    int(row[0]),
                    float(row[1]),
                    float(row[2]),
                    float(row[3]),
                    float(row[4]),
                    float(row[5])
                ]
                for row in candles['data']
            ][::-1]
        else:
            print(f"[fetch_ohlcv] Format respons tidak sesuai: {candles}")
            return None
    except Exception as e:
        print(f"[fetch_ohlcv] Gagal ambil data {symbol}: {e}")
        return None

# === 2. Generate Cumulative ROI Chart ===
def generate_roi_chart(closed_positions, save_path="app/static/graphs/cumulative_roi.png"):
    try:
        if not closed_positions:
            print("[ROI Chart] Tidak ada data posisi tertutup.")
            return

        roi_values = [pos.get("roi", 0) for pos in closed_positions]
        cum_roi = [sum(roi_values[:i+1]) for i in range(len(roi_values))]

        plt.figure(figsize=(8, 3))
        plt.plot(cum_roi, marker='o', linestyle='-', linewidth=1.5)
        plt.title("Cumulative ROI")
        plt.xlabel("Trade #")
        plt.ylabel("ROI (%)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
    except Exception as e:
        print(f"[ROI Chart] Gagal membuat chart ROI: {e}")

# === 3. Save data to CSV ===
def save_to_csv(filepath, data):
    if not data:
        return

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    keys = data[0].keys() if isinstance(data, list) else data.keys()
    with open(filepath, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        if isinstance(data, list):
            writer.writerows(data)
        else:
            writer.writerow(data)