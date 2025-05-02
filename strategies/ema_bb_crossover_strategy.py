import logging
import pandas as pd
from typing import Dict, List, Callable

class EMA_BB_CrossoverStrategy:
    """Strategi kombinasi Bollinger Bands + EMA crossover + MA200 + RSI + AI confirmation."""

    def __init__(
        self,
        symbols: List[str],
        get_data_func: Callable[[str], pd.DataFrame],
        get_ai_signal_func: Callable[[str], str],
        rsi_threshold: float = 50
    ):
        """
        Args:
            symbols: Daftar simbol.
            get_data_func: Fungsi untuk mengambil DataFrame OHLCV.
            get_ai_signal_func: Fungsi ambil sinyal AI ('BUY' / 'SELL').
            rsi_threshold: Level RSI netral sebagai filter tambahan.
        """
        self.symbols = symbols
        self.get_data = get_data_func
        self.get_ai_signal = get_ai_signal_func
        self.rsi_threshold = rsi_threshold
        self.logger = logging.getLogger(__name__)

    def check_signals(self) -> Dict[str, Dict[str, str]]:
        signals = {}

        for symbol in self.symbols:
            try:
                df = self.get_data(symbol)
                if df is None or len(df) < 50:
                    self.logger.warning(f"Data tidak cukup untuk {symbol}.")
                    continue

                required_columns = ['close', 'ema_20', 'ema_50', 'ma_200', 'lower_bb', 'upper_bb', 'rsi']
                if not all(col in df.columns for col in required_columns):
                    self.logger.error(f"Indikator tidak lengkap untuk {symbol}.")
                    continue

                current_price = df['close'].iloc[-1]
                ema20 = df['ema_20'].iloc[-1]
                ema50 = df['ema_50'].iloc[-1]
                ma200 = df['ma_200'].iloc[-1]
                lower_bb = df['lower_bb'].iloc[-1]
                upper_bb = df['upper_bb'].iloc[-1]
                rsi = df['rsi'].iloc[-1]
                close_prev = df['close'].iloc[-2]

                ai_signal = self.get_ai_signal(symbol).upper()

                buy_condition = (
                    current_price < lower_bb and
                    ema20 > ema50 and
                    close_prev < ema20 and current_price > ema20 and
                    current_price > ma200 and
                    rsi < self.rsi_threshold and
                    ai_signal == "BUY"
                )

                sell_condition = (
                    current_price > upper_bb and
                    ema20 < ema50 and
                    close_prev > ema20 and current_price < ema20 and
                    current_price < ma200 and
                    rsi > self.rsi_threshold and
                    ai_signal == "SELL"
                )

                if buy_condition:
                    signals[symbol] = {
                        "strategy_signal": "BUY",
                        "tags": ["EMA+BB", "Trend Up", "AI Confirm", "RSI < threshold"]
                    }
                elif sell_condition:
                    signals[symbol] = {
                        "strategy_signal": "SELL",
                        "tags": ["EMA+BB", "Trend Down", "AI Confirm", "RSI > threshold"]
                    }

            except Exception as e:
                self.logger.error(f"Error {symbol}: {str(e)}")

        return signals