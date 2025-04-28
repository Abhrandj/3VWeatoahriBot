import os

# Base path dari project
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Folder Uploads
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
# Folder Graphs (static/graphs)
GRAPH_FOLDER = os.path.join(BASE_DIR, "app", "static", "graphs")
# Folder Portfolio History (static/portfolio)
PORTFOLIO_FOLDER = os.path.join(BASE_DIR, "app", "static", "portfolio")

# Auto create folder jika belum ada
for folder in [UPLOAD_FOLDER, GRAPH_FOLDER, PORTFOLIO_FOLDER]:
    os.makedirs(folder, exist_ok=True)