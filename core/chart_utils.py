import os
import pandas as pd
import matplotlib.pyplot as plt
from core.utils import fetch_ohlcv

def generate_mini_chart(symbol, save_path="static/mini"):
    try:
        os.makedirs(save_path, exist_ok=True)

        data = fetch_ohlcv(symbol, interval='1m', limit=30)
        if not data or len(data) < 10:
            print(f"[Mini Chart] Tidak cukup data untuk {symbol}")
            return None

        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        fig, ax = plt.subplots(figsize=(4, 2))
        ax.plot(df["timestamp"], df["close"], label="Price", color="blue", linewidth=1.5)
        ax.set_title(symbol, fontsize=10)
        ax.tick_params(axis='x', labelrotation=45, labelsize=6)
        ax.tick_params(axis='y', labelsize=6)
        plt.tight_layout()

        filename = f"{symbol.replace('-', '').lower()}_mini.png"
        full_path = os.path.join(save_path, filename)
        plt.savefig(full_path, dpi=100)
        plt.close()

        print(f"[Mini Chart] Disimpan: {full_path}")
        return full_path
    except Exception as e:
        print(f"[Mini Chart] Gagal membuat chart untuk {symbol}: {e}")
        return None