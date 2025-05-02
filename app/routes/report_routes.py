# routes/report_routes.py

from flask import Blueprint, render_template
from core.report_generator import generate_daily_report

report_bp = Blueprint("report", __name__)

@report_bp.route("/send-daily-report")
def send_daily_report():
    result = generate_daily_report()
    return render_template("report_result.html", result=result)