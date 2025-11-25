const inputText = document.getElementById("inputText");
const modeSelect = document.getElementById("modeSelect");
const analyzeBtn = document.getElementById("analyzeBtn");
const statusMessage = document.getElementById("statusMessage");

const summaryOutput = document.getElementById("summaryOutput");
const sentimentLabel = document.getElementById("sentimentLabel");
const sentimentDetails = document.getElementById("sentimentDetails");
const sentimentBarFill = document.getElementById("sentimentBarFill");
const keywordsOutput = document.getElementById("keywordsOutput");
const historyList = document.getElementById("historyList");

const historyMax = 6;
const useMockIfApiFails = false;

analyzeBtn.addEventListener("click", async () => {
  const text = inputText.value.trim();
  const mode = modeSelect.value || "default";

  if (!text) {
    statusMessage.textContent =
      "Please enter some text before running analysis.";
    return;
  }

  setLoading(true);
  statusMessage.textContent = "Analyzing text...";

  try {
    const result = await analyzeText(text, mode);
    renderResult(text, result);
    prependHistoryItem(text, result);
    statusMessage.textContent = "Analysis completed.";
  } catch (err) {
    console.error("Analysis failed:", err);
    statusMessage.textContent =
      "Analysis failed. Please try again in a moment.";
  } finally {
    setLoading(false);
  }
});

window.addEventListener("load", () => {
  loadRecentHistory();
});

function setLoading(isLoading) {
  if (isLoading) {
    analyzeBtn.classList.add("loading");
    analyzeBtn.disabled = true;
  } else {
    analyzeBtn.classList.remove("loading");
    analyzeBtn.disabled = false;
  }
}

async function analyzeText(text, mode) {
  const payload = { text, mode };

  const response = await fetch("/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`HTTP error ${response.status}`);
  }

  const data = await response.json();
  return normalizeResult(data);
}

function normalizeResult(data) {
  return {
    summary: data.summary || "",
    sentiment: data.sentiment || "neutral",
    sentiment_score:
      typeof data.sentiment_score === "number" ? data.sentiment_score : 0,
    keywords: Array.isArray(data.keywords) ? data.keywords : [],
    created_at: data.created_at || new Date().toISOString(),
  };
}

function renderResult(inputTextValue, result) {
  summaryOutput.classList.remove("placeholder");
  summaryOutput.textContent =
    result.summary && result.summary.trim().length > 0
      ? result.summary
      : "No summary could be generated for this text.";

  const score = result.sentiment_score || 0;
  const sentimentClass = result.sentiment || "neutral";

  sentimentLabel.classList.remove("positive", "negative", "neutral");
  sentimentBarFill.classList.remove("positive", "negative", "neutral");

  sentimentLabel.classList.add(sentimentClass);
  sentimentBarFill.classList.add(sentimentClass);

  sentimentLabel.textContent = `${capitalize(sentimentClass)} · ${score.toFixed(
    2
  )}`;

  const absScore = Math.min(1, Math.max(0, Math.abs(score)));
  sentimentBarFill.style.width = `${absScore * 100}%`;

  if (sentimentClass === "positive") {
    sentimentDetails.textContent =
      "The text appears mainly positive. The content suggests a constructive or optimistic tone.";
  } else if (sentimentClass === "negative") {
    sentimentDetails.textContent =
      "The text contains more negative or critical signals. The overall tone is likely skeptical or dissatisfied.";
  } else {
    sentimentDetails.textContent =
      "The text is generally neutral or balanced in tone, without strong emotional polarity.";
  }

  keywordsOutput.innerHTML = "";
  if (result.keywords && result.keywords.length > 0) {
    result.keywords.forEach((kw) => {
      const span = document.createElement("span");
      span.className = "keyword-pill";
      span.textContent = kw;
      keywordsOutput.appendChild(span);
    });
  } else {
    const span = document.createElement("span");
    span.className = "keyword-pill keyword-pill-muted";
    span.textContent = "No significant keywords detected";
    keywordsOutput.appendChild(span);
  }
}

async function loadRecentHistory() {
  try {
    const response = await fetch("/api/recent");
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const items = await response.json();
    historyList.innerHTML = "";

    if (!items.length) {
      const p = document.createElement("p");
      p.className = "placeholder";
      p.textContent =
        "Once you start analyzing text, the last few entries will appear here.";
      historyList.appendChild(p);
      return;
    }

    items.forEach((item) => {
      prependHistoryItem(item.text, normalizeResult(item), false);
    });
  } catch (err) {
    console.error("Failed to load recent history:", err);
  }
}

function prependHistoryItem(text, result, prepend = true) {
  const item = document.createElement("div");
  item.className = "history-item";

  const time = new Date(result.created_at || Date.now());
  const timeStr = time.toLocaleTimeString(undefined, {
    hour: "2-digit",
    minute: "2-digit",
  });

  const preview = document.createElement("span");
  preview.className = "history-item-text";
  preview.textContent = text.replace(/\s+/g, " ").trim().slice(0, 60);
  if (text.length > 60) preview.textContent += "...";

  const meta = document.createElement("span");
  meta.textContent = `${capitalize(
    result.sentiment || "neutral"
  )} · ${timeStr}`;

  item.appendChild(preview);
  item.appendChild(meta);

  if (historyList.querySelector(".placeholder")) {
    historyList.innerHTML = "";
  }

  if (prepend) {
    historyList.prepend(item);
  } else {
    historyList.appendChild(item);
  }

  const items = historyList.querySelectorAll(".history-item");
  if (items.length > historyMax) {
    items[items.length - 1].remove();
  }
}

function capitalize(str) {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1);
}

