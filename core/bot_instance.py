import os
import csv
import datetime
from dotenv import load_dotenv
from core.okx_client import OKXClient
from core.trading_engine import TradingEngine
from core.risk_management import RiskManager
from core.portfolio_manager import Portfolio
from core.telegram import send_telegram_message, send_telegram_photo
from core.ai_predictor import predict_next_close_linear
from core.mini_chart import generate_mini_chart
from core.strategy_engine import StrategyEngine
from core.utils import is_live_mode

class BotInstance:
    _instance = None

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OKX_API_KEY")
        api_secret = os.getenv("OKX_API_SECRET")
        passphrase = os.getenv("OKX_PASSPHRASE")

        self.engine = TradingEngine(api_key, api_secret, passphrase)
        self.risk = RiskManager()
        self.portfolio = Portfolio()
        self.ai_signals = {}
        self.custom_lot_size = {}
        self.trailing_data = {}

        def get_ai_signal(symbol):
            return self.ai_signals.get(symbol, "N/A").split()[0]

        self.strategy_engine = StrategyEngine(
            symbols=self.engine.symbols,
            get_data=self.engine.get_data,
            get_ai_signal=get_ai_signal
        )

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_price(self, pair):
        if not pair.endswith("-SWAP"):
            pair = f"{pair}-SWAP"

        price = self.engine.last_price.get(pair)
        if price:
            return price
        try:
            ticker = self.engine.okx.get_ticker(pair)
            price = float(ticker.get("last", 0))
            if price > 0:
                self.engine.last_price[pair] = price
                self.log_price(pair, price)
                return price
        except Exception as e:
            send_telegram_message(f"[ERROR] get_price({pair}) failed: {e}")
            print(f"[ERROR] Failed to fetch real-time price for {pair}: {e}")
        return None

    def log_price(self, pair, price):
        path = f"data/price_log_{pair.replace('-', '').replace('SWAP', '')}.csv"
        os.makedirs("data", exist_ok=True)
        with open(path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.datetime.now().isoformat(), pair, price])

    def run(self, notify=True):
        self.ai_signals = {}
        for symbol in self.engine.symbols:
            df = self.engine.get_data(symbol)
            if df is not None and len(df) >= 10:
                predicted = predict_next_close_linear(df)
                last_price = df['close'].iloc[-1]
                direction = "BUY" if predicted > last_price else "SELL"
                self.ai_signals[symbol] = direction
            else:
                self.ai_signals[symbol] = "N/A"

        signals = self.strategy_engine.evaluate_all()
        combined_signals = {}

        for symbol, signal in signals.items():
            current_price = self.get_price(symbol)
            if current_price is None:
                continue

            action = signal.get("strategy_signal", "HOLD")
            tags = signal.get("tags", [])

            if action in ["BUY", "SELL"] and symbol not in self.portfolio.get_all():
                self.portfolio.open_position(symbol, action, current_price)

            self.portfolio.update_trailing(symbol, current_price)

            if self.portfolio.check_exit(symbol, current_price):
                pos = self.portfolio.get_all().get(symbol, {})
                if pos:
                    entry = pos["entry"]
                    side = pos["side"]
                    roi = (current_price - entry) / entry * 100 if side == "BUY" else (entry - current_price) / entry * 100
                    if notify:
                        send_telegram_message(f"Trailing Stop Triggered: {symbol}\nExit @ {current_price:.2f}\nROI: {roi:.2f}%")
                self.portfolio.close_position(symbol)

            if notify:
                text = f"{symbol}\nStrategy: {action}\nAI: {self.ai_signals.get(symbol, '-')}\nPrice: {current_price:.2f}\nTags: {', '.join(tags)}"
                chart = generate_mini_chart(symbol)
                if chart and os.path.exists(chart):
                    send_telegram_photo(chart, caption=text)
                else:
                    send_telegram_message(text)

            combined_signals[symbol] = {
                "strategy_signal": action,
                "ai_signal": self.ai_signals.get(symbol, "N/A"),
                "price": current_price,
                "tags": tags
            }

        self.manage_trailing()
        return combined_signals

    def calculate_dynamic_lot_size(self, pair, balance, risk_pct, leverage, price):
        margin = balance / leverage
        qty = self.custom_lot_size.get(pair, round((margin * risk_pct) / price, 4))
        return qty

    def open_buy(self, pair, balance=100, risk_pct=0.005, leverage=10):
        price = self.get_price(pair)
        if not price:
            send_telegram_message(f"[ERROR] Price not available for {pair}")
            return
        qty = self.calculate_dynamic_lot_size(pair, balance, risk_pct, leverage, price)
        pair_swap = pair if pair.endswith("-SWAP") else f"{pair}-SWAP"

        if is_live_mode():
            self.engine.okx.place_order(pair_swap, side="buy", size=qty)
            sl = round(price * 0.99, 2)
            tp = round(price * 1.03, 2)
            self.engine.okx.place_trigger_order(pair_swap, side="sell", trigger_price=tp, order_type="limit", size=qty)
            self.engine.okx.place_trigger_order(pair_swap, side="sell", trigger_price=sl, order_type="market", size=qty)
            self.trailing_data[pair_swap] = {"entry_price": price, "best_price": price, "qty": qty, "side": "BUY"}
            send_telegram_message(f"[REAL BUY] {pair_swap} | Qty: {qty} | Entry: {price} | TP: {tp} | SL: {sl}")
        else:
            send_telegram_message(f"[TEST BUY] {pair_swap} | Qty: {qty} | Price: {price}")

    def open_sell(self, pair, balance=100, risk_pct=0.005, leverage=10):
        price = self.get_price(pair)
        if not price:
            send_telegram_message(f"[ERROR] Price not available for {pair}")
            return
        qty = self.calculate_dynamic_lot_size(pair, balance, risk_pct, leverage, price)
        pair_swap = pair if pair.endswith("-SWAP") else f"{pair}-SWAP"

        if is_live_mode():
            self.engine.okx.place_order(pair_swap, side="sell", size=qty)
            sl = round(price * 1.01, 2)
            tp = round(price * 0.97, 2)
            self.engine.okx.place_trigger_order(pair_swap, side="buy", trigger_price=tp, order_type="limit", size=qty)
            self.engine.okx.place_trigger_order(pair_swap, side="buy", trigger_price=sl, order_type="market", size=qty)
            self.trailing_data[pair_swap] = {"entry_price": price, "best_price": price, "qty": qty, "side": "SELL"}
            send_telegram_message(f"[REAL SELL] {pair_swap} | Qty: {qty} | Entry: {price} | TP: {tp} | SL: {sl}")
        else:
            send_telegram_message(f"[TEST SELL] {pair_swap} | Qty: {qty} | Price: {price}")

    def close_position(self, pair):
        pair_swap = pair if pair.endswith("-SWAP") else f"{pair}-SWAP"
        pos = self.portfolio.get_all().get(pair)
        if not pos:
            send_telegram_message(f"[CLOSE FAILED] No open position for {pair}")
            return

        price = self.get_price(pair)
        if not price:
            send_telegram_message(f"[ERROR] Cannot close, price not available for {pair}")
            return

        self.cancel_all_triggers(pair_swap)
        side = "sell" if pos["side"] == "BUY" else "buy"
        qty = round(pos.get("entry_amount", 0.001), 4)

        if is_live_mode():
            self.engine.okx.place_order(pair_swap, side=side, size=qty)
            send_telegram_message(f"[MANUAL CLOSE] {pair_swap} | Side: {side} | Qty: {qty} | Price: {price}")
        else:
            send_telegram_message(f"[TEST CLOSE] {pair_swap} | Side: {side} | Qty: {qty} | Price: {price}")

        if pair_swap in self.trailing_data:
            del self.trailing_data[pair_swap]

    def cancel_all_triggers(self, pair):
        if not pair.endswith("-SWAP"):
            pair = f"{pair}-SWAP"
        try:
            result = self.engine.okx.cancel_algos(pair)
            if result.get("error"):
                send_telegram_message(f"[CANCEL ERROR] {pair} | {result['error']}")
            elif result.get("result"):
                send_telegram_message(f"[CANCEL TRIGGERS] {pair} | {result['result']}")
            elif result.get("code") == "0":
                send_telegram_message(f"[CANCEL TRIGGERS] {pair} | Success")
            else:
                send_telegram_message(f"[CANCEL TRIGGERS] {pair} | Result: {result}")
        except Exception as e:
            send_telegram_message(f"[ERROR] Cancel trigger gagal {pair} | {str(e)}")

    def manage_trailing(self):
        for pair, data in self.trailing_data.items():
            current_price = self.get_price(pair)
            if not current_price:
                continue

            entry = data["entry_price"]
            best = data["best_price"]
            side = data["side"]

            if side == "BUY" and current_price > best:
                self.trailing_data[pair]["best_price"] = current_price
            elif side == "SELL" and current_price < best:
                self.trailing_data[pair]["best_price"] = current_price

            if side == "BUY":
                gain = (current_price - entry) / entry * 100
                if gain > 1:
                    trigger_price = best * 0.997
                    send_telegram_message(f"[TRAILING BUY] {pair} | New SL: {trigger_price:.2f}")
            elif side == "SELL":
                gain = (entry - current_price) / entry * 100
                if gain > 1:
                    trigger_price = best * 1.003
                    send_telegram_message(f"[TRAILING SELL] {pair} | New SL: {trigger_price:.2f}")

def get_price(self, pair):
    # Jika pair belum pakai -SWAP, tambahkan otomatis
    futures_pair = pair if pair.endswith("-SWAP") else f"{pair}-SWAP"

    price = self.engine.last_price.get(futures_pair)
    if price:
        return price

    try:
        ticker = self.engine.okx.get_ticker(futures_pair)
        price = float(ticker.get("last", 0))
        if price > 0:
            self.engine.last_price[futures_pair] = price
            self.log_price(futures_pair, price)
            return price
    except Exception as e:
        msg = f"[ERROR] get_price({futures_pair}) failed: {e}"
        print(msg)
        send_telegram_message(msg)

    return None

# Singleton
bot = BotInstance.get_instance()