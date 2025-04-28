# setup_folder.py

import os

# List folder yang wajib ada
folders = [
    "uploads",
    "app/static/graphs",
    "app/static/portfolio"
]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Folder dibuat: {folder}")

    # Buat file .keep di dalam folder
    keep_path = os.path.join(folder, ".keep")
    with open(keep_path, "w") as f:
        f.write("")  # Isi kosong
    print(f".keep file dibuat: {keep_path}")

print("Setup folder dan .keep selesai.")