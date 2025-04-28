# core/graph_generator.py

import os
import pandas as pd
import plotly.graph_objects as go
from core.utils import fetch_ohlcv
from core.indicators import calculate_ema, calculate_bb, calculate_rsi
from core.ai_predictor import predict_next_close_linear, predict_next_close_prophet

GRAPH_FOLDER = "flask_app/static/graphs"
os.makedirs(GRAPH_FOLDER, exist_ok=True)

def generate_pair_chart(symbol, interval='1m', limit=100):
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
    path = os.path.join(GRAPH_FOLDER, filename)
    fig.write_html(path)
    return filename