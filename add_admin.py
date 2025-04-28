from core.auth import add_user

if __name__ == "__main__":
    username = input("Masukkan username baru: ").strip()
    password = input("Masukkan password baru: ").strip()

    if add_user(username, password):
        print(f"[SUCCESS] User '{username}' berhasil ditambahkan!")
    else:
        print(f"[ERROR] User '{username}' sudah ada!")