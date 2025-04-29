import os
from flask import Blueprint, render_template, session, redirect, url_for
from core.paths import LIVE_BACKTEST_FOLDER

live_backtest_bp = Blueprint("live_backtest", __name__)

@live_backtest_bp.route("/")
def live_backtest():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    return render_template("live_backtest.html")