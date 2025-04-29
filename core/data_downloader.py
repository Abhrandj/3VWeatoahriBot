# core/data_downloader.py

import os
import time
import requests
import pandas as pd

# Untuk BACKTEST upload (save ke CSV)
def fetch_and_save(symbol: str, bar: str, total: int) -> str:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    limit = 1000
    after = None
    all_data = []
    loops = max(1, total // limit)

    for _ in range(loops):
        params = {"instId": symbol, "bar": bar, "limit": limit}
        if after:
            params["after"] = after
        resp = requests.get("https://www.okx.com/api/v5/market/history-candles", params=params)
        data = resp.json().get("data", [])
        if not data:
            break
        all_data.extend(data)
        after = data[-1][0]
        time.sleep(0.3)

    df = pd.DataFrame(all_data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "volCcy", "volCcyQuote", "confirm"
    ])
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df = df.iloc[::-1]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    filename = f"{symbol.replace('-', '_').lower()}_{bar.lower()}.csv"
    path = os.path.join(UPLOAD_FOLDER, filename)
    df.to_csv(path, index=False)
    return filename

# Untuk LIVE BACKTEST realtime (langsung return data)
def fetch_ohlcv(symbol: str, interval: str = "1m", limit: int = 100):
    try:
        params = {
            "instId": symbol,
            "bar": interval,
            "limit": limit
        }
        resp = requests.get("https://www.okx.com/api/v5/market/history-candles", params=params)
        data = resp.json().get("data", [])

        if not data:
            return None

        ohlcv = []
        for row in reversed(data):
            ohlcv.append({
                "datetime": int(row[0]),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5])
            })

        return ohlcv

    except Exception as e:
        print(f"[fetch_ohlcv] Gagal ambil data: {e}")
        return None