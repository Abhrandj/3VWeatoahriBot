import os

# Pastikan base path dinamis berdasarkan posisi jalan app
BASE_DIR = os.getcwd()

# Folder uploads
UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Folder untuk grafik backtest & dashboard
GRAPHS_FOLDER = os.path.join(BASE_DIR, "app", "static", "graphs")
os.makedirs(GRAPHS_FOLDER, exist_ok=True)

# Folder untuk export portfolio
PORTFOLIO_FOLDER = os.path.join(BASE_DIR, "app", "static", "portfolio")
os.makedirs(PORTFOLIO_FOLDER, exist_ok=True)

# Folder untuk hasil live prediction chart
LIVE_BACKTEST_FOLDER = os.path.join(BASE_DIR, "app", "static")
os.makedirs(LIVE_BACKTEST_FOLDER, exist_ok=True)