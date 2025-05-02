import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend non-GUI untuk Flask/server
import matplotlib.pyplot as plt

from core.utils import fetch_ohlcv
from core.indicators import calculate_ema

# Folder untuk menyimpan mini chart
MINI_FOLDER = "static/mini"
os.makedirs(MINI_FOLDER, exist_ok=True)

def generate_mini_chart(symbol, interval='1m', limit=100):
    try:
        data = fetch_ohlcv(symbol, interval, limit)
        if not data or len(data) < 30:
            print(f"[Mini Chart] Data kurang untuk {symbol}")
            return None

        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["EMA_20"] = calculate_ema(df["close"], 20)

        # Plot
        plt.figure(figsize=(5, 2))
        plt.plot(df["timestamp"], df["close"], label="Close", linewidth=1.2, color="blue")
        plt.plot(df["timestamp"], df["EMA_20"], label="EMA 20", linestyle="--", linewidth=1, color="orange")
        plt.xticks([]); plt.yticks([])
        plt.legend(loc="upper left", fontsize=6)
        plt.tight_layout()

        filename = f"mini_chart_{symbol.replace('-', '').lower()}.png"
        full_path = os.path.join(MINI_FOLDER, filename)
        plt.savefig(full_path, dpi=100)
        plt.close()

        print(f"[Mini Chart] Disimpan: {full_path}")
        return full_path
    except Exception as e:
        print(f"[Mini Chart] Gagal generate untuk {symbol}: {e}")
        return None