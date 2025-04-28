import os
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

from core.backtest_engine import run_backtest
from core.data_downloader import fetch_and_save

# Inisialisasi Blueprint
backtest_bp = Blueprint("backtest_bp", __name__)

# Setup Upload Folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', '..', 'app', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@backtest_bp.route('/', methods=['GET', 'POST'])
def backtest():
    result = None
    filename = None
    error = None

    if request.method == 'POST':
        # Handle file upload
        if "csv_file" in request.files:
            file = request.files["csv_file"]
            if file and file.filename.lower().endswith(".csv"):
                try:
                    filename = secure_filename(file.filename)
                    path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(path)
                    result = run_backtest(path)
                except Exception as e:
                    error = str(e)

        # Handle symbol download
        elif "symbol" in request.form:
            symbol = request.form.get("symbol")
            bar = request.form.get("bar")
            total = int(request.form.get("total", 1000))
            try:
                filename = fetch_and_save(symbol, bar, total)
                path = os.path.join(UPLOAD_FOLDER, filename)
                result = run_backtest(path)
            except Exception as e:
                error = str(e)

    return render_template("backtest.html", result=result, filename=filename, error=error)