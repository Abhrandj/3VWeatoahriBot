# strategies/bb_breakout_strategy.py

import logging
import pandas as pd
from typing import Dict, List, Callable
from core.utils import is_live_mode

class BB_BreakoutStrategy:
    """Strategi breakout Bollinger Bands dengan konfirmasi EMA200, RSI, dan MACD."""

    def __init__(
        self,
        symbols: List[str],
        get_data_func: Callable[[str], pd.DataFrame],
        ema_period: int = 200,
        rsi_oversold: float = 35,
        rsi_overbought: float = 65
    ):
        self.symbols = symbols
        self.get_data = get_data_func
        self.ema_period = ema_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.logger = logging.getLogger(__name__)

    def check_signals(self) -> Dict[str, Dict[str, str]]:
        signals = {}

        for symbol in self.symbols:
            try:
                df = self.get_data(symbol)
                if df is None or len(df) < 50:
                    self.logger.warning(f"[BB] Data tidak cukup untuk {symbol}")
                    continue

                required_cols = ['close', 'lower_band', 'upper_band', 'rsi', 'macd_histogram', 'ema200']
                if not all(col in df.columns for col in required_cols):
                    self.logger.warning(f"[BB] Kolom indikator tidak lengkap untuk {symbol}")
                    continue

                price = df['close'].iloc[-1]
                ema200 = df['ema200'].iloc[-1]
                lower = df['lower_band'].iloc[-1]
                upper = df['upper_band'].iloc[-1]
                rsi = df['rsi'].iloc[-1]
                macd_hist = df['macd_histogram'].iloc[-1]

                trend_up = price > ema200
                trend_down = price < ema200

                if not is_live_mode():
                    # MODE LATIHAN – lebih sensitif
                    self.logger.info(f"[BB DEBUG TEST] {symbol} | Price={price:.2f}, EMA200={ema200:.2f}, RSI={rsi:.2f}, MACD_Hist={macd_hist:.4f}")

                    if price <= lower and trend_up and macd_hist > -5:
                        signals[symbol] = {
                            "strategy_signal": "BUY",
                            "tags": ["TEST MODE", "BB Aggressive", "MACD > 0", "RSI < 60"]
                        }
                    elif price >= upper and trend_down and macd_hist < 5:
                        signals[symbol] = {
                            "strategy_signal": "SELL",
                            "tags": ["TEST MODE", "BB Aggressive", "MACD < 0", "RSI > 40"]
                        }
                else:
                    # MODE LIVE – konservatif
                    buy = (
                        price < lower and trend_up and
                        rsi < self.rsi_oversold and macd_hist > 0
                    )
                    sell = (
                        price > upper and trend_down and
                        rsi > self.rsi_overbought and macd_hist < 0
                    )

                    if buy:
                        signals[symbol] = {
                            "strategy_signal": "BUY",
                            "tags": ["BB Breakout", "Trend Up", "RSI Oversold", "MACD Confirm"]
                        }
                    elif sell:
                        signals[symbol] = {
                            "strategy_signal": "SELL",
                            "tags": ["BB Breakout", "Trend Down", "RSI Overbought", "MACD Confirm"]
                        }

            except Exception as e:
                self.logger.error(f"[BB ERROR] {symbol} gagal diproses: {str(e)}")

        return signals