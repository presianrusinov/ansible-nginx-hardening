from flask import Flask, request, jsonify
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from database import get_db, init_db

app = Flask(__name__)

# Initialize Vader (no nltk)
analyzer = SentimentIntensityAnalyzer()


# --------------------------
# Sentiment Analysis
# --------------------------
def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    score = scores["compound"]

    if score >= 0.05:
        sentiment = "positive"
    elif score <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return sentiment, score


# --------------------------
# Summary (simple rule)
# --------------------------
def summarize(text):
    if len(text) <= 120:
        return text
    return text[:120].rsplit(" ", 1)[0] + "..."


# --------------------------
# Keywords
# --------------------------
def extract_keywords(text):
    words = [
        w.lower() for w in text.split()
        if len(w) > 4 and w.isalpha()
    ]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    sorted_kw = sorted(freq, key=freq.get, reverse=True)
    return sorted_kw[:6]


# --------------------------
# API
# --------------------------
@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text required"}), 400

    sentiment, score = analyze_sentiment(text)
    summary = summarize(text)
    keywords = extract_keywords(text)

    # save to DB
    conn = get_db()
    conn.execute(
        "INSERT INTO analysis (text, summary, sentiment, sentiment_score, keywords) "
        "VALUES (?, ?, ?, ?, ?)",
        (text, summary, sentiment, score, ",".join(keywords)),
    )
    conn.commit()

    return jsonify({
        "summary": summary,
        "sentiment": sentiment,
        "sentiment_score": score,
        "keywords": keywords,
        "created_at": datetime.utcnow().isoformat()
    })


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

