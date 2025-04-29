import os
from flask import Blueprint, render_template, session, redirect, url_for
from core.paths import PORTFOLIO_FOLDER

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("/")
def portfolio():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    return render_template("portfolio.html")