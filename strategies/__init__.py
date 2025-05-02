from strategies.bb_breakout_strategy import BB_BreakoutStrategy
from strategies.ema_pullback_strategy import EMA_PullbackStrategy
from strategies.volume_spike_strategy import Volume_SpikeStrategy
from strategies.ema_bb_crossover_strategy import EMA_BB_CrossoverStrategy

class StrategyEngine:
    def __init__(self, symbols, get_data, get_ai_signal):
        self.strategies = [
            BB_BreakoutStrategy(symbols, get_data),
            EMA_PullbackStrategy(symbols, get_data),
            Volume_SpikeStrategy(symbols, get_data),
            EMA_BB_CrossoverStrategy(symbols, get_data, get_ai_signal)
        ]

    def evaluate_all(self):
        combined_signals = {}

        for strategy in self.strategies:
            result = strategy.check_signals()
            for symbol, signal in result.items():
                if symbol not in combined_signals:
                    combined_signals[symbol] = {"strategy_signal": None, "tags": []}
                combined_signals[symbol]["strategy_signal"] = signal["strategy_signal"]
                combined_signals[symbol]["tags"] += signal["tags"]

        return combined_signals