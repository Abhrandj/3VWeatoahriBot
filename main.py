# main.py

import os
from app import create_app

# Auto-create essential folders
required_dirs = [
    "uploads",
    "app/static/graphs",
    "app/static/portfolio"
]

for directory in required_dirs:
    os.makedirs(directory, exist_ok=True)

# Create Flask app instance
app = create_app()

# Run server
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))