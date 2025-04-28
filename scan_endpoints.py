# scan_endpoints.py

import os
import re

def scan_folder(folder):
    print(f"Scanning folder: {folder}")
    problems = []

    for subdir, dirs, files in os.walk(folder):
        for filename in files:
            if filename.endswith((".py", ".html")):
                filepath = os.path.join(subdir, filename)
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    # Cari url_for endpoint pattern
                    matches = re.findall(r"url_for\(\s*['\"]([^'\"]+)['\"]", content)
                    for match in matches:
                        if match.startswith("main."):
                            problems.append((filepath, match))

    if problems:
        print("\n[!] Found potential issues:")
        for filepath, match in problems:
            print(f" - {filepath} : {match}")
    else:
        print("\n✅ No problem found. All endpoint references look clean!")

if __name__ == "__main__":
    scan_folder("./app")  # Folder app/