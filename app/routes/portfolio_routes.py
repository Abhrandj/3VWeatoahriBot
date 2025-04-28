import os
from datetime import datetime
from flask import Blueprint, render_template, send_from_directory, send_file, redirect, url_for, session

from core.bot_instance import bot
from core.utils import generate_roi_chart

portfolio_bp = Blueprint("portfolio", __name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

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
        return send_from_directory("static", "portfolio.csv", as_attachment=True)
    return "Export failed", 500

@portfolio_bp.route("/export_history")
def export_history():
    if "user" not in session:
        return redirect(url_for('auth.login'))
    csv_path = os.path.join(BASE_DIR, "..", "static", "portfolio_history.csv")
    filename = bot.portfolio.export_history_to_csv(csv_path)
    return send_file(filename, as_attachment=True)

@portfolio_bp.route("/debug_roi")
def debug_roi():
    if "user" not in session:
        return redirect(url_for('auth.login'))
    dummy_position = {
        "symbol": "BTC-USDT",
        "side": "BUY",
        "entry": 9000,
        "close_price": 9500,
        "roi": (9500 - 9000) / 9000 * 100,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "closed_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

    if dummy_position not in bot.portfolio.closed:
        bot.portfolio.closed.append(dummy_position)

    generate_roi_chart(bot.portfolio.get_closed())
    return redirect(url_for("dashboard.dashboard"))