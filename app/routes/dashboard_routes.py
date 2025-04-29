import os
from flask import Blueprint, render_template, session, redirect, url_for
from core.paths import GRAPHS_FOLDER

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html")