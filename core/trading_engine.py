# core/trading_engine.py

import pandas as pd
from core.okx_sdk import OKXClient
from core.risk_management import RiskManager
from core.utils import fetch_ohlcv
from core.indicators import calculate_indicators
from core.ai_predictor import predict_next_close_linear, predict_next_close_prophet
from core.strategy_engine import StrategyEngine

class TradingEngine:
    def __init__(self, api_key, api_secret, passphrase, symbols=None):
        self.okx = OKXClient(api_key, api_secret, passphrase)
        self.symbols = symbols if symbols else ["BTC-USDT", "ETH-USDT", "SOL-USDT"]
        self.last_price = {}
        self.position = {}
        self.risk_manager = RiskManager()
        self.ai_predictions = {}
        self.cached_df = {}

    def get_data(self, symbol):
        if symbol in self.cached_df:
            return self.cached_df[symbol]

        df = fetch_ohlcv(symbol, interval='1m', limit=100)
        if df is None or len(df) < 50:
            print(f"[ERROR] Data terlalu sedikit untuk {symbol}")
            return None

        df = pd.DataFrame(df, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df = calculate_indicators(df)

        required_cols = ['ema_20', 'ema_50', 'ema200', 'ma_200', 'rsi',
                         'upper_band', 'lower_band', 'macd_histogram']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            print(f"[ERROR] Indikator tidak lengkap untuk {symbol}. Missing: {missing}")
            return None

        print(f"[OK] {symbol} data lengkap. Kolom: {df.columns.tolist()[-8:]}")
        self.cached_df[symbol] = df
        return df

    def get_ohlcv(self, symbol, interval='1m', limit=100):
        return fetch_ohlcv(symbol, interval, limit)

    def get_ai_signal(self, symbol):
        return self.ai_predictions.get(symbol, "N/A")

    def update_prices(self):
        for symbol in self.symbols:
            ticker = self.okx.get_ticker(symbol)
            if 'data' in ticker and isinstance(ticker['data'], list) and len(ticker['data']) > 0:
                try:
                    price = float(ticker['data'][0]['last'])
                    self.last_price[symbol] = price
                except (KeyError, ValueError) as e:
                    print(f"Gagal parsing harga untuk {symbol}: {e}")

    def evaluate_signal(self):
        self.update_prices()
        self.ai_predictions = {}
        self.cached_df = {}
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
            ai_signal = "BUY" if prophet_pred and current_price < prophet_pred else "SELL"
            self.ai_predictions[symbol] = ai_signal

        self.strategy_engine = StrategyEngine(
            symbols=self.symbols,
            get_data=lambda symbol: self.cached_df.get(symbol),
            get_ai_signal=self.get_ai_signal
        )
        strategy_signals = self.strategy_engine.evaluate_all()

        for symbol in self.symbols:
            signals[symbol] = {
                "strategy_signal": strategy_signals.get(symbol, {}).get("strategy_signal", "HOLD"),
                "ai_signal": self.ai_predictions.get(symbol, "N/A"),
                "tags": strategy_signals.get(symbol, {}).get("tags", [])
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