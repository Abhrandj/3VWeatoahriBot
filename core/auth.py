import os
import csv
import bcrypt

USERS_FILE = os.path.join("data", "users.csv")

def load_users():
    if not os.path.exists(USERS_FILE):
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password"])  # Header
        print("[INFO] User database created at:", USERS_FILE)

    users = {}
    with open(USERS_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[row["username"]] = row["password"]
    return users

def authenticate(username, password):
    users = load_users()
    if username in users:
        stored_hash = users[username]
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
    return False

def add_user(username, password):
    users = load_users()
    if username in users:
        return False  # Username already exists

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    with open(USERS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([username, hashed_password.decode("utf-8")])
    return True