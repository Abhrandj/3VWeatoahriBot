import csv
from datetime import datetime

class Portfolio:
    def __init__(self):
        self.positions = {}  # {symbol: {...}}
        self.closed = []     # list of closed positions

    def open_position(self, symbol, side, entry_price):
        self.positions[symbol] = {
            "symbol": symbol,
            "side": side,
            "entry": entry_price,
            "trailing": entry_price,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }

    def update_trailing(self, symbol, current_price):
        pos = self.positions.get(symbol)
        if not pos:
            return
        if pos["side"] == "BUY":
            pos["trailing"] = max(pos["trailing"], current_price)
        elif pos["side"] == "SELL":
            pos["trailing"] = min(pos["trailing"], current_price)

    def check_exit(self, symbol, current_price, buffer_pct=0.005):
        pos = self.positions.get(symbol)
        if not pos:
            return False
        buffer = pos["trailing"] * buffer_pct
        if pos["side"] == "BUY" and current_price < pos["trailing"] - buffer:
            return True
        if pos["side"] == "SELL" and current_price > pos["trailing"] + buffer:
            return True
        return False

    def close_position(self, symbol, price_now=None):
        if symbol in self.positions:
            pos = self.positions[symbol]
            closed_pos = pos.copy()
            closed_pos["closed_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            closed_pos["close_price"] = price_now or pos["trailing"]
            closed_pos["roi"] = ((closed_pos["close_price"] - pos["entry"]) / pos["entry"] * 100) \
                if pos["side"] == "BUY" else ((pos["entry"] - closed_pos["close_price"]) / pos["entry"] * 100)
            self.closed.append(closed_pos)
            del self.positions[symbol]

    def get_all(self):
        return self.positions

    def get_open_positions(self):
        return self.get_all()

    def get_closed(self):
        return self.closed

    def export_to_csv(self, path="flask_app/static/portfolio.csv", current_prices=None):
        try:
            with open(path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Symbol", "Side", "Entry", "Current", "ROI (%)", "Trailing", "Opened At"])
                for symbol, data in self.positions.items():
                    current = current_prices.get(symbol, 0) if current_prices else 0
                    roi = ((current - data["entry"]) / data["entry"] * 100) if data["side"] == "BUY" \
                          else ((data["entry"] - current) / data["entry"] * 100)
                    writer.writerow([
                        symbol,
                        data["side"],
                        data["entry"],
                        current,
                        round(roi, 2),
                        round(data["trailing"], 2),
                        data["timestamp"]
                    ])
            return path
        except Exception as e:
            print(f"[Portfolio CSV] Export gagal: {e}")
            return None

    def export_history_to_csv(self, path="flask_app/static/portfolio_history.csv"):
        try:
            with open(path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Symbol", "Side", "Entry", "Close Price", "ROI (%)", "Opened", "Closed"])
                for row in self.closed:
                    writer.writerow([
                        row.get("symbol", "-"),
                        row["side"],
                        row["entry"],
                        row["close_price"],
                        round(row["roi"], 2),
                        row["timestamp"],
                        row["closed_at"]
                    ])
            return path
        except Exception as e:
            print(f"[Export History CSV] Failed: {e}")
            return None