import os
import zipfile
from datetime import datetime

def safe_write(zipf, filepath, arcname):
    try:
        zipf.write(filepath, arcname)
    except ValueError:
        print(f"[WARNING] Skip file (bad timestamp): {filepath}")

def backup_project(source_dir="./", output_dir="./backups"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join(output_dir, f"tradingbot_backup_{timestamp}.zip")

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(source_dir):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                if (
                    not filepath.startswith("./backups") and
                    not filepath.endswith(".zip") and
                    ".git" not in filepath and
                    "__pycache__" not in filepath and
                    ".replit" not in filepath and
                    ".venv" not in filepath
                ):
                    arcname = os.path.relpath(filepath, source_dir)
                    safe_write(zipf, filepath, arcname)

    print(f"[SUCCESS] Backup created: {zip_filename}")

if __name__ == "__main__":
    backup_project()