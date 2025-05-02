# core/strategy_engine.py

from strategies.bb_breakout_strategy import BB_BreakoutStrategy
from strategies.ema_pullback_strategy import EMA_PullbackStrategy
from strategies.volume_spike_strategy import Volume_SpikeStrategy
from strategies.ema_bb_crossover_strategy import EMA_BB_CrossoverStrategy

class StrategyEngine:
    def __init__(self, symbols, get_data, get_ai_signal):
        self.symbols = symbols
        self.get_data = get_data
        self.get_ai_signal = get_ai_signal

        # Inisialisasi semua strategi
        self.strategies = [
            BB_BreakoutStrategy(self.symbols, self.get_data),
            EMA_PullbackStrategy(self.symbols, self.get_data),
            Volume_SpikeStrategy(self.symbols, self.get_data),
            EMA_BB_CrossoverStrategy(self.symbols, self.get_data, self.get_ai_signal)
        ]

    def evaluate_all(self):
        combined_signals = {}
        priority = {"BUY": 2, "SELL": 1, "HOLD": 0}

        for strategy in self.strategies:
            result = strategy.check_signals()

            if not result:
                print(f"[STRATEGY] {strategy.__class__.__name__} tidak menghasilkan sinyal.")

            for symbol, signal in result.items():
                action = signal.get("strategy_signal", "HOLD")
                tags = signal.get("tags", [])

                print(f"[STRATEGY DEBUG] {symbol} -> {action} | Tags: {tags}")

                if symbol not in combined_signals:
                    combined_signals[symbol] = {
                        "strategy_signal": action,
                        "tags": tags.copy()
                    }
                else:
                    current = combined_signals[symbol]["strategy_signal"]
                    if priority.get(action, 0) > priority.get(current, 0):
                        combined_signals[symbol]["strategy_signal"] = action
                    combined_signals[symbol]["tags"] += tags

        return combined_signals