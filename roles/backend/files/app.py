from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sqlite3
from datetime import datetime

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

DB_PATH = "/var/www/ai_project/ai.db"

# Ensure DB + table
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            summary TEXT,
            sentiment TEXT,
            sentiment_score REAL,
            keywords TEXT,
            created_at TEXT
        );
    """)
    conn.commit()
    conn.close()

init_db()

def extract_keywords(text):
    words = text.split()
    return [w for w in words if len(w) > 4]

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    sentiment_scores = analyzer.polarity_scores(text)
    sentiment_score = sentiment_scores["compound"]
    sentiment = ("positive" if sentiment_score > 0
                 else "negative" if sentiment_score < 0
                 else "neutral")

    keywords = extract_keywords(text)
    summary = text[:200]

    created_at = datetime.utcnow().isoformat()

    # Save into DB
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO analysis (text, summary, sentiment, sentiment_score, keywords, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (text, summary, sentiment, sentiment_score, ", ".join(keywords), created_at)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "text": text,
        "summary": summary,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "keywords": keywords,
        "created_at": created_at
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

