import os
from flask import Flask

# Import semua Blueprint dari routes
from app.routes.auth_routes import auth_bp
from app.routes.home_routes import home_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.backtest_routes import backtest_bp
from app.routes.portfolio_routes import portfolio_bp
from app.routes.live_backtest_routes import live_backtest_bp
from app.routes.trade_routes import trade_bp  # Penting untuk eksekusi trading manual

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_secret_key")  # Gunakan env key jika ada

    # Buat folder penting jika belum ada
    folders_to_create = [
        os.path.join(os.getcwd(), "uploads"),
        os.path.join(os.getcwd(), "app", "static", "graphs"),
        os.path.join(os.getcwd(), "app", "static", "portfolio"),
        os.path.join(os.getcwd(), "app", "static", "mini"),
    ]
    for folder in folders_to_create:
        os.makedirs(folder, exist_ok=True)

    # Daftarkan semua blueprint
    all_blueprints = [
        (auth_bp, ""),                        # Login/Logout
        (home_bp, "/"),                       # Landing Page
        (dashboard_bp, "/dashboard"),         # Dashboard
        (backtest_bp, "/backtest"),           # Backtesting
        (portfolio_bp, "/portfolio"),         # Portfolio Tracking
        (live_backtest_bp, "/live_backtest"), # Live AI Prediction
        (trade_bp, "/trade"),                 # Manual Trade
    ]
    for bp, prefix in all_blueprints:
        app.register_blueprint(bp, url_prefix=prefix)

    return app