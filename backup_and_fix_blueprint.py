import os
import shutil
import zipfile

def backup_templates_folder(src="./app/templates", backup="./app/templates_backup"):
    if not os.path.exists(backup):
        shutil.copytree(src, backup)
        print(f"[Backup] Folder '{src}' berhasil di-copy ke '{backup}'")
    else:
        print(f"[Backup] Folder backup '{backup}' sudah ada. Lewat...")

def zip_backup_folder(folder="./app/templates_backup", zip_name="./app/templates_backup.zip"):
    if os.path.exists(folder):
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, folder)
                    zipf.write(filepath, arcname)
        print(f"[ZIP] Folder '{folder}' berhasil di-zip ke '{zip_name}'")
    else:
        print(f"[ZIP] Folder backup '{folder}' tidak ditemukan!")

def scan_and_fix_html_files(base_dir="./app/templates"):
    blueprint_suffix = "_bp"
    fixed = 0
    total_files = 0

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                if blueprint_suffix in content:
                    print(f"[!] Found in: {filepath}")
                    print("-" * 40)

                    # Show preview
                    lines = content.splitlines()
                    for idx, line in enumerate(lines):
                        if blueprint_suffix in line:
                            print(f"Line {idx + 1}: {line.strip()}")

                    # Auto fix: replace _bp. → .
                    new_content = content.replace(blueprint_suffix + ".", ".")

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)

                    fixed += 1
                total_files += 1

    print("\n=== SUMMARY ===")
    print(f"Total HTML files checked: {total_files}")
    print(f"Files fixed: {fixed}")
    if fixed == 0:
        print("No problems found. All clean!")

if __name__ == "__main__":
    backup_templates_folder()
    zip_backup_folder()
    scan_and_fix_html_files()