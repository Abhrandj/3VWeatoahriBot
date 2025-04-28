from flask import Blueprint, render_template, session, redirect, url_for

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
def home():
    # Cek kalau belum login
    if "user" not in session:
        return redirect(url_for("auth.login"))
    # Kalau sudah login, baru render home.html
    return render_template("home.html", username=session["user"])