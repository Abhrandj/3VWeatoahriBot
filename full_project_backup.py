import os
import zipfile
from datetime import datetime

def full_backup_project(output_dir="./backups", exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = ["__pycache__", ".git", ".idea", "venv", ".venv", "env", ".replit", "node_modules", ".pythonlibs"]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join(output_dir, f"project_backup_{timestamp}.zip")

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as backup_zip:
        for foldername, subfolders, filenames in os.walk("."):
            # Skip excluded directories
            if any(excluded in foldername for excluded in exclude_dirs):
                continue

            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                # Skip backup files themselves
                if output_dir in filepath:
                    continue
                arcname = os.path.relpath(filepath, ".")
                backup_zip.write(filepath, arcname)

    print(f"[BACKUP SUCCESS] Full project backup created: {zip_filename}")

if __name__ == "__main__":
    full_backup_project()