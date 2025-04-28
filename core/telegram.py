# core/telegram.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str) -> None:
    """
    Mengirim pesan teks ke Telegram.
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Telegram] Token atau Chat ID belum diset di .env")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)  # <- Pake JSON di sini
        if response.status_code != 200:
            print(f"[Telegram] Gagal kirim pesan: {response.text}")
        else:
            print("[Telegram] Pesan berhasil dikirim.")
    except Exception as e:
        print(f"[Telegram] Exception saat kirim pesan: {e}")

def send_telegram_photo(image_path: str, caption: str = "") -> None:
    """
    Mengirim gambar ke Telegram dengan caption opsional.
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Telegram] Token atau Chat ID belum diset di .env")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    try:
        with open(image_path, "rb") as photo:
            files = {"photo": photo}
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": caption
            }
            response = requests.post(url, data=data, files=files)
            if response.status_code != 200:
                print(f"[Telegram] Gagal kirim foto: {response.text}")
            else:
                print("[Telegram] Foto berhasil dikirim.")
    except Exception as e:
        print(f"[Telegram] Exception saat kirim foto: {e}")