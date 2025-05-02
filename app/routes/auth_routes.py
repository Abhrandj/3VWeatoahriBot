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
            flash("Login berhasil!", "success")
            return redirect(url_for("home_bp.home"))  # Setelah login, ke landing/home
        else:
            flash("Username atau password salah!", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Anda telah logout.", "info")
    return redirect(url_for("home_bp.home"))  # Redirect ke landing page setelah logout