import os
from flask import Blueprint, render_template, send_from_directory, flash, redirect, url_for, request, session

from core.bot_instance import bot
from core.graph_generator import generate_pair_chart
from core.utils import generate_roi_chart
from core.report_generator import generate_daily_report
from core.paths import GRAPHS_FOLDER  # <<== Pakai paths

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    pair_list = ["BTC-USDT", "ETH-USDT", "SOL-USDT"]

    if request.method == "POST":
        pair = request.form.get("pair")
        if pair and pair not in pair_list:
            pair_list.append(pair)
            if pair not in bot.engine.symbols:
                bot.engine.symbols.append(pair)

    signal = bot.run()

    for pair in pair_list:
        generate_pair_chart(pair)

    positions = bot.portfolio.get_all()
    total_roi, roi_count = 0, 0
    for sym, pos in positions.items():
        price_now = bot.engine.last_price.get(sym, 0)
        if pos["entry"] > 0:
            roi = (price_now - pos["entry"]) / pos["entry"] * 100 if pos["side"] == "BUY" else (pos["entry"] - price_now) / pos["entry"] * 100
            total_roi += roi
            roi_count += 1

    avg_roi = round(total_roi / roi_count, 2) if roi_count else 0
    generate_roi_chart(bot.portfolio.get_closed())

    return render_template('dashboard.html', signal=signal, pair_list=pair_list, bot=bot, avg_roi=avg_roi)

@dashboard_bp.route("/graphs/<path:filename>")
def graph_file(filename):
    return send_from_directory(GRAPHS_FOLDER, filename)

@dashboard_bp.route("/send_daily_report", methods=["POST"])
def send_daily_report():
    result = generate_daily_report()
    flash(result)
    return redirect(url_for('dashboard_bp.dashboard'))