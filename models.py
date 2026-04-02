from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class DailyReport(db.Model):
    __tablename__ = "daily_reports"

    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, nullable=False, unique=True, default=date.today)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    market_summary = db.Column(db.Text, nullable=True)
    full_html = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="draft")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    published_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<DailyReport {self.report_date} - {self.title}>"