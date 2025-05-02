from flask import Blueprint, redirect, url_for, request, flash
from core.bot_instance import bot

trade_bp = Blueprint('trade', __name__)

@trade_bp.route("/trade/buy/<pair>", methods=["POST"])
def open_buy(pair):
    bot.open_buy(pair)
    flash(f"Buy order placed for {pair}!", "success")
    return redirect(url_for('dashboard.dashboard'))

@trade_bp.route("/trade/sell/<pair>", methods=["POST"])
def open_sell(pair):
    bot.open_sell(pair)
    flash(f"Sell order placed for {pair}!", "danger")
    return redirect(url_for('dashboard.dashboard'))

@trade_bp.route("/trade/close/<pair>", methods=["POST"])
def close_position(pair):
    bot.close_position(pair)
    flash(f"Closed position for {pair}.", "warning")
    return redirect(url_for('dashboard.dashboard'))