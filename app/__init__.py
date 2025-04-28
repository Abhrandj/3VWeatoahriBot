from flask import Flask

# Import semua Blueprint
from app.routes.main_routes import main_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.backtest_routes import backtest_bp
from app.routes.portfolio_routes import portfolio_bp
from app.routes.live_backtest_routes import live_backtest_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"

    # Daftar semua blueprint + url_prefix
    all_blueprints = [
        (main_bp, "/"),
        (dashboard_bp, "/dashboard"),
        (backtest_bp, "/backtest"),
        (portfolio_bp, "/portfolio"),
        (live_backtest_bp, "/live_backtest"),
    ]

    for bp, prefix in all_blueprints:
        app.register_blueprint(bp, url_prefix=prefix)

    return app