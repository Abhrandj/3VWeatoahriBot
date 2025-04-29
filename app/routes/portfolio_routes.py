import os
from flask import Blueprint, render_template, redirect, url_for, session
from core.bot_instance import bot
from core.utils import save_to_csv
from core.paths import PORTFOLIO_FOLDER, GRAPHS_FOLDER

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("/", methods=["GET"])
def portfolio():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    positions = bot.portfolio.get_all()
    closed_positions = bot.portfolio.get_closed()

    return render_template("portfolio.html", positions=positions, closed_positions=closed_positions)

@portfolio_bp.route("/export")
def export_portfolio():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    positions = bot.portfolio.get_all()
    filepath = os.path.join(PORTFOLIO_FOLDER, "open_positions.csv")
    save_to_csv(filepath, positions)
    return redirect(url_for("portfolio.portfolio"))

@portfolio_bp.route("/export_history")
def export_history():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    closed_positions = bot.portfolio.get_closed()
    filepath = os.path.join(PORTFOLIO_FOLDER, "closed_positions.csv")
    save_to_csv(filepath, closed_positions)
    return redirect(url_for("portfolio.portfolio"))