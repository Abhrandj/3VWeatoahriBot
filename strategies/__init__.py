from .ema_bb_strategy import ema_bb_strategy
from .bb_breakout_strategy import bb_breakout_strategy
from .volume_spike_strategy import volume_spike_strategy

def run_all_strategies(df, ai_signal):
    tags = []
    tags += ema_bb_strategy(df, ai_signal)
    tags += bb_breakout_strategy(df)
    tags += volume_spike_strategy(df)
    return tags