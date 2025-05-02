# core/report_generator.py

from datetime import datetime
from core.telegram import send_telegram_message

def generate_daily_report(portfolio):
    """
    Kirim laporan harian ke Telegram berdasarkan posisi yang sudah tertutup hari ini.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    closed = portfolio.get_closed()

    # Filter posisi yang ditutup hari ini
    trades_today = [
        t for t in closed
        if str(t.get("closed_at", "")).startswith(today)
    ]

    if not trades_today:
        message = f"[DAILY REPORT] {today}\nNo trades closed today."
        send_telegram_message(message)
        return message

    # Hitung total ROI dan PnL
    total_roi = sum(t.get("roi", 0) for t in trades_today)
    total_pnl = sum(t.get("pnl", 0) for t in trades_today)
    total_roi = round(total_roi, 2)
    total_pnl = round(total_pnl, 2)

    # Trade terbaik dan terburuk
    best = max(trades_today, key=lambda t: t.get("roi", -999))
    worst = min(trades_today, key=lambda t: t.get("roi", 999))

    summary = (
        f"[DAILY REPORT] {today}\n"
        f"Closed Trades: {len(trades_today)}\n"
        f"Total PnL: {total_pnl:.2f} USDT\n"
        f"Total ROI: {total_roi:.2f}%\n"
        f"Best: {best.get('symbol', '-')} {best.get('roi', 0):.2f}%\n"
        f"Worst: {worst.get('symbol', '-')} {worst.get('roi', 0):.2f}%"
    )

    send_telegram_message(summary)
    return "[Daily Report] Terkirim ke Telegram."