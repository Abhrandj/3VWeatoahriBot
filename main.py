import os

# Auto-create essential folders
required_dirs = [
    "uploads",
    "app/static/graphs",
    "app/static/portfolio"
]

for d in required_dirs:
    os.makedirs(d, exist_ok=True)

# Import Flask App
from app import create_app

# Create app instance
app = create_app()

# Run app
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))