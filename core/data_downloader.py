import os
import time
import requests
import pandas as pd

def fetch_and_save(symbol: str, bar: str, total: int) -> str:
    """
    Download OHLCV dari OKX dan simpan sebagai CSV di flask_app/uploads/.
    Returns nama file yang disimpan.
    """
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'flask_app', 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    limit = 1000
    after = None
    all_data = []
    loops = max(1, total // limit)

    for _ in range(loops):
        params = {"instId": symbol, "bar": bar, "limit": limit}
        if after:
            params["after"] = after
        resp = requests.get(
            "https://www.okx.com/api/v5/market/history-candles", params=params
        )
        data = resp.json().get("data", [])
        if not data:
            break
        all_data.extend(data)
        after = data[-1][0]
        time.sleep(0.3)

    df = pd.DataFrame(all_data, columns=[
        "timestamp","open","high","low","close","volume",
        "volCcy","volCcyQuote","confirm"
    ])
    df = df[["timestamp","open","high","low","close","volume"]]
    df = df.iloc[::-1]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    filename = f"{symbol.replace('-', '_').lower()}_{bar.lower()}.csv"
    path = os.path.join(UPLOAD_FOLDER, filename)
    df.to_csv(path, index=False)
    return filename