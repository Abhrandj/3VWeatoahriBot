# daily_report_runner.py

from core.bot_instance import bot
from core.report_generator import generate_daily_report

if __name__ == "__main__":
    generate_daily_report(bot.portfolio)