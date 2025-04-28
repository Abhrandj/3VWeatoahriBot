# test_telegram.py

from core.telegram import send_telegram_message

if __name__ == "__main__":
    test_message = "✅ Test message berhasil dikirim dari TradingBot (via test_telegram.py)"
    send_telegram_message(test_message)