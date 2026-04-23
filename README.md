# 🧠 AlgoSensei — Adaptive DSA Tutor

**Stop looking up answers. Start building intuition.**

AlgoSensei gives you calibrated Socratic hints for 175+ DSA problems — guiding you toward the insight without handing you the answer. The leakage gate architecturally prevents direct answer reveals, even if you ask directly.

🚀 **[Try Live Demo](https://adityaamitra-algosensei.hf.space)** · 🌐 **[Website](https://adityaamitra.github.io/AlgoSensei-GenAI/)** · 📄 **[Technical Report](AlgoSensei_Technical_Report.pdf)**

---

## The Problem

You're stuck on a LeetCode problem at 11 PM. You have two options: keep suffering, or look up the solution, skim it, tell yourself you understand it, and move on.

Every DSA prep tool either solves the problem for you or gives vague encouragement. AlgoSensei does neither — it gives you the minimum hint needed to make progress. And it's architecturally enforced: the system cannot give a direct answer even if you explicitly ask for one.

---

## Features

| Feature | Description |
|---|---|
| 💡 **3-Level Hints** | Direction → Structure → Near-solution. Never names the algorithm. |
| 💻 **Code Analysis** | Paste your attempt. Get a targeted hint about your specific bottleneck. |
| 📸 **Screenshot → Session** | Upload a LeetCode screenshot. Auto-detects problem, starts full tutoring session. |
| 📖 **Concept Explainer** | RAG-grounded explanations with real-world analogies and knowledge citations. |
| 🔊 **Audio Output** | Listen button on every hint via Web Speech API. |
| 👤 **User Accounts** | Track progress across 175+ problems with a personal dashboard. |
| 🛡️ **Leakage Gate** | Two-stage safety check (regex + semantic) on every response. Verified 0% leakage. |
| 🧠 **Context Memory** | Each hint builds on previous ones — progressively guides without repeating. |

---

## Generative AI Components

| Component | Technology | What it does |
|---|---|---|
| **RAG** | Qdrant Cloud + all-MiniLM-L6-v2 | 49 KB chunks across 14 DSA patterns, retrieved per query |
| **Prompt Engineering** | OpenAI / OpenRouter | 3 system prompts + leakage gate + calibrated hint levels |
| **Multimodal** | pytesseract + Web Speech API | Screenshot → OCR → pattern detection + audio output |
| **Synthetic Data** | Auto-generated JSONL | 110 evaluation pairs across 22 problems × 5 interaction types |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/adityaamitra/AlgoSensei-GenAI
cd AlgoSensei-GenAI/algosensei_genai

# 2. Install
pip install -r requirements.txt

# 3. Install Tesseract OCR (macOS)
brew install tesseract

# 4. Add API keys
cp .env.example .env
# Fill in: OPENROUTER_API_KEY, QDRANT_URL, QDRANT_API_KEY

# 5. Build knowledge base (one-time, ~2 min)
python scripts/setup_qdrant.py

# 6. Launch
uvicorn main:app --reload --port 8000
```

Open:
- `http://localhost:8000` — landing page
- `http://localhost:8000/tutor` — tutor app
- `http://localhost:8000/signup` — create account
- `http://localhost:8000/dashboard` — progress dashboard

---

## Environment Variables

```bash
# Required
OPENROUTER_API_KEY=sk-or-v1-your-key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-key
JWT_SECRET=any-random-string

# Optional — use OpenAI instead of OpenRouter
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4o-mini

# Optional — override default model
OPENROUTER_MODEL=nvidia/llama-3.1-nemotron-ultra-253b-v1:free
```

---

## Project Structure

```
algosensei_genai/
├── main.py                    ← FastAPI backend
├── config.py                  ← Configuration
├── requirements.txt
├── Dockerfile                 ← HF Spaces Docker deployment
│
├── static/                    ← Frontend
│   ├── index.html             ← Landing page
│   ├── tutor.html             ← Tutor app
│   ├── login.html             ← Sign in
│   ├── signup.html            ← Create account
│   ├── dashboard.html         ← Progress dashboard
│   └── style.css              ← Shared styles
│
├── auth/                      ← Authentication
│   ├── database.py            ← SQLite (users, progress, hint history)
│   ├── security.py            ← PBKDF2 password hashing + JWT tokens
│   └── routes.py              ← /api/auth/* endpoints
│
├── engine/                    ← AI Engine
│   ├── gemini_client.py       ← LLM client (OpenAI/OpenRouter)
│   ├── leakage_gate.py        ← Two-stage safety checker
│   └── tutor.py               ← TutoringSession + AlgoSenseiEngine
│
├── rag/                       ← Retrieval-Augmented Generation
│   ├── embedder.py            ← all-MiniLM-L6-v2 (local)
│   ├── vector_store.py        ← Qdrant REST API (no grpcio)
│   └── retriever.py           ← Retrieval + faithfulness scoring
│
├── knowledge/
│   ├── blind75_kb.py          ← 49 DSA knowledge chunks
│   └── problem_db.py          ← 175 problems (Blind75 + NeetCode150 + Grind169)
│
├── prompts/
│   └── templates.py           ← All LLM prompt templates
│
└── web/
    └── index.html             ← GitHub Pages landing page
```

---

## Evaluation Metrics

| Metric | Target | Description |
|---|---|---|
| Retrieval Recall @4 | >90% | Correct concept in top 4 retrieved chunks |
| Hint Leakage Rate | <5% | Hints with direct solution reveals |
| Faithfulness Score | >95% | Hints grounded in retrieved context |
| Directional Accuracy | >85% | Hints pointing toward correct DSA pattern |

Run the evaluation suite:
```bash
python scripts/run_evaluation.py
```

---

## Tech Stack — Total Cost: $0

| Service | Usage | Cost |
|---|---|---|
| OpenRouter | LLM inference (free models) | $0 |
| Qdrant Cloud | Vector DB (free tier 1GB) | $0 |
| all-MiniLM-L6-v2 | Embeddings (local inference) | $0 |
| pytesseract | OCR (local) | $0 |
| Web Speech API | Audio output (browser-native) | $0 |
| Hugging Face Spaces | Hosting | $0 |
| GitHub Pages | Landing page | $0 |

---

## Problem Coverage

175 problems across 14 DSA patterns:

`Arrays & Hashing` · `Two Pointers` · `Sliding Window` · `Stack` · `Binary Search` · `Linked List` · `Trees` · `Tries` · `Heap/PQ` · `Backtracking` · `Graphs` · `DP 1D` · `DP 2D` · `Greedy`

Includes all **Blind 75**, **NeetCode 150**, and **Grind 169** problems with company tags (Google, Amazon, Meta, Microsoft, Apple).

---

## Deploying to Hugging Face Spaces

1. Create a new Space with **Docker SDK**
2. Upload all project files maintaining folder structure
3. Add Secrets: `OPENROUTER_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `JWT_SECRET`
4. The space builds and runs automatically on port 7860

Live at: **https://adityaamitra-algosensei.hf.space**

---

## Author

**Aditya Mitra**


[![GitHub](https://img.shields.io/badge/GitHub-adityaamitra-black?logo=github)](https://github.com/adityaamitra)
[![HF Space](https://img.shields.io/badge/🤗-Live%20Demo-yellow)](https://adityaamitra-algosensei.hf.space)