# app/routes/live_backtest_routes.py

import os
import pandas as pd
from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for
import plotly.graph_objs as go

from core.bot_instance import bot
from core.ai_predictor import predict_next_close_linear
from core.okx_trader import execute_trade
from core.telegram import send_telegram_message, send_telegram_photo
from core.graph_generator import generate_mini_chart  # untuk mini chart image

live_backtest_bp = Blueprint("live_backtest", __name__)

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
    plot_html = None

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

            # === Generate Interaktif Chart ===
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['datetime'], y=df['close'], mode='lines+markers', name='Actual Price'))
            fig.add_hline(y=entry, line_dash='dash', line_color='gray',
                          annotation_text=f"Entry: {entry}", annotation_position="top left")
            fig.add_hline(y=predicted, line_dash='dash', line_color='orange',
                          annotation_text=f"Predicted: {predicted}", annotation_position="top left")
            fig.add_hline(y=sl, line_dash='dot', line_color='red',
                          annotation_text=f"SL: {sl}", annotation_position="bottom left")
            fig.add_hline(y=tp, line_dash='dot', line_color='green',
                          annotation_text=f"TP: {tp}", annotation_position="bottom left")
            fig.update_layout(
                title=f"Live Prediction: {selected_pair}",
                xaxis_title="Datetime",
                yaxis_title="Price",
                template="plotly_white",
                height=400
            )
            plot_html = fig.to_html(full_html=False)

            # === Kirim Telegram jika Prediksi Baru ===
            if is_new_prediction:
                text = (
                    f"[Sinyal Baru]\n"
                    f"Pair: {selected_pair}\n"
                    f"Time: {current_time}\n"
                    f"Signal: {signal}\n"
                    f"Entry: {entry}\n"
                    f"SL: {sl} | TP: {tp}"
                )
                chart_path = generate_mini_chart(selected_pair)
                if chart_path and os.path.exists(chart_path):
                    send_telegram_photo(chart_path, caption=text)
                else:
                    send_telegram_message(text)

                # === Auto Trade jika aktif ===
                if session.get("auto_trade"):
                    execute_trade(selected_pair, signal, entry, sl, tp)
                    send_telegram_message(f"[AUTO TRADE] {selected_pair} | {signal} @ {entry}")

        # === Tabel data terakhir ===
        result = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]\
                    .iloc[::-1].head(20).to_dict(orient='records')

    return render_template(
        "live_backtest.html",
        prediction=prediction,
        result=result,
        selected_pair=selected_pair,
        current_time=current_time,
        plot_html=plot_html
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