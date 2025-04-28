import requests
import pandas as pd
import time

# === Fungsi Ambil Data dari OKX ===
def fetch_candles(symbol, bar, after=None, limit=1000):
    url = "https://www.okx.com/api/v5/market/history-candles"
    params = {
        'instId': symbol,
        'bar': bar,
        'limit': limit
    }
    if after:
        params['after'] = after

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print("Gagal ambil data:", response.status_code)
        return []

# === Main Downloader ===
def download_okx_data(symbol, bar, total_candles):
    max_candles = 1000
    loops = total_candles // max_candles
    after = None
    all_data = []

    for i in range(loops):
        print(f"[{i+1}/{loops}] Mengambil data untuk {symbol} ({bar})...")
        data = fetch_candles(symbol, bar, after, max_candles)
        if not data:
            break
        all_data.extend(data)
        after = data[-1][0]
        time.sleep(0.5)

    print(f"Total candlestick didapat: {len(all_data)}")

    # Format dan Simpan ke CSV
    df = pd.DataFrame(all_data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'volCcy', 'volCcyQuote', 'confirm'
    ])
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    df = df[::-1]  # Urutkan dari lama ke baru
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    filename = f"{symbol.replace('-', '_').lower()}_{bar.lower()}.csv"
    df.to_csv(filename, index=False)
    print(f"Sukses simpan ke file: {filename}")

# === Input Manual dari Terminal ===
if __name__ == '__main__':
    print("=== OKX Historical Data Downloader ===")
    symbol = input("Pair (contoh: BTC-USDT): ").strip().upper()
    bar = input("Interval (1m, 5m, 15m, 1H, 4H, 1D): ").strip()
    total = int(input("Total data candlestick (kelipatan 1000): "))

    download_okx_data(symbol, bar, total)