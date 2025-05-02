# core/graph_generator.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from core.utils import fetch_ohlcv
from core.indicators import calculate_ema, calculate_bb, calculate_rsi
from core.ai_predictor import predict_next_close_linear, predict_next_close_prophet
from core.bot_instance import bot
from core.paths import GRAPHS_FOLDER

# Folder untuk menyimpan grafik
os.makedirs(GRAPHS_FOLDER, exist_ok=True)

def generate_pair_chart(symbol, interval='1m', limit=100):
    """
    Generate chart HTML interaktif + prediksi AI.
    """
    data = fetch_ohlcv(symbol, interval, limit)
    if not data or len(data) < 30:
        return None

    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    df["EMA_20"] = calculate_ema(df["close"], 20)
    df["BB_upper"], df["BB_lower"] = calculate_bb(df["close"], 20)
    df["RSI"] = calculate_rsi(df["close"], 14)

    linear_pred = predict_next_close_linear(df)
    prophet_pred = predict_next_close_prophet(df)
    future_time = df["timestamp"].iloc[-1] + pd.Timedelta(minutes=1)

    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df["timestamp"],
        open=df["open"], high=df["high"], low=df["low"], close=df["close"],
        name="Candlestick"
    ))

    # Indikator
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["EMA_20"], mode="lines", name="EMA 20"))
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["BB_upper"], mode="lines", name="Upper BB", line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["BB_lower"], mode="lines", name="Lower BB", line=dict(dash='dot')))

    # AI Predictions
    if linear_pred:
        fig.add_trace(go.Scatter(
            x=[df["timestamp"].iloc[-1], future_time],
            y=[df["close"].iloc[-1], linear_pred],
            mode="lines+markers",
            name="Linear Prediction",
            line=dict(dash="dot", color="orange")
        ))
    if prophet_pred:
        fig.add_trace(go.Scatter(
            x=[df["timestamp"].iloc[-1], future_time],
            y=[df["close"].iloc[-1], prophet_pred],
            mode="lines+markers",
            name="Prophet Prediction",
            line=dict(dash="dash", color="green")
        ))

    fig.update_layout(
        title=f"Chart + AI Prediction for {symbol}",
        xaxis_title="Time",
        yaxis_title="Price",
        template="plotly_white"
    )

    filename = f"chart_{symbol.replace('-', '').lower()}.html"
    path = os.path.join(GRAPHS_FOLDER, filename)
    fig.write_html(path)
    return filename


def generate_mini_chart(symbol):
    """
    Generate mini chart PNG untuk dikirim via Telegram.
    """
    df = bot.engine.get_data(symbol)
    if df is None or len(df) < 10:
        return None

    df = df.tail(30)
    plt.figure(figsize=(6, 2))
    plt.plot(df['close'], marker='o', linestyle='-', linewidth=1.2)
    plt.title(f"{symbol} - Mini Chart")
    plt.tight_layout()

    os.makedirs(GRAPHS_FOLDER, exist_ok=True)
    filepath = os.path.join(GRAPHS_FOLDER, f"mini_{symbol.replace('-', '').lower()}.png")
    plt.savefig(filepath)
    plt.close()

    return filepath