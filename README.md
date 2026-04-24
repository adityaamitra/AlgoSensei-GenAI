# 🧠 AlgoSensei

**The DSA tutor that guides you — without giving away the answer.**

AlgoSensei gives you calibrated Socratic hints for 175+ LeetCode problems. Instead of handing you the solution, it asks you the right questions until you arrive at the insight yourself. The leakage gate makes this architecturally enforced — the system cannot reveal the answer even if you ask directly.

🚀 **[Try it free](https://adityaamitra-algosensei.hf.space)** · 🌐 **[Website](https://adityaamitra.github.io/AlgoSensei-GenAI/)** · 🌐 **[Demo Video](https://youtu.be/DngHH4ujmcY)**

---

## Why AlgoSensei

Every DSA prep tool either solves the problem for you or gives vague encouragement. ChatGPT hands you the answer. Editorials walk you through the solution. There's no middle ground — until now.

AlgoSensei lives in the gap between *"I'm stuck"* and *"I looked up the answer."* It gives you the minimum hint needed to make progress, and it's enforced at the system level — not just a prompt instruction.

---

## Features

**💡 Three-level hints**
Direction → Structure → Near-solution. Each level gets one step closer without ever naming the algorithm or writing code. Every hint builds on the previous one.

**💻 Code analysis**
Paste your current attempt. AlgoSensei identifies exactly where your approach breaks down and asks one targeted question about it — not a generic observation, a question about your specific code.

**📸 Screenshot to session**
Upload any LeetCode problem screenshot. OCR reads the problem, detects the pattern, and starts a full tutoring session automatically.

**📖 Concept explainer**
Type any DSA concept. Get a grounded explanation with real-world analogies, complexity analysis, and a comprehension check — backed by a curated knowledge base.

**🔊 Audio output**
Every hint has a Listen button. Web Speech API reads it aloud so your eyes can stay on your code editor.

**👤 Progress tracking**
Create a free account. Track which problems you've solved, see your progress across 14 DSA patterns, and pick up where you left off.

**🛡️ Leakage gate**
Two-stage safety check on every response — regex for direct algorithm names, semantic check for subtle reveals. Verified 0% leakage rate across all hint levels.

---

## Getting Started

### Use the hosted version

**[https://adityaamitra-algosensei.hf.space](https://adityaamitra-algosensei.hf.space)**

No installation, no signup required. Create a free account to save progress.

### Run locally

**Prerequisites:** Python 3.11+, [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html), free accounts at [OpenRouter](https://openrouter.ai/keys) and [Qdrant Cloud](https://cloud.qdrant.io)

```bash
git clone https://github.com/adityaamitra/AlgoSensei-GenAI
cd AlgoSensei-GenAI/algosensei_genai

pip install -r requirements.txt

# macOS
brew install tesseract

cp .env.example .env
# Edit .env with your API keys

# One-time setup: builds the knowledge base in Qdrant (~2 min)
python scripts/setup_qdrant.py

uvicorn main:app --reload --port 8000
```

Open `http://localhost:8000`

---

## Configuration

```bash
# .env

# Required
OPENROUTER_API_KEY=sk-or-v1-...     # openrouter.ai/keys
QDRANT_URL=https://...              # cloud.qdrant.io
QDRANT_API_KEY=...
JWT_SECRET=any-long-random-string

# Optional: use OpenAI instead of OpenRouter
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Optional: override the default model
OPENROUTER_MODEL=nvidia/llama-3.1-nemotron-ultra-253b-v1:free
```

**Total cost to run: $0** — OpenRouter free tier, Qdrant free tier (1GB), local embeddings, local OCR.

---

## Problem Coverage

**175 problems** across **14 DSA patterns** — full Blind 75, NeetCode 150, and Grind 169 coverage with difficulty ratings and company tags.

| Pattern | Problems |
|---|---|
| Arrays & Hashing | 21 |
| Trees | 17 |
| Graphs | 17 |
| Dynamic Programming 1D | 16 |
| Linked List | 14 |
| Dynamic Programming 2D | 13 |
| Backtracking | 11 |
| Sliding Window | 9 |
| Heap / Priority Queue | 9 |
| Greedy | 9 |
| Stack | 10 |
| Binary Search | 8 |
| Two Pointers | 7 |
| Tries | 5 |

Company tags included: Google, Amazon, Meta, Microsoft, Apple, Bloomberg, LinkedIn, Uber.

---

## How it works

```
Your question / screenshot
        ↓
Mode detection (hint / explain / code analysis / screenshot)
        ↓
Query embedded locally (all-MiniLM-L6-v2, zero API cost)
        ↓
Qdrant Cloud returns top-4 relevant knowledge chunks
        ↓
LLM generates Socratic hint grounded in retrieved context
        ↓
Leakage gate: regex + semantic check
Failed? → regenerate (up to 3×)
        ↓
Approved hint + 🔊 Listen button
```

---

## Architecture

```
algosensei_genai/
├── main.py                    ← FastAPI backend
├── static/                    ← Frontend (HTML/CSS/JS)
│   ├── index.html             ← Landing page
│   ├── tutor.html             ← Main tutor app
│   ├── login.html / signup.html / dashboard.html
│   └── style.css
├── auth/                      ← Authentication
│   ├── database.py            ← SQLite: users, progress, hint history
│   ├── security.py            ← PBKDF2 hashing + JWT tokens
│   └── routes.py              ← /api/auth/* endpoints
├── engine/
│   ├── gemini_client.py       ← LLM client (OpenAI / OpenRouter)
│   ├── leakage_gate.py        ← Two-stage safety checker
│   └── tutor.py               ← Core tutoring engine
├── rag/
│   ├── embedder.py            ← Local sentence embeddings
│   ├── vector_store.py        ← Qdrant REST API (no grpcio)
│   └── retriever.py           ← Retrieval + faithfulness scoring
├── knowledge/
│   ├── blind75_kb.py          ← 49 curated DSA knowledge chunks
│   └── problem_db.py          ← 175 problems with metadata
└── prompts/
    └── templates.py           ← All LLM prompt templates
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/hint` | Generate Socratic hint |
| `POST` | `/api/explain` | Explain a DSA concept |
| `POST` | `/api/analyze-code` | Analyze code attempt |
| `POST` | `/api/screenshot` | Process screenshot |
| `GET` | `/api/problems` | List problems (filterable) |
| `POST` | `/api/auth/signup` | Create account |
| `POST` | `/api/auth/login` | Sign in |
| `GET` | `/api/auth/progress` | Get user progress |
| `POST` | `/api/auth/progress` | Save progress |

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI + uvicorn |
| Frontend | Vanilla HTML / CSS / JS |
| LLM | OpenRouter (free) or OpenAI |
| Vector DB | Qdrant Cloud |
| Embeddings | all-MiniLM-L6-v2 (local) |
| OCR | pytesseract (local) |
| Auth | SQLite + JWT (no external service) |
| Hosting | Hugging Face Spaces (Docker) |

---

## Contributing

Issues and pull requests are welcome. If you find a hint that reveals the answer directly, please open an issue — that's a leakage gate miss and should be fixed.

---

## License

MIT — free to use, modify, and deploy.

---

Built by [Aditya Mitra](https://github.com/adityaamitra)