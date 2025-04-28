# core/okx_trader.py

import time
from core.okx_sdk import OKXClient

okx = OKXClient()  # Optional: isi API key kalau mau akses private

def execute_trade(pair, direction, entry, sl, tp, size=1):
    side = "buy" if direction.upper() == "BUY" else "sell"
    order = okx.place_order(
        inst_id=pair,
        side=side,
        size=str(size),
        type="market"
    )
    time.sleep(1)
    return order
