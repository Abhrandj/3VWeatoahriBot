import os
from flask import Flask

# Import semua Blueprint
from app.routes.auth_routes import auth_bp
from app.routes.home_routes import home_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.backtest_routes import backtest_bp
from app.routes.portfolio_routes import portfolio_bp
from app.routes.live_backtest_routes import live_backtest_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_secret_key")  # Gunakan SECRET_KEY dari environment kalau ada

    # === FIX: Pastikan semua folder penting ada ===
    folders_to_create = [
        os.path.join(os.getcwd(), "uploads"),
        os.path.join(os.getcwd(), "app", "static", "graphs"),
        os.path.join(os.getcwd(), "app", "static", "portfolio"),
    ]
    for folder in folders_to_create:
        os.makedirs(folder, exist_ok=True)

    # === Register semua Blueprint
    all_blueprints = [
        (auth_bp, ""),                  # Auth Login/Logout
        (home_bp, "/"),                  # Home Landing Page
        (dashboard_bp, "/dashboard"),    # Dashboard
        (backtest_bp, "/backtest"),       # Backtest
        (portfolio_bp, "/portfolio"),     # Portfolio
        (live_backtest_bp, "/live_backtest"),  # Live Backtest
    ]

    for bp, prefix in all_blueprints:
        app.register_blueprint(bp, url_prefix=prefix)

    return app