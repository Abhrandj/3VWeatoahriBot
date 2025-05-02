import logging
import pandas as pd
from typing import Dict, List, Callable

class EMA_PullbackStrategy:
    """Strategi pullback ke EMA20/EMA50 dengan konfirmasi tren EMA200, RSI, dan MACD."""

    def __init__(
        self,
        symbols: List[str],
        get_data_func: Callable[[str], pd.DataFrame],
        rsi_oversold: float = 40,
        rsi_overbought: float = 60
    ):
        self.symbols = symbols
        self.get_data = get_data_func
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.logger = logging.getLogger(__name__)

    def check_signals(self) -> Dict[str, Dict[str, str]]:
        signals = {}

        for symbol in self.symbols:
            try:
                df = self.get_data(symbol)
                if df is None or len(df) < 50:
                    self.logger.warning(f"Data tidak cukup untuk {symbol}.")
                    continue

                required_columns = ['close', 'ema20', 'ema50', 'ema200', 'rsi', 'macd_histogram']
                if not all(col in df.columns for col in required_columns):
                    self.logger.error(f"Indikator tidak lengkap untuk {symbol}.")
                    continue

                price = df['close'].iloc[-1]
                ema20 = df['ema20'].iloc[-1]
                ema50 = df['ema50'].iloc[-1]
                ema200 = df['ema200'].iloc[-1]
                rsi = df['rsi'].iloc[-1]
                macd_hist = df['macd_histogram'].iloc[-1]

                trend_up = price > ema200
                trend_down = price < ema200

                buy_condition = (
                    trend_up and
                    ema20 > ema50 and
                    price > ema20 and
                    rsi < self.rsi_oversold and
                    macd_hist > 0
                )

                sell_condition = (
                    trend_down and
                    ema20 < ema50 and
                    price < ema20 and
                    rsi > self.rsi_overbought and
                    macd_hist < 0
                )

                if buy_condition:
                    signals[symbol] = {
                        "strategy_signal": "BUY",
                        "tags": ["EMA Pullback", "Trend Up", "RSI Support", "MACD Bullish"]
                    }
                elif sell_condition:
                    signals[symbol] = {
                        "strategy_signal": "SELL",
                        "tags": ["EMA Pullback", "Trend Down", "RSI Resistance", "MACD Bearish"]
                    }

            except Exception as e:
                self.logger.error(f"Error {symbol}: {str(e)}")

        return signals