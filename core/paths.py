import os

# Path dasar
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Folder uploads
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Folder untuk grafik
GRAPHS_FOLDER = os.path.join(BASE_DIR, "app", "static", "graphs")
os.makedirs(GRAPHS_FOLDER, exist_ok=True)

# Folder untuk portfolio export
PORTFOLIO_FOLDER = os.path.join(BASE_DIR, "app", "static", "portfolio")
os.makedirs(PORTFOLIO_FOLDER, exist_ok=True)