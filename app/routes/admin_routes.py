# app/routes/admin_routes.py

from flask import Blueprint, render_template, session, redirect, url_for
from core.auth import load_users
from app.routes.auth_routes import login_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin_panel")
@login_required
def admin_panel():
    users = load_users()
    return render_template("admin_panel.html", users=users)