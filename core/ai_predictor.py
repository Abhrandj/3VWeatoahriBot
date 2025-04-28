# core/ai_predictor.py

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from prophet import Prophet

def predict_next_close_linear(df):
    """
    Prediksi harga penutupan berikutnya + simpan grafik prediksi.
    :param df: DataFrame dengan kolom 'close'
    :return: Prediksi harga penutupan berikutnya (float)
    """
    if len(df) < 10 or 'close' not in df.columns:
        return None

    df = df.tail(50).copy()
    df["t"] = np.arange(len(df))
    X = df["t"].values.reshape(-1, 1)
    y = df["close"].values

    model = LinearRegression()
    model.fit(X, y)

    next_time = np.array([[len(df)]])
    predicted_close = model.predict(next_time)[0]

    # === Buat dan simpan grafik prediksi ===
    plt.figure(figsize=(10, 4))
    plt.plot(df["t"], y, label="Actual Close", marker='o')
    plt.plot(next_time[0][0], predicted_close, 'ro', label="Predicted", markersize=8)
    plt.title("Linear Regression Prediction")
    plt.xlabel("Time Step")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid(True)

    # Pastikan folder static/ ada
    output_path = os.path.join("flask_app", "static", "live_prediction_chart.png")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return predicted_close


def predict_next_close_prophet(df):
    """
    Prediksi harga penutupan berikutnya menggunakan Prophet.
    """
    if len(df) < 20 or 'close' not in df.columns or 'timestamp' not in df.columns:
        return None

    data = df[['timestamp', 'close']].copy()
    data.rename(columns={'timestamp': 'ds', 'close': 'y'}, inplace=True)
    data['ds'] = pd.to_datetime(data['ds'])

    model = Prophet(daily_seasonality=True)
    model.fit(data)

    future = model.make_future_dataframe(periods=1, freq='min')
    forecast = model.predict(future)
    next_pred = forecast['yhat'].iloc[-1]

    return next_pred