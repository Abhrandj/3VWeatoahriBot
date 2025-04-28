# app/routes/auth_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from core.auth import authenticate

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if authenticate(username, password):
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard.dashboard"))  # ⟵ langsung ke dashboard
        else:
            flash("Invalid credentials!", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("auth.login"))