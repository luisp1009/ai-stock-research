from datetime import date, datetime
from flask import Flask, render_template
from config import Config
from models import db, DailyReport

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    latest_report = (
        DailyReport.query
        .filter_by(status="published")
        .order_by(DailyReport.report_date.desc())
        .first()
    )
    return render_template("index.html", report=latest_report)

@app.route("/generate-test-report")
def generate_test_report():
    today = date.today()

    existing = DailyReport.query.filter_by(report_date=today).first()
    if existing:
        return f"Test report already exists for {today}"

    report = DailyReport(
        report_date=today,
        title=f"Daily Market Research - {today}",
        slug=f"daily-market-research-{today}",
        market_summary="The market showed mixed action today. Technology remained strong, financials were steady, and traders focused on momentum names with above-average volume.",
        full_html="""
        <h3>Market Overview</h3>
        <p>Stocks traded mixed with leadership in large-cap technology.</p>
        <h3>Top Stocks to Watch</h3>
        <ul>
            <li>NVDA - strong momentum and sector leadership</li>
            <li>MSFT - steady trend and institutional support</li>
            <li>AMD - elevated interest and relative strength</li>
        </ul>
        <h3>Risk Notes</h3>
        <p>Some names are extended and could be vulnerable to pullbacks.</p>
        """,
        status="published",
        published_at=datetime.utcnow()
    )

    db.session.add(report)
    db.session.commit()

    return f"Test report created for {today}"

if __name__ == "__main__":
    app.run(debug=True)