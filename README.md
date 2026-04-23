# AlgoSensei — Adaptive DSA Tutor

**Stop looking up answers. Start building intuition.**

AlgoSensei gives you calibrated Socratic hints for Blind 75 LeetCode problems — guiding you toward the insight without handing you the answer. Three hint levels, a leakage gate that architecturally prevents solution reveals, and a knowledge base grounded in CLRS + MIT OCW.

🚀 **[Try the live demo](https://huggingface.co/spaces/adityaamitra/AlgoSensei)** · 🌐 **[Project website](https://adityaamitra.github.io/AlgoSensei-GenAI/)** · 📄 **[Technical report](AlgoSensei_Technical_Report.pdf)**

---

## What it does

You're stuck on a LeetCode problem. Every other tool either solves it for you or gives vague encouragement. AlgoSensei does neither — it asks you questions that guide you toward the insight.

**Three modes:**

| Mode | How to use |
|---|---|
| **Get a Hint** | Enter a problem title, pick a pattern, click Hint 1 / 2 / 3 |
| **Explain a Concept** | Type any DSA concept — get a retrieval-grounded explanation with analogies |
| **Upload Screenshot** | Drop a LeetCode screenshot — OCR detects the problem, gives a first hint automatically |

**Three hint levels:**
- Level 1 — Direction only. Points toward what to examine, nothing more.
- Level 2 — Structure. Guides toward the type of operation needed.
- Level 3 — Near-solution. Describes the abstract approach without naming the algorithm or writing code.

---

## Generative AI components

| Component | Technology | What it does |
|---|---|---|
| RAG | Qdrant Cloud + all-MiniLM-L6-v2 | 49 knowledge chunks, 14 DSA patterns, retrieved per query |
| Prompt Engineering | OpenRouter LLM | 3 system prompts + leakage gate + calibrated hint levels |
| Multimodal | OCR (pytesseract) + Web Speech API | Screenshot → text → pattern + 🔊 Listen button |
| Synthetic Data | Auto-generated JSONL | 110 evaluation pairs across 22 problems × 5 interaction types |

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/adityaamitra/AlgoSensei-GenAI
cd AlgoSensei-GenAI/algosensei_genai

# 2. Install
pip install -r requirements.txt

# 3. Install Tesseract OCR (for screenshot tab)
brew install tesseract          # macOS
# sudo apt install tesseract-ocr  # Ubuntu

# 4. Add API keys
cp .env.example .env
# Fill in: OPENROUTER_API_KEY, QDRANT_URL, QDRANT_API_KEY

# 5. Build knowledge base (one-time, ~2 min)
python scripts/setup_qdrant.py

# 6. Generate evaluation data (one-time)
python scripts/generate_synthetic.py

# 7. Launch
streamlit run app.py
```

**Free API keys:**
- OpenRouter: [openrouter.ai/keys](https://openrouter.ai/keys) — use any free model (e.g. `nvidia/llama-3.1-nemotron-ultra-253b-v1:free`)
- Qdrant Cloud: [cloud.qdrant.io](https://cloud.qdrant.io) — free tier, 1GB

---

## Project structure

```
algosensei_genai/
├── app.py                        ← Streamlit app (Home, Tutor, Metrics, How it works)
├── config.py                     ← All config — reads from .env locally, Secrets on HF
├── requirements.txt
├── .env.example
│
├── knowledge/
│   └── blind75_kb.py             ← 49 DSA knowledge chunks, 14 patterns
│
├── rag/
│   ├── embedder.py               ← all-MiniLM-L6-v2, pre-computed + cached
│   ├── vector_store.py           ← Qdrant Cloud interface
│   └── retriever.py              ← Retrieval + faithfulness scoring
│
├── prompts/
│   └── templates.py              ← All prompt templates (3 modes + leakage gate)
│
├── engine/
│   ├── gemini_client.py          ← OpenRouter HTTP client (no SDK needed)
│   ├── leakage_gate.py           ← Two-stage safety checker (regex + semantic)
│   └── tutor.py                  ← Core engine: TutoringSession + AlgoSenseiEngine
│
├── multimodal/
│   └── audio.py                  ← Web Speech API 🔊 Listen button
│
├── synthetic/
│   ├── generate.py               ← 110 evaluation pair generator
│   └── data/
│       ├── eval_pairs.jsonl      ← Generated evaluation dataset
│       └── stats.json
│
├── evaluation/
│   └── evaluator.py              ← 4 metrics: Recall @4, Leakage, Faithfulness, Accuracy
│
├── scripts/
│   ├── setup_qdrant.py           ← ONE-TIME: embed KB + upload to Qdrant
│   ├── generate_synthetic.py     ← Generate evaluation data
│   └── run_evaluation.py         ← Run full evaluation suite
│
├── tests/
│   └── test_all.py               ← 24 unit tests
│
└── web/
    └── index.html                ← GitHub Pages landing page
```

---

## Evaluation

```bash
python scripts/run_evaluation.py
```

| Metric | Target | What it measures |
|---|---|---|
| Retrieval Recall @4 | >90% | Correct concept in top 4 retrieved chunks |
| Hint Leakage Rate | <5% | Hints with direct solution steps |
| Faithfulness Score | >95% | Hint claims grounded in retrieved context |
| Directional Accuracy | >85% | Hints pointing toward correct DSA pattern |

---

## How the RAG pipeline works

```
Student question
      ↓
all-MiniLM-L6-v2 embeds query (local, zero cost)
      ↓
Qdrant Cloud cosine similarity search → top-4 chunks
      ↓
Chunks injected into system prompt as grounding context
      ↓
OpenRouter LLM generates calibrated Socratic hint
      ↓
Leakage gate (regex + semantic) validates output
      ↓
Approved hint + 🔊 Listen button
```

---

## Deploying to Hugging Face Spaces

1. Create a new Streamlit Space at [huggingface.co](https://huggingface.co)
2. Upload this entire folder
3. Rename `README_HF.md` → `README.md`
4. Add Secrets in Space Settings:
   - `OPENROUTER_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `OPENROUTER_MODEL` (optional — defaults to Nemotron)
5. Push — auto-deploys in ~3 minutes

---

## Tech stack — Total cost: $0

| Service | Usage |
|---|---|
| OpenRouter | LLM inference — free models available |
| Qdrant Cloud | Vector DB — free tier, 1GB |
| all-MiniLM-L6-v2 | Embeddings — local inference, no API |
| pytesseract | OCR — local, no API |
| Web Speech API | Audio output — browser-native |
| Streamlit | UI framework |
| Hugging Face Spaces | Hosting — free |
| GitHub Pages | Landing page — free |

---

## Author

Aditya Mitra — [GitHub](https://github.com/adityaamitra)
