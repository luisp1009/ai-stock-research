from datetime import date, datetime
from flask import Flask, render_template
from config import Config
from models import db, DailyReport
from ai_writer import generate_market_report

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
        existing.title = f"Daily Market Research - {today}"
        existing.slug = f"daily-market-research-{today}"
        existing.market_summary = (
            "The market showed mixed action today. Technology remained strong, "
            "financials were steady, and traders focused on momentum names with "
            "above-average volume."
        )
        existing.full_html = """
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
        """
        existing.status = "published"
        existing.published_at = datetime.utcnow()

        db.session.commit()
        return f"Test report updated for {today}"

    report = DailyReport(
        report_date=today,
        title=f"Daily Market Research - {today}",
        slug=f"daily-market-research-{today}",
        market_summary=(
            "The market showed mixed action today. Technology remained strong, "
            "financials were steady, and traders focused on momentum names with "
            "above-average volume."
        ),
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


@app.route("/generate-ai-report")
def generate_ai_report():
    today = date.today()

    structured_data = {
        "market_tone": "Mixed trading with strength in technology and selective momentum names.",
        "market_overview": {
            "sp500": "Mixed",
            "nasdaq": "Stronger",
            "dow": "Flat to slightly weaker",
            "sector_leadership": ["Technology", "Semiconductors"],
            "sector_weakness": ["Defensive names", "Rate-sensitive areas"]
        },
        "top_stocks": [
            {
                "ticker": "NVDA",
                "reason": "Sector leadership, strong momentum, and continued trader interest"
            },
            {
                "ticker": "MSFT",
                "reason": "Steady uptrend and institutional support"
            },
            {
                "ticker": "AMD",
                "reason": "Relative strength and elevated attention in the semiconductor group"
            }
        ],
        "risk_notes": [
            "Some leadership names appear extended after recent gains.",
            "Volatility may rise around macroeconomic news and rate expectations.",
            "Momentum setups can fail quickly if the broader market weakens."
        ]
    }

    try:
        ai_report = generate_market_report(structured_data)

        existing = DailyReport.query.filter_by(report_date=today).first()

        if existing:
            existing.title = ai_report["title"]
            existing.slug = f"daily-market-research-{today}"
            existing.market_summary = ai_report["market_summary"]
            existing.full_html = ai_report["full_html"]
            existing.status = "published"
            existing.published_at = datetime.utcnow()

            db.session.commit()
            return f"AI report updated for {today}"

        report = DailyReport(
            report_date=today,
            title=ai_report["title"],
            slug=f"daily-market-research-{today}",
            market_summary=ai_report["market_summary"],
            full_html=ai_report["full_html"],
            status="published",
            published_at=datetime.utcnow()
        )

        db.session.add(report)
        db.session.commit()

        return f"AI report created for {today}"

    except Exception as e:
        return f"Error generating AI report: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)