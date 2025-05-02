# run_loop.py

import time
from core.bot_instance import bot

if __name__ == "__main__":
    print("=== Auto Loop Bot Started ===")
    while True:
        try:
            print("[AUTO] Bot is running...")
            bot.run()
        except Exception as e:
            print(f"[ERROR] Bot gagal jalan: {e}")
        time.sleep(60)  # Jalankan tiap 60 detik