import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory

from core.bot_instance import bot
from core.utils import generate_roi_chart, is_live_mode
from core.graph_generator import generate_pair_chart
from core.report_generator import generate_daily_report
from core.paths import GRAPHS_FOLDER

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    signal = bot.run(notify=False)
    pair_list = bot.engine.symbols

    # Tambah Pair baru
    if request.method == "POST":
        new_pair = request.form.get("pair")
        if new_pair and new_pair not in pair_list:
            pair_list.append(new_pair)

    # Generate chart per pair
    for pair in pair_list:
        generate_pair_chart(pair)

    # Hitung ROI aktif
    positions = bot.portfolio.get_all()
    total_roi, roi_count = 0, 0
    for sym, pos in positions.items():
        price_now = bot.engine.last_price.get(sym, 0)
        if pos["entry"] > 0:
            roi = ((price_now - pos["entry"]) / pos["entry"] * 100
                   if pos["side"] == "BUY"
                   else (pos["entry"] - price_now) / pos["entry"] * 100)
            total_roi += roi
            roi_count += 1
    avg_roi = round(total_roi / roi_count, 2) if roi_count else 0

    # ROI Chart historis
    generate_roi_chart(bot.portfolio.get_closed())

    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot_mode = session.get("bot_mode_override", "LIVE" if is_live_mode() else "TEST")

    return render_template(
        "dashboard.html",
        signal=signal,
        pair_list=pair_list,
        bot=bot,
        avg_roi=avg_roi,
        last_updated=last_updated,
        bot_mode=bot_mode
    )

@dashboard_bp.route("/start-bot", methods=["POST"])
def start_bot():
    result = bot.run(notify=True)
    flash("Bot dijalankan secara manual!", "success")
    return redirect(url_for("dashboard.dashboard"))

@dashboard_bp.route("/send_daily_report", methods=["POST"])
def send_daily_report():
    result = generate_daily_report(bot.portfolio)
    flash(result)
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route("/toggle_auto_trade", methods=["POST"])
def toggle_auto_trade():
    session["auto_trade"] = request.form.get("auto_trade") == "1"
    flash(f"Auto Trade {'Aktif' if session['auto_trade'] else 'Nonaktif'}", "info")
    return redirect(url_for("dashboard.dashboard"))

@dashboard_bp.route("/toggle_mode", methods=["POST"])
def toggle_bot_mode():
    new_mode = request.form.get("mode", "TEST").upper()
    session["bot_mode_override"] = new_mode
    flash(f"Bot mode changed to {new_mode}", "info")
    return redirect(url_for("dashboard.dashboard"))

@dashboard_bp.route("/graphs/<path:filename>")
def graph_file(filename):
    return send_from_directory(GRAPHS_FOLDER, filename)