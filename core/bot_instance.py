import os
from dotenv import load_dotenv
import pandas as pd

from core.trading_engine import TradingEngine
from core.risk_management import RiskManager
from core.portfolio_manager import Portfolio
from core.telegram import send_telegram_message, send_telegram_photo
from core.ai_predictor import predict_next_close_linear
from core.mini_chart import generate_mini_chart


class Bot:
    _instance = None

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OKX_API_KEY")
        api_secret = os.getenv("OKX_API_SECRET")
        passphrase = os.getenv("OKX_PASSPHRASE")

        self.engine = TradingEngine(api_key, api_secret, passphrase)
        self.risk = RiskManager()
        self.portfolio = Portfolio()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def run(self):
        signals = self.engine.evaluate_signal()
        ai_signals = {}

        for symbol in self.engine.symbols:
            df = self.engine.get_data(symbol)
            if df is not None and len(df) >= 10:
                predicted = predict_next_close_linear(df)
                last_price = df["close"].iloc[-1]
                if predicted is not None:
                    direction = "BUY" if predicted > last_price else "SELL"
                    ai_signals[symbol] = f"{direction} Predicted {predicted:.2f}"
                else:
                    ai_signals[symbol] = "N/A"
            else:
                ai_signals[symbol] = "N/A"

        combined_signals = {}

        for symbol, signal in signals.items():
            current_price = self.engine.last_price.get(symbol)
            if current_price is None:
                continue

            # === PORTFOLIO LOGIC ===
            action = signal.get("strategy_signal")
            if action in ["BUY", "SELL"]:
                if symbol not in self.portfolio.get_all():
                    self.portfolio.open_position(symbol, action, current_price)

            self.portfolio.update_trailing(symbol, current_price)

            if self.portfolio.check_exit(symbol, current_price):
                pos = self.portfolio.get_all().get(symbol, {})
                if pos:
                    entry = pos["entry"]
                    side = pos["side"]
                    roi = (current_price - entry) / entry * 100 if side == "BUY" else (entry - current_price) / entry * 100
                    msg = f"Trailing Stop Triggered: {symbol}\nExit @ {current_price:.2f} | ROI: {roi:.2f}%"
                    send_telegram_message(msg)
                self.portfolio.close_position(symbol)

            # === NOTIFIKASI ===
            tags = signal.get("tags", [])
            tags_str = ", ".join(tags)

            text = (
                f"{symbol}\n"
                f"Strategy: {signal.get('strategy_signal', '-')}\n"
                f"AI: {ai_signals.get(symbol, '-')}\n"
                f"Price: {current_price:.2f}\n"
                f"Tags: {tags_str}"
            )
            mini_path = generate_mini_chart(symbol)
            if mini_path and os.path.exists(mini_path):
                send_telegram_photo(mini_path, caption=text)
            else:
                send_telegram_message(text)

            combined_signals[symbol] = {
                "strategy_signal": action,
                "ai_signal": ai_signals.get(symbol, "N/A"),
                "price": current_price
            }

        return combined_signals


# Singleton instance (hanya di baris ini, cukup satu kali)
bot = Bot.get_instance()