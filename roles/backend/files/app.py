from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from database import get_db, init_db

app = Flask(__name__)
CORS(app)

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound > 0.25:
        label = "positive"
    elif compound < -0.25:
        label = "negative"
    else:
        label = "neutral"

    return label, float(round(compound, 2))


def summarize(text: str) -> str:
    if len(text) <= 140:
        return text
    cut = text[:140].rsplit(" ", 1)[0]
    return cut + "..."


def extract_keywords(text: str):
    tokens = [
        w.lower()
        for w in text.split()
        if len(w) > 4 and w.isalpha()
    ]
    freq = {}
    for w in tokens:
        freq[w] = freq.get(w, 0) + 1

    sorted_kw = sorted(freq, key=freq.get, reverse=True)
    return sorted_kw[:6]


@app.before_first_request
def setup_db():
    init_db()


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Text is required"}), 400

    mode = data.get("mode") or "default"

    sentiment, score = analyze_sentiment(text)
    summary = summarize(text) if mode in ("default", "summary") else ""
    keywords = extract_keywords(text) if mode in ("default", "keywords") else []

    created_at = datetime.utcnow().isoformat()

    conn = get_db()
    conn.execute(
        """
        INSERT INTO analysis (text, summary, sentiment, sentiment_score, keywords, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (text, summary, sentiment, score, ",".join(keywords), created_at),
    )
    conn.commit()
    conn.close()

    return jsonify(
        {
            "summary": summary,
            "sentiment": sentiment,
            "sentiment_score": score,
            "keywords": keywords,
            "created_at": created_at,
        }
    )


@app.route("/api/recent", methods=["GET"])
def api_recent():
    limit = 10

    conn = get_db()
    cur = conn.execute(
        """
        SELECT text, summary, sentiment, sentiment_score, keywords, created_at
        FROM analysis
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        items.append(
            {
                "text": r["text"],
                "summary": r["summary"],
                "sentiment": r["sentiment"],
                "sentiment_score": r["sentiment_score"],
                "keywords": (r["keywords"] or "").split(",")
                if r["keywords"]
                else [],
                "created_at": r["created_at"],
            }
        )

    return jsonify(items)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

