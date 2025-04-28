# core/trading_engine.py

import pandas as pd
from core.okx_sdk import OKXClient
from core.risk_management import RiskManager
from core.utils import fetch_ohlcv
from core.indicators import calculate_indicators
from core.ai_predictor import predict_next_close_linear,predict_next_close_prophet
from strategies import run_all_strategies  # Import strategi terpusat

class TradingEngine:
    def __init__(self, api_key, api_secret, passphrase, symbols=None):
        self.okx = OKXClient(api_key, api_secret, passphrase)
        self.symbols = symbols if symbols else ["BTC-USDT", "ETH-USDT", "SOL-USDT"]
        self.last_price = {}
        self.position = {}
        self.risk_manager = RiskManager()

    def update_prices(self):
        for symbol in self.symbols:
            ticker = self.okx.get_ticker(symbol)
            if 'data' in ticker and isinstance(ticker['data'], list) and len(ticker['data']) > 0:
                try:
                    price = float(ticker['data'][0]['last'])
                    self.last_price[symbol] = price
                except (KeyError, ValueError) as e:
                    print(f"Gagal parsing harga untuk {symbol}: {e}")

    def get_data(self, symbol):
        df = fetch_ohlcv(symbol, interval='1m', limit=100)
        if df is None or len(df) < 50:
            return None
        df = pd.DataFrame(df, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df = calculate_indicators(df)
        return df

    def get_ohlcv(self, symbol, interval='1m', limit=100):
        return fetch_ohlcv(symbol, interval, limit)

    def evaluate_signal(self):
        self.update_prices()
        signals = {}

        for symbol in self.symbols:
            price = self.last_price.get(symbol)
            if price is None:
                signals[symbol] = {"strategy_signal": "NO_SIGNAL", "ai_signal": "N/A", "tags": []}
                continue

            df = self.get_data(symbol)
            if df is None:
                signals[symbol] = {"strategy_signal": "NO_DATA", "ai_signal": "N/A", "tags": []}
                continue

            current_price = df['close'].iloc[-1]

            prophet_pred = predict_next_close_prophet(df)
            ai_signal = None
            if prophet_pred:
                ai_signal = "BUY" if current_price < prophet_pred else "SELL"

            tags = run_all_strategies(df, ai_signal)  # Jalankan semua strategi sebagai plugin

            strategy_signal = "HOLD"
            if "EMA_BB_BUY" in tags or "VOL_SPIKE_BUY" in tags:
                strategy_signal = "BUY"
            elif "EMA_BB_SELL" in tags or "VOL_SPIKE_SELL" in tags:
                strategy_signal = "SELL"

            self.last_price[symbol] = current_price
            signals[symbol] = {
                "strategy_signal": strategy_signal,
                "ai_signal": ai_signal or "N/A",
                "tags": tags
            }

        return signals

    def execute_trade(self, signal, current_price):
        stop_loss = self.risk_manager.calculate_stop_loss(current_price)
        take_profit = self.risk_manager.calculate_take_profit(current_price)

        for symbol, result in signal.items():
            action = result["strategy_signal"]
            if action == "BUY":
                response = self.okx.place_order(symbol, side="buy", size=1)
                print(f"Executed BUY on {symbol}:", response)
                print(f"SL: {stop_loss}, TP: {take_profit}")
            elif action == "SELL":
                response = self.okx.place_order(symbol, side="sell", size=1)
                print(f"Executed SELL on {symbol}:", response)
                print(f"SL: {stop_loss}, TP: {take_profit}")
            else:
                print(f"No trade for {symbol}. Signal: {action}")