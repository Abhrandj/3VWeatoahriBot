import pandas as pd
import numpy as np
import time
from strategies.bb_breakout_strategy import BB_BreakoutStrategy
from strategies.ema_pullback_strategy import EMA_PullbackStrategy
from strategies.volume_spike_strategy import Volume_SpikeStrategy
from strategies.ema_bb_crossover_strategy import EMA_BB_CrossoverStrategy

class RiskManager:
    def __init__(self, max_risk_per_trade=0.02, account_balance=1000):
        self.max_risk_per_trade = max_risk_per_trade
        self.account_balance = account_balance

    def calculate_position_size(self, stop_loss_distance):
        if stop_loss_distance <= 0:
            return 0
        risk_amount = self.account_balance * self.max_risk_per_trade
        return round(risk_amount / stop_loss_distance, 2)

    def update_account_balance(self, new_balance):
        self.account_balance = new_balance

    def calculate_stop_loss(self, current_price, sl_percentage=0.01):
        return round(current_price * (1 - sl_percentage), 2)

    def calculate_take_profit(self, current_price, tp_percentage=0.01):
        return round(current_price * (1 + tp_percentage), 2)

def calculate_ema(prices, period=10):
    return pd.Series(prices).ewm(span=period, adjust=False).mean().values

def calculate_rsi(prices, period=14):
    prices = pd.Series(prices)
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.values

def calculate_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    macd = ema_fast - ema_slow
    signal_line = calculate_ema(macd, signal)
    histogram = macd - signal_line
    return macd, signal_line, histogram

def apply_indicators(df):
    df['ema_20'] = calculate_ema(df['close'], 20)
    df['ema_50'] = calculate_ema(df['close'], 50)
    df['ma_200'] = df['close'].rolling(window=200).mean()
    df['rsi'] = calculate_rsi(df['close'], 14)
    df['macd'], df['macd_signal'], df['macd_hist'] = calculate_macd(df['close'])
    df['upper_bb'] = df['close'].rolling(window=20).mean() + 2 * df['close'].rolling(window=20).std()
    df['lower_bb'] = df['close'].rolling(window=20).mean() - 2 * df['close'].rolling(window=20).std()
    return df

class BacktestEngine:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.initial_balance = 1000
        self.trade_log = []

    def run(self):
        start_time = time.time()
        df = pd.read_csv(self.csv_path)
        df = apply_indicators(df)

        balance = self.initial_balance
        risk_manager = RiskManager(account_balance=balance)
        position = None
        entry_price = 0
        stop_loss = 0
        take_profit = 0

        # Inisialisasi strategi baru
        bb_strategy = BB_BreakoutStrategy(['TEST'], lambda _: df)
        ema_pullback = EMA_PullbackStrategy(['TEST'], lambda _: df)
        volume_spike = Volume_SpikeStrategy(['TEST'], lambda _: df)
        ema_bb_cross = EMA_BB_CrossoverStrategy(['TEST'], lambda _: df, lambda _: "BUY")

        for i in range(50, len(df)):
            current_df = df.iloc[:i+1]

            price = current_df['close'].iloc[-1]
            if current_df.isnull().any().any():
                continue

            # Simulasi AI signal (sederhana)
            ai_signal = "BUY" if current_df['rsi'].iloc[-1] < 50 else "SELL"

            # Update AI signal untuk EMA+BB crossover
            ema_bb_cross.get_ai_signal = lambda _: ai_signal

            # Dapatkan tags dari semua strategi
            bb_tags = bb_strategy.check_signals().get('TEST', {}).get('tags', [])
            ema_tags = ema_pullback.check_signals().get('TEST', {}).get('tags', [])
            vol_tags = volume_spike.check_signals().get('TEST', {}).get('tags', [])
            cross_tags = ema_bb_cross.check_signals().get('TEST', {}).get('tags', [])

            tags = bb_tags + ema_tags + vol_tags + cross_tags

            if position is None:
                if any(tag.endswith("BUY") for tag in tags):
                    entry_price = price
                    stop_loss = risk_manager.calculate_stop_loss(price)
                    take_profit = risk_manager.calculate_take_profit(price)
                    position = 'long'
                    self.trade_log.append(f"BUY at {price:.2f} | Tags: {tags}")
            elif position == 'long':
                if price <= stop_loss or price >= take_profit or any(tag.endswith("SELL") for tag in tags):
                    pnl = (price - entry_price)
                    balance += pnl
                    risk_manager.update_account_balance(balance)
                    self.trade_log.append(f"SELL at {price:.2f} | PnL: {pnl:.2f} | Tags: {tags}")
                    position = None

        final_pnl = balance - self.initial_balance
        end_time = time.time()

        return {
            "initial_balance": self.initial_balance,
            "final_balance": round(balance, 2),
            "profit": round(final_pnl, 2),
            "trades": self.trade_log,
            "duration": round(end_time - start_time, 2)
        }

def run_backtest(csv_path):
    engine = BacktestEngine(csv_path)
    return engine.run()