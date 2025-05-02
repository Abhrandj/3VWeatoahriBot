# app/routes/home_routes.py

from flask import Blueprint, render_template, session

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
def home():
    return render_template("home.html", username=session.get("user"))