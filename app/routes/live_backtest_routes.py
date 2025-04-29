import os
import time
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, session
from core.live_backtest_engine import run_live_backtest
from core.utils import fetch_ohlcv  # Ambil data dari OKX langsung

live_backtest_bp = Blueprint("live_backtest", __name__)

@live_backtest_bp.route("/", methods=["GET", "POST"])
def live_backtest():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    result = None
    last_updated = None
    error = None
    selected_pair = "BTC-USDT"  # Default pair awal
    interval = "1m"  # Default interval

    if request.method == "POST":
        selected_pair = request.form.get("symbol", "BTC-USDT").upper()
        interval = request.form.get("interval", "1m")

        if not selected_pair:
            error = "Symbol harus diisi, contoh: BTC-USDT."
            return render_template("live_backtest.html", error=error)

        df = fetch_ohlcv(selected_pair, interval, limit=50)

        # Kalau gagal fetch, retry sekali
        if not df or len(df) < 20:
            time.sleep(0.5)
            df = fetch_ohlcv(selected_pair, interval, limit=50)

        if not df or len(df) < 20:
            error = "Data tidak tersedia atau gagal memuat OHLCV. Coba klik Run lagi."
        else:
            try:
                df = pd.DataFrame(df, columns=["timestamp", "open", "high", "low", "close", "volume"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                result = run_live_backtest(df)
                last_updated = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                error = str(e)

    return render_template(
        "live_backtest.html",
        result=result,
        last_updated=last_updated,
        selected_pair=selected_pair,
        interval=interval,
        error=error
    )