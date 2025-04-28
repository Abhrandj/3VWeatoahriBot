import os
from flask import Blueprint, render_template, send_from_directory, send_file, redirect, url_for, session

from core.bot_instance import bot
from core.utils import generate_roi_chart
from core.paths import PORTFOLIO_FOLDER  # <<== Pakai paths

portfolio_bp = Blueprint("portfolio_bp", __name__)

@portfolio_bp.route("/", methods=["GET"])
def portfolio():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    positions = bot.portfolio.get_open_positions()
    table = []

    for symbol, pos in positions.items():
        last_price = bot.engine.last_price.get(symbol, pos["entry"])
        profit = (last_price - pos["entry"]) if pos["side"] == "BUY" else (pos["entry"] - last_price)
        roi = (profit / pos["entry"]) * 100 if pos["entry"] else 0
        table.append({
            "symbol": symbol,
            "side": pos["side"],
            "entry": pos["entry"],
            "price": last_price,
            "tp": pos.get("trailing"),
            "status": "OPEN",
            "pl": round(profit, 4),
            "roi": f"{roi:.2f}%",
            "timestamp": pos.get("timestamp"),
            "opened_at": pos.get("timestamp"),
        })

    closed = bot.portfolio.get_closed()
    return render_template("portfolio.html", positions=table, closed_positions=closed)

@portfolio_bp.route("/positions")
def positions():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    return render_template("positions.html", positions=bot.portfolio.get_open_positions(), bot=bot)

@portfolio_bp.route("/export_portfolio")
def export_portfolio():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    file_path = bot.portfolio.export_to_csv()
    if file_path:
        return send_from_directory(PORTFOLIO_FOLDER, "portfolio.csv", as_attachment=True)
    return "Export failed", 500

@portfolio_bp.route("/export_history")
def export_history():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    filename = bot.portfolio.export_history_to_csv()
    if filename:
        return send_file(filename, as_attachment=True)
    return "Export history failed", 500