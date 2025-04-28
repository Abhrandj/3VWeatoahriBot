import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for

from core.bot_instance import bot
from core.ai_predictor import predict_next_close_linear
from core.okx_trader import execute_trade
from core.telegram import send_telegram_message, send_telegram_photo

live_backtest_bp = Blueprint("live_backtest", __name__)

STATIC_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'static')
GRAPH_PATH = os.path.join(STATIC_FOLDER, "live_prediction_chart.png")

@live_backtest_bp.route("/", methods=["GET", "POST"])
def live_backtest():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    selected_pair = request.form.get("pair", "BTC-USDT")
    interval = request.form.get("interval", "1m")
    data = bot.engine.get_ohlcv(selected_pair, interval=interval, limit=100)

    prediction = None
    result = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_new_prediction = False

    if data is not None and len(data) >= 10:
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['datetime'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

        predicted = predict_next_close_linear(df)
        if predicted:
            last_price = round(df['close'].iloc[-1], 2)
            predicted = round(predicted, 2)
            signal = "BUY" if predicted > last_price else "SELL"
            entry = last_price
            sl = round(entry * 0.99, 2)
            tp = round(entry * 1.01, 2)

            current_pred = f"{predicted}_{signal}"
            if session.get("last_prediction") != current_pred:
                is_new_prediction = True
                session["last_prediction"] = current_pred

            prediction = {
                "last": last_price,
                "predicted": predicted,
                "signal": signal,
                "entry": entry,
                "sl": sl,
                "tp": tp,
                "is_new": is_new_prediction
            }

            # === Plot chart ===
            plt.figure(figsize=(10, 4))
            plt.plot(df['datetime'][-30:], df['close'][-30:], label="Actual Price", marker='o')
            plt.axhline(y=entry, color='gray', linestyle='--', label=f"Entry: {entry}")
            plt.axhline(y=predicted, color='orange', linestyle='--', label=f"Predicted: {predicted}")
            plt.axhline(y=sl, color='red', linestyle=':', label=f"SL: {sl}")
            plt.axhline(y=tp, color='green', linestyle=':', label=f"TP: {tp}")
            plt.xticks(rotation=45)
            plt.title(f"Live Prediction: {selected_pair} ({interval})")
            plt.xlabel("Datetime")
            plt.ylabel("Price")
            plt.legend()
            plt.tight_layout()
            plt.savefig(GRAPH_PATH)
            plt.close()

            if is_new_prediction:
                signal_msg = (
                    f"[Sinyal Baru Detected]\n"
                    f"Pair: {selected_pair}\n"
                    f"Time: {current_time}\n"
                    f"Signal: {signal}\n"
                    f"Entry: {entry}\n"
                    f"SL: {sl} | TP: {tp}"
                )
                send_telegram_message(signal_msg)
                send_telegram_photo(GRAPH_PATH, caption=signal_msg)

        result = df[['datetime', 'open', 'high', 'low', 'close', 'volume']].iloc[::-1].head(20).to_dict(orient='records')

    return render_template(
        "live_backtest.html",
        prediction=prediction,
        result=result,
        selected_pair=selected_pair,
        current_time=current_time
    )

@live_backtest_bp.route("/open_trade", methods=["POST"])
def open_trade():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    pair = request.form.get("pair")
    entry = request.form.get("entry")
    sl = request.form.get("sl")
    tp = request.form.get("tp")
    signal = request.form.get("signal")

    order = execute_trade(pair, signal, entry, sl, tp)

    msg = (
        f"Trade Executed:\n"
        f"Pair: {pair}\nDirection: {signal}\n"
        f"Entry: {entry}\nSL: {sl}\nTP: {tp}\nOrder ID: {order.get('ordId', '-')}"
    )
    send_telegram_message(msg)

    session["last_trade"] = f"{signal} {pair} @ {entry}"

    return render_template("trade_result.html", pair=pair, entry=entry, sl=sl, tp=tp, signal=signal)