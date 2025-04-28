import os
import csv
import bcrypt
from core.auth import USERS_FILE

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users[row["username"]] = row["password"]
    return users

def save_users(users):
    with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password"])
        for username, password in users.items():
            writer.writerow([username, password])

def add_user():
    username = input("Masukkan username baru: ").strip()
    password = input("Masukkan password baru: ").strip()
    users = load_users()

    if username in users:
        print(f"[ERROR] User '{username}' sudah ada!")
        return

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users[username] = hashed_password.decode("utf-8")
    save_users(users)
    print(f"[SUCCESS] User '{username}' berhasil dibuat!")

def list_users():
    users = load_users()
    print("\n[INFO] Daftar User:")
    for idx, username in enumerate(users.keys(), 1):
        print(f"{idx}. {username}")

def update_password():
    username = input("Masukkan username yang ingin diganti password: ").strip()
    users = load_users()

    if username not in users:
        print(f"[ERROR] User '{username}' tidak ditemukan!")
        return

    new_password = input("Masukkan password baru: ").strip()
    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
    users[username] = hashed_password.decode("utf-8")
    save_users(users)
    print(f"[SUCCESS] Password user '{username}' berhasil diganti!")

def delete_user():
    username = input("Masukkan username yang ingin dihapus: ").strip()
    users = load_users()

    if username not in users:
        print(f"[ERROR] User '{username}' tidak ditemukan!")
        return

    confirm = input(f"Apakah anda yakin ingin menghapus user '{username}'? (y/n): ").lower()
    if confirm == "y":
        users.pop(username)
        save_users(users)
        print(f"[SUCCESS] User '{username}' berhasil dihapus!")
    else:
        print("[CANCEL] Penghapusan dibatalkan.")

def main_menu():
    while True:
        print("\n=== User Management CLI ===")
        print("1. Tambah User Baru")
        print("2. Lihat Semua User")
        print("3. Ganti Password User")
        print("4. Hapus User")
        print("0. Keluar")
        choice = input("Pilih opsi: ")

        if choice == "1":
            add_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            update_password()
        elif choice == "4":
            delete_user()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("[ERROR] Pilihan tidak valid!")

if __name__ == "__main__":
    main_menu()