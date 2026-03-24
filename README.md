# Influencer Marketing Analytics Pipeline

## The business problem

A brand spends £500k on influencer partnerships this year. At the end of the year, their CMO asks: which of those partnerships actually moved the needle?

Most marketing teams can't answer that question. Not because the data doesn't exist, but because nobody built the right system to ask it.

This pipeline answers that question. It tells a brand not just whether sponsorships work but also which type of creator, which disclosure strategy, and which audience segment drives real business outcomes. And critically, when the data is telling you something is going wrong before it becomes a crisis.

---

## What the system found

Four distinct creator segments, each requiring a completely different campaign strategy:

| Segment | Profile | Engagement | Sentiment | Growth | Strategy |
|---------|---------|-----------|-----------|--------|----------|
| **Trust-builders** | Lifestyle, organic blend | High | Highest (0.907) | 0.5%/day | Prioritise alignment over volume |
| **Transparency performers** | Tech-Micro, explicit | Highest (14.5%) | 0.836 | 0.4%/day | Explicit disclosure is the strategy |
| **Diminishing returns** | Tech-Macro, implicit | Lowest (3.3%) | Lowest (0.772) | 0.1%/day | Avoid - hidden sponsorship backfires at scale |
| **Consistency segment** | Mixed | Moderate | Moderate | 0.25%/day | Optimise for reliability, not peak metrics |

**The headline finding:** There is no one-size-fits-all model for influencer marketing. Using the wrong strategy in the wrong segment doesn't just waste budget — it actively destroys audience trust.

**The honest causal finding:** A matched OLS model shows +1.45pp engagement lift from sponsorship. But once creator identity and time are controlled via two-way fixed effects, that effect disappears (β=−0.0007, p=0.878). Sponsorship alone does not drive engagement. Creator-audience trust, brand fit, and content quality do.

---

## Pipeline architecture

```
YouTube Data API v3
        │
        ▼
01_data_collection_eda.ipynb
   • 1,193 videos, 55,000+ comments
   • 30 creators: Tech + Lifestyle, Nano/Micro/Macro
   • 3 relational layers unified at video level
        │
        ▼
02_sponsorship_classification.ipynb
   • Regex heuristic classifier → Organic / Implicit / Explicit
   • Validated against 100 manually labelled videos
        │
        ▼
03_sentiment_analysis.ipynb
   • RoBERTa (cardiffnlp/twitter-roberta-base-sentiment-latest)
   • 55,000+ comments scored in batches of 64
   • Validated against 200 manually labelled comments
        │
        ▼
04_causal_inference.ipynb
   • PSM (Mahalanobis distance) → balanced matched groups
   • Matched OLS DiD → average treatment effect
   • Two-way fixed effects (creator + month FE)
   • Size × Sponsorship and Genre × Sponsorship interactions
   • Event study ±4 weeks → temporal shape of audience reaction
        │
        ▼
05_clustering_shap.ipynb
   • PCA (14 components → 90% variance)
   • Hierarchical clustering → validates K
   • K-Means (K=4, silhouette=0.251)
   • Random Forest + SHAP per cluster per target metric
```

---

## Why each design decision was made

**PSM over naive regression:** Sponsorship is not randomly assigned. Creators with growing audiences self-select into more sponsorships. A naive regression would conflate selection bias with treatment effect and give the wrong answer.

**RoBERTa over VADER:** YouTube comments use slang, sarcasm, and platform-specific language. VADER (keyword-based) fails on contextual sentiment. RoBERTa is trained on social media text and validated against manual labels.

**SHAP per cluster:** The drivers of performance are different in each segment. Running SHAP globally would average out the signal. Running it within each cluster reveals what actually matters for each creator type.

---

## Getting started

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/influencer-analytics.git
cd influencer-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up API keys
cp .env.example .env
# Edit .env and add your YouTube API key
# YOUTUBE_API_KEY=your_key_here

# 4. Add your data
# Place your CSV files in the data/ folder
# See data/sample/ for the expected schema

# 5. Run notebooks in order
jupyter lab
```

---

## Data schema

**channels_data_2024_2025.csv**: channel-level metadata (channelId, name, genre, sizeCategory, subscriberCount, etc.)

**videos_data_2024_2025.csv**: video-level metadata (videoId, channelId, title, viewCount, likeCount, commentCount, duration, publishedAt, etc.)

**comments_data_2024_2025.csv**: comment-level data (videoId, commentText, commentLikeCount, commentPublishedAt)

See `data/sample/` for anonymised example rows showing the expected format.

---

## Future scope

The pipeline currently answers *what happened and why*. Three extensions would complete the system:

**AI-powered campaign recommendations**: take each cluster profile and generate a structured campaign brief using a generative AI layer. The brief would include disclosure strategy, posting cadence, expected sentiment trajectory, risk flags, and a measurement framework. The cluster profiles and prompt architecture are already designed; implementation requires a generative AI API connection.

**Live sentiment monitoring**: a scheduled pipeline that pulls new YouTube comments weekly, scores sentiment using the same RoBERTa model, and triggers an alert when a creator's post-sponsorship sentiment drops below threshold. This closes the loop from insight to real-time brand risk management.

**Marketing Mix Modelling integration**: connect creator-level performance signals to channel-level budget attribution. The causal inference framework already established here transfers directly to MMM; the extension would answer how much of total marketing revenue is attributable to influencer spend versus paid search, email, and organic.

---

## Tech stack

Python · Pandas · RoBERTa (HuggingFace Transformers) · statsmodels · scikit-learn · SHAP · YouTube Data API v3

---

## About this project

Built to answer a real business question that most marketing teams cannot: which creator partnerships actually drive outcomes, and why.

The analysis covers 30 YouTube creators, 1,193 videos, and 55,000+ audience comments over 12 months across Tech and Lifestyle genres, Nano/Micro/Macro influencer tiers, and three sponsorship disclosure types.

The pipeline is designed to be modular and reusable where the same architecture applies to any platform where creator-brand dynamics generate measurable audience signals.