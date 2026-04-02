import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_market_report(structured_data):
    prompt = f"""
You are a professional stock market research analyst.

Generate a clean daily market report.

Return ONLY valid JSON with these keys:
- title
- market_summary
- full_html

Rules:
- Use a professional tone
- Do not guarantee outcomes
- Use "stocks to watch" language, not direct financial advice
- Include these sections in the HTML:
  - Market Overview
  - Top Stocks to Watch
  - Risk Notes

DATA:
{json.dumps(structured_data, indent=2)}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    text = response.output_text
    return json.loads(text)