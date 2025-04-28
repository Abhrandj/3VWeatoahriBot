# core/report_generator.py

import os
import pandas as pd
from datetime import datetime
from core.telegram import send_telegram_message

PORTFOLIO_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "portfolio_closed.csv")


def generate_daily_report():
    if not os.path.exists(PORTFOLIO_CSV):
        return "File portfolio_closed.csv tidak ditemukan."

    try:
        df = pd.read_csv(PORTFOLIO_CSV)
        if df.empty:
            return "Data histori kosong."

        # Filter trade hari ini
        today = datetime.now().date()
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
        daily_df = df[df['timestamp'] == today]

        if daily_df.empty:
            return "Tidak ada trade hari ini."

        # Hitung metrik
        total_trades = len(daily_df)
        total_pnl = daily_df['pnl'].sum()
        avg_roi = daily_df['roi_percent'].mean()

        # Format pesan Telegram
        message = (
            f"📊 <b>Daily Report</b> - <code>{today}</code>\n"
            f"———————————————\n"
            f"🧾 Total Trades: <b>{total_trades}</b>\n"
            f"💰 Total PnL: <b>${round(total_pnl, 2)}</b>\n"
            f"📈 Avg ROI: <b>{round(avg_roi, 2)}%</b>\n"
        )

        # Kirim pesan
        send_telegram_message(message)
        return "Laporan harian berhasil dikirim ke Telegram."

    except Exception as e:
        return f"Terjadi error: {str(e)}"