from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
from database import get_db, init_db

app = Flask(__name__)

# ------------------------------
# BASIC RULE-BASED AI LOGIC
# ------------------------------

positive_words = ["good", "great", "excellent", "happy", "amazing", "love"]
negative_words = ["bad", "terrible", "sad", "hate", "awful", "problem"]

def analyze_sentiment(text):
    t = text.lower()
    score = 0

    for w in positive_words:
        score += t.count(w)

    for w in negative_words:
        score -= t.count(w)

    if score > 1:
        return "positive", min(1.0, score / 5)
    elif score < -1:
        return "negative", max(-1.0, score / 5)
    else:
        return "neutral", 0.0

def summarize(text):
    if len(text) < 120:
        return text
    return text[:120].rsplit(" ", 1)[0] + "..."

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


# ------------------------------
# API ENDPOINT
# ------------------------------

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text required"}), 400

    sentiment, score = analyze_sentiment(text)
    summary = summarize(text)
    keywords = extract_keywords(text)

    # Save to DB
    conn = get_db()
    conn.execute(
        "INSERT INTO analysis (text, summary, sentiment, sentiment_score, keywords) VALUES (?,?,?,?,?)",
        (text, summary, sentiment, score, ",".join(keywords)),
    )
    conn.commit()

    return jsonify({
        "summary": summary,
        "sentiment": sentiment,
        "sentiment_score": score,
        "keywords": keywords,
        "created_at": datetime.utcnow().isoformat(),
    })


# ------------------------------
# APP STARTUP
# ------------------------------

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

