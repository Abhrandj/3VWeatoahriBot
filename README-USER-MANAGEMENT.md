# User Management Tools - TradingBot

Tools ini berfungsi untuk mengelola pengguna (admin login) pada sistem TradingBot.

---

## File Tools

| File | Fungsi |
|:--|:--|
| `add_admin.py` | Menambah satu user baru secara cepat dari terminal |
| `manage_users.py` | Menu CLI lengkap: tambah user, lihat user, ganti password, hapus user |

---

## Struktur Database User

- Lokasi: `data/users.csv`
- Format CSV:
  ```csv
  username,password
  admin,$2b$12$encrypted_password_hash