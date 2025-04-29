import os
import csv
import matplotlib.pyplot as plt
from core.okx_sdk import OKXClient as CustomOKX

# === 1. Fetch OHLCV dari OKX ===
def fetch_ohlcv(symbol, interval='1m', limit=100):
    """
    Mengambil data OHLCV dari OKX (tanpa autentikasi).
    :param symbol: contoh 'BTC-USDT'
    :param interval: timeframe, contoh '1m'
    :param limit: jumlah data terakhir yang ingin diambil
    :return: list [timestamp, open, high, low, close, volume]
    """
    okx = CustomOKX()
    try:
        candles = okx.get_kline(symbol=symbol, interval=interval, limit=limit)
        if isinstance(candles, dict) and 'data' in candles and isinstance(candles['data'], list):
            return [
                [
                    int(row[0]),     # timestamp (ms)
                    float(row[1]),   # open
                    float(row[2]),   # high
                    float(row[3]),   # low
                    float(row[4]),   # close
                    float(row[5])    # volume
                ]
                for row in candles['data']
            ][::-1]  # dibalik agar ASC (lama ke baru)
        else:
            print(f"[fetch_ohlcv] Format respons tidak sesuai: {candles}")
            return None
    except Exception as e:
        print(f"[fetch_ohlcv] Gagal ambil data {symbol}: {e}")
        return None

# === 2. Generate Cumulative ROI Chart ===
def generate_roi_chart(closed_positions, save_path="app/static/graphs/cumulative_roi.png"):
    """
    Membuat grafik kumulatif ROI dari posisi tertutup.
    :param closed_positions: list posisi closed dari portfolio
    :param save_path: path penyimpanan grafik PNG
    """
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
    """
    Simpan data dict ke file CSV.
    :param filepath: path ke file CSV
    :param data: dict atau list of dict
    """
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