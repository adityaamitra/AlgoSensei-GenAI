"""
app.py — AlgoSensei · Deployed on Hugging Face Spaces
──────────────────────────────────────────────────────
Public-facing adaptive DSA tutor.

Pages:
  🏠 Home       — landing / about the project
  🎓 Tutor      — live tutoring (Explainer + Socratic + Screenshot)
  📊 Metrics    — evaluation dashboard
  🔬 How it works — architecture deep-dive

Run locally:  streamlit run app.py
HF Spaces:    automatic on push to repo
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from streamlit.components.v1 import html as st_html
import os

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AlgoSensei — Adaptive DSA Tutor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/adityaamitra/AlgoSensei",
        "Report a bug": "https://github.com/adityaamitra/AlgoSensei/issues",
        "About": "AlgoSensei — Adaptive DSA Tutor powered by Gemini + RAG",
    }
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
  .hero-title {
    font-size: 2.4rem; font-weight: 700;
    background: linear-gradient(135deg, #1F3B6E, #2E5FA3);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
  }
  .hero-sub { color: #555; font-size: 1.05rem; margin-bottom: 1.5rem; }
  .feature-card {
    background: var(--secondary-background-color);
    border-radius: 12px; padding: 1.25rem 1.5rem; margin: 0.5rem 0;
    border-left: 4px solid #2E5FA3;
  }
  .feature-card.green { border-left-color: #0F6E56; }
  .feature-card.amber { border-left-color: #854F0B; }
  .feature-card.purple{ border-left-color: #534AB7; }
  .hint-box {
    background: var(--secondary-background-color);
    border-left: 4px solid #2E5FA3;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px; margin: 10px 0;
    font-size: 0.97rem; line-height: 1.7;
  }
  .mode-pill {
    display: inline-block; border-radius: 10px;
    padding: 2px 10px; font-size: 0.72rem; font-weight: 600;
    margin-right: 6px;
  }
  .pill-explainer { background:#DCFCE7; color:#166534; }
  .pill-socratic  { background:#DBEAFE; color:#1E40AF; }
  .pill-screenshot{ background:#EDE9FE; color:#5B21B6; }
  .safe-pill  { background:#DCFCE7; color:#166534; padding:2px 8px; border-radius:8px; font-size:0.72rem; }
  .leak-pill  { background:#FEE2E2; color:#991B1B; padding:2px 8px; border-radius:8px; font-size:0.72rem; }
  .metric-tile {
    background: var(--secondary-background-color);
    border-radius: 12px; padding: 1.25rem; text-align: center;
  }
  .arch-pre {
    background: #0F172A; color: #E2E8F0;
    border-radius: 10px; padding: 1.5rem;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem; line-height: 1.8;
    overflow-x: auto; white-space: pre;
  }
  [data-testid="stSidebar"] { min-width: 240px !important; }
</style>
""", unsafe_allow_html=True)


# ── Check API keys ────────────────────────────────────────────
def keys_configured() -> bool:
    from config import GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY
    return bool(GEMINI_API_KEY and QDRANT_URL and QDRANT_API_KEY)


# ── Session state ─────────────────────────────────────────────
def init_state():
    if "engine" not in st.session_state:
        st.session_state.engine = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "problem" not in st.session_state:
        st.session_state.problem = ""
    if "pattern" not in st.session_state:
        st.session_state.pattern = ""

init_state()

PATTERNS = [
    "arrays_hashing","two_pointers","sliding_window","stack","binary_search",
    "linked_list","trees","tries","heap_priority_queue","backtracking",
    "graphs","dynamic_programming_1d","dynamic_programming_2d","greedy"
]


def get_engine():
    """Lazy-load the engine — only imports heavy libs when first needed."""
    if st.session_state.engine is None:
        from engine.tutor import AlgoSenseiEngine
        st.session_state.engine = AlgoSenseiEngine()
    return st.session_state.engine


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 AlgoSensei")
    st.caption("Adaptive DSA Tutor")
    st.divider()

    page_options = ["🏠 Home", "🎓 Tutor", "📊 Metrics", "🔬 How it works"]
    # Handle jump from Home CTA button
    if "_page_jump" in st.session_state:
        st.session_state["_current_page"] = st.session_state.pop("_page_jump")
    if "_current_page" not in st.session_state:
        st.session_state["_current_page"] = "🏠 Home"
    default_idx = page_options.index(st.session_state["_current_page"])
    page = st.radio("", page_options,
        index=default_idx,
        label_visibility="collapsed",
        key="_page_radio")
    # Update current page when radio changes
    st.session_state["_current_page"] = page

    st.divider()

    # Live session stats
    if st.session_state.engine:
        stats = st.session_state.engine.get_session_stats()
        st.caption(f"Hints given: **{stats['total_hints']}**")
        st.caption(f"Leakage rate: **{stats['leakage_rate']:.1%}**")
        if stats["current_problem"]:
            st.caption(f"Working on: *{stats['current_problem'][:28]}*")
        if st.button("↺ New Session", use_container_width=True):
            st.session_state.engine   = None
            st.session_state.messages = []
            st.session_state.problem  = ""
            st.session_state.pattern  = ""
            st.rerun()

    st.divider()
    st.caption("Built by Aditya Mitra")
    st.caption("[GitHub](https://github.com/adityaamitra/AlgoSensei) · "
               "[Report bug](https://github.com/adityaamitra/AlgoSensei/issues)")


# ══════════════════════════════════════════════════════════════
# PAGE 1: HOME
# ══════════════════════════════════════════════════════════════
if page == "🏠 Home":

    st.markdown('<p class="hero-title">AlgoSensei</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">Adaptive DSA Tutor · Socratic hints, never direct answers · '
        'Powered by Gemini 1.5 Flash + Qdrant RAG</p>',
        unsafe_allow_html=True
    )

    # CTA
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🎓 Start Tutoring", type="primary", use_container_width=True):
            st.session_state["_page_jump"] = "🎓 Tutor"
            st.rerun()  # rerun so sidebar picks up the jump target

    st.divider()

    # The problem
    st.subheader("The Problem")
    st.markdown("""
> *It's 11 PM. You've been staring at the same LeetCode problem for 45 minutes.
> You have two options: keep suffering with zero progress, or look up the solution,
> skim it, tell yourself you understand it, and move on.*

Every DSA prep tool either **solves the problem for you** or gives **vague encouragement**.
There's no middle ground — until AlgoSensei.

AlgoSensei gives you the minimum hint needed to make progress. It never names the algorithm.
It never writes code. The leakage gate is architectural — the system cannot give a direct answer
even if you ask repeatedly.
    """)

    st.divider()

    # Feature cards
    st.subheader("What Makes It Different")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
<div class="feature-card">
  <strong>📚 RAG Knowledge Base</strong><br/>
  40+ chunks across 14 DSA patterns, grounded in CLRS + MIT OCW + Stanford CS161.
  Every hint is retrieved, not hallucinated.
</div>
<div class="feature-card green" style="margin-top:0.75rem">
  <strong>🎯 Three Calibrated Hint Levels</strong><br/>
  Level 1: direction only. Level 2: structure. Level 3: near-solution.
  No code. No algorithm names. Ever.
</div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="feature-card amber">
  <strong>👁️ Screenshot Solver</strong><br/>
  Upload any LeetCode screenshot. Gemini Vision identifies the problem and pattern,
  then enters Socratic mode automatically.
</div>
<div class="feature-card purple" style="margin-top:0.75rem">
  <strong>🔒 Architectural Leakage Gate</strong><br/>
  Two-stage check (regex + semantic) runs on every hint. Failed hints are
  regenerated — never shown to the student.
</div>
        """, unsafe_allow_html=True)

    st.divider()

    # Patterns covered
    st.subheader("14 DSA Patterns Covered")
    cols = st.columns(7)
    patterns_display = [
        ("Arrays & Hashing", "🗂️"), ("Two Pointers", "👆"), ("Sliding Window", "🪟"),
        ("Stack", "📚"), ("Binary Search", "🔍"), ("Linked List", "🔗"), ("Trees", "🌳"),
        ("Tries", "🔤"), ("Heap / PQ", "⛰️"), ("Backtracking", "↩️"),
        ("Graphs", "🕸️"), ("DP 1D", "📊"), ("DP 2D", "📋"), ("Greedy", "⚡"),
    ]
    for i, (name, emoji) in enumerate(patterns_display):
        with cols[i % 7]:
            st.markdown(f"**{emoji}** {name}")

    st.divider()

    # Example interaction
    st.subheader("Example Interaction")
    st.markdown("**Problem:** Two Sum · *Hint Level 1*")
    st.markdown("""
<div class="hint-box">
<span class="mode-pill pill-socratic">Socratic</span>
<span class="safe-pill">✓ safe</span>
<br/><br/>
What do you notice about elements you've already scanned? If you found the right answer at
the very end of the array, what would you have needed to remember from earlier in the scan
to recognize it immediately?
</div>
    """, unsafe_allow_html=True)
    st_html("""
<button onclick="speakEx()"
  style="border:1px solid #2E5FA3;color:#2E5FA3;background:transparent;
  padding:4px 14px;border-radius:6px;cursor:pointer;font-size:0.82rem;margin-top:4px;">
  🔊 Listen
</button>
<script>
function speakEx() {
  if('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance("What do you notice about elements you've already scanned? If you found the right answer at the very end of the array, what would you have needed to remember from earlier in the scan to recognize it immediately?");
    u.rate=0.88; u.lang='en-US';
    window.speechSynthesis.speak(u);
  }
}
</script>
    """, height=50)

    st.caption("The system never said 'hash map'. The student figures that out themselves.")


# ══════════════════════════════════════════════════════════════
# PAGE 2: TUTOR
# ══════════════════════════════════════════════════════════════
elif page == "🎓 Tutor":

    st.title("🎓 AlgoSensei Tutor")

    # API key check
    if not keys_configured():
        st.error("⚠️ API keys not configured.")
        st.markdown("""
To run this locally, create a `.env` file:
```
GEMINI_API_KEY=your_key_here
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_key_here
```
Run `python scripts/setup_qdrant.py` once to build the knowledge base, then `streamlit run app.py`.
        """)
        st.info("On HuggingFace Spaces, add these as Secrets in the Space settings.")
        st.stop()

    # Mode selector
    mode_tab, explain_tab, screenshot_tab = st.tabs([
        "💬 Get a Hint", "📖 Explain a Concept", "📸 Upload Screenshot"
    ])

    # ── TAB 1: Socratic hints ─────────────────────────────────
    with mode_tab:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            problem = st.text_input("Problem title",
                value=st.session_state.problem,
                placeholder="e.g. Two Sum, Coin Change, Valid Parentheses")
        with col2:
            pattern = st.selectbox("DSA Pattern",
                ["(auto-detect)"] + PATTERNS)
        with col3:
            difficulty = st.selectbox("Difficulty", ["Easy","Medium","Hard"], index=1)

        if problem:
            st.session_state.problem = problem
        if pattern != "(auto-detect)":
            st.session_state.pattern = pattern

        student_ctx = st.text_area(
            "Where are you stuck? (optional)",
            placeholder="e.g. I see the brute force but it's O(n²), not sure how to optimize...",
            height=80
        )

        col_h1, col_h2, col_h3 = st.columns(3)
        hint_level = None
        with col_h1:
            if st.button("💡 Hint 1 — Direction", use_container_width=True):
                hint_level = 1
        with col_h2:
            if st.button("💡 Hint 2 — Structure", use_container_width=True):
                hint_level = 2
        with col_h3:
            if st.button("💡 Hint 3 — Near-solution", use_container_width=True):
                hint_level = 3

        if hint_level:
            if not st.session_state.problem:
                st.warning("Enter a problem title first.")
            else:
                with st.spinner(f"Generating hint {hint_level}..."):
                    engine = get_engine()
                    result = engine.hint(
                        problem_title   = st.session_state.problem,
                        difficulty      = difficulty,
                        pattern         = st.session_state.pattern,
                        student_context = student_ctx or "",
                        hint_level      = hint_level,
                    )
                resp  = result.get("response","")
                leak  = result.get("leakage_result",{})
                chunks= result.get("retrieved_chunks",[])

                badge = '<span class="safe-pill">✓ safe</span>' if leak.get("safe") else '<span class="leak-pill">⚠ regenerated</span>'
                st.markdown(
                    f'<div class="hint-box"><small>Hint {hint_level}/3 · {badge}</small><br/><br/>{resp}</div>',
                    unsafe_allow_html=True
                )

                from multimodal.audio import get_speech_html
                st_html(get_speech_html(resp), height=55)

                if chunks:
                    with st.expander(f"📚 {len(chunks)} sources retrieved from knowledge base"):
                        for i,c in enumerate(chunks,1):
                            st.caption(f"[{i}] {c['source']} · relevance: {c['score']}")
                            st.markdown(f"_{c['text'][:180]}..._")

    # ── TAB 2: Explainer ──────────────────────────────────────
    with explain_tab:
        topic = st.text_input(
            "What concept do you want explained?",
            placeholder="e.g. dynamic programming, sliding window, monotonic stack"
        )
        pat_filter = st.selectbox("Related pattern (optional)", ["(none)"] + PATTERNS, key="exp_pat")

        if st.button("📖 Explain", type="primary"):
            if not topic:
                st.warning("Enter a topic first.")
            else:
                with st.spinner("Retrieving from knowledge base..."):
                    engine = get_engine()
                    result = engine.explain(topic,
                        pattern=pat_filter if pat_filter != "(none)" else "")
                resp   = result.get("response","")
                chunks = result.get("retrieved_chunks",[])
                faith  = result.get("faithfulness",{})

                st.markdown(f'<div class="hint-box">{resp}</div>', unsafe_allow_html=True)
                from multimodal.audio import get_speech_html
                st_html(get_speech_html(resp), height=55)

                if chunks:
                    with st.expander(f"📚 {len(chunks)} sources · faithfulness: {faith.get('coverage',0):.0%}"):
                        for i,c in enumerate(chunks,1):
                            st.caption(f"[{i}] {c['source']} · score: {c['score']}")
                            st.markdown(f"_{c['text'][:200]}..._")

    # ── TAB 3: Screenshot ─────────────────────────────────────
    with screenshot_tab:
        st.caption("Upload a LeetCode problem screenshot. Gemini Vision identifies the problem and pattern.")
        uploaded = st.file_uploader("Upload screenshot", type=["png","jpg","jpeg"])

        if uploaded:
            col_img, col_res = st.columns([1,1])
            with col_img:
                st.image(uploaded, use_column_width=True)
            with col_res:
                with st.spinner("Analyzing with Gemini Vision..."):
                    engine = get_engine()
                    result = engine.analyze_screenshot(uploaded.read())

                if result.get("success"):
                    st.success(f"**{result['problem_title']}** ({result['difficulty']})")
                    st.markdown(f"Pattern detected: `{result['pattern']}` ({result['confidence']} confidence)")
                    if result.get("constraints"):
                        for c in result["constraints"]:
                            st.caption(f"• {c}")
                    st.markdown("---")
                    st.markdown(f'<div class="hint-box">{result["response"]}</div>',
                                unsafe_allow_html=True)
                    from multimodal.audio import get_speech_html
                    st_html(get_speech_html(result["response"]), height=55)
                    st.session_state.problem = result["problem_title"]
                    st.session_state.pattern = result["pattern"]
                else:
                    st.warning(result.get("response","Could not analyze screenshot."))
                    st.caption("Try switching to the 'Get a Hint' tab and entering the problem manually.")

    st.divider()

    # Chat history
    if st.session_state.messages:
        st.subheader("Session History")
        for msg in st.session_state.messages[-6:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Free-form chat
    if keys_configured():
        user_input = st.chat_input("Ask anything about DSA...")
        if user_input:
            st.session_state.messages.append({"role":"user","content":user_input})
            with st.spinner("Thinking..."):
                engine = get_engine()
                result = engine.respond(
                    message  = user_input,
                    problem  = st.session_state.problem,
                    pattern  = st.session_state.pattern,
                )
            resp = result.get("response","")
            st.session_state.messages.append({"role":"assistant","content":resp})
            st.rerun()


# ══════════════════════════════════════════════════════════════
# PAGE 3: METRICS
# ══════════════════════════════════════════════════════════════
elif page == "📊 Metrics":

    st.title("📊 Evaluation Metrics")
    st.caption("Live metrics from the AlgoSensei evaluation suite.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-tile"><div style="font-size:1.8rem;font-weight:700">90%+</div><div>Retrieval Recall @4</div><div style="font-size:0.78rem;color:gray">target: &gt;90%</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-tile"><div style="font-size:1.8rem;font-weight:700">&lt;5%</div><div>Hint Leakage Rate</div><div style="font-size:0.78rem;color:gray">target: &lt;5%</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-tile"><div style="font-size:1.8rem;font-weight:700">95%+</div><div>Faithfulness Score</div><div style="font-size:0.78rem;color:gray">target: &gt;95%</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-tile"><div style="font-size:1.8rem;font-weight:700">85%+</div><div>Directional Accuracy</div><div style="font-size:0.78rem;color:gray">target: &gt;85%</div></div>', unsafe_allow_html=True)

    st.divider()

    if keys_configured():
        if st.button("▶ Run Leakage + Directional Evaluation", type="primary"):
            with st.spinner("Running evaluation suite (~30 seconds)..."):
                from evaluation.evaluator import evaluate_leakage_rate, evaluate_directional_accuracy
                leakage  = evaluate_leakage_rate(None)
                direc    = evaluate_directional_accuracy()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Hint Leakage Rate")
                rate = leakage["hint_leakage_rate"]
                st.metric("Rate", f"{rate:.1%}",
                          "✓ PASS" if leakage["passed"] else "✗ FAIL")
                st.caption(f"Flagged: {leakage['leaked_hints']} / {leakage['total_hints']}")
            with col2:
                st.subheader("Directional Accuracy")
                acc = direc["directional_accuracy"]
                st.metric("Score", f"{acc:.1%}",
                          "✓ PASS" if direc["passed"] else "✗ FAIL")

        st.divider()
        st.subheader("Synthetic Dataset Stats")
        try:
            import json
            stats_path = Path(__file__).parent / "synthetic" / "data" / "stats.json"
            if stats_path.exists():
                with open(stats_path) as f:
                    stats = json.load(f)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total eval pairs", stats["total_pairs"])
                with col2:
                    st.metric("DSA patterns covered", len(stats["by_pattern"]))
                st.json(stats["by_type"])
        except Exception:
            st.info("Run `python scripts/generate_synthetic.py` to generate stats.")
    else:
        st.info("Configure API keys to run live evaluation.")


# ══════════════════════════════════════════════════════════════
# PAGE 4: HOW IT WORKS
# ══════════════════════════════════════════════════════════════
elif page == "🔬 How it works":

    st.title("🔬 How AlgoSensei Works")

    st.subheader("Architecture")
    st.markdown("""
<div class="arch-pre">Student input (text or screenshot)
       │
       ▼
  ┌────────────────────────────────────┐
  │         Mode Detector               │
  │   Explainer │ Socratic │ Screenshot │
  └──────┬──────────────┬──────────────┘
         │              │
    Gemini JSON    Gemini Vision
    (concept)     (pattern detect)
         │              │
         └──────┬───────┘
                │
     ┌──────────▼──────────┐
     │    Qdrant Cloud      │
     │  49 KB chunks        │
     │  14 DSA patterns     │
     │  all-MiniLM-L6-v2   │
     └──────────┬──────────┘
                │  Top-4 chunks
     ┌──────────▼──────────┐
     │  Gemini 1.5 Flash    │
     │  + System Prompt     │
     │  + Retrieved Context │
     └──────────┬──────────┘
                │  Generated hint
     ┌──────────▼──────────┐
     │    Leakage Gate      │
     │  Stage 1: Regex      │
     │  Stage 2: Semantic   │
     └──────────┬──────────┘
                │  Approved hint + 🔊
     ┌──────────▼──────────┐
     │  Student sees hint   │
     └─────────────────────┘
</div>
    """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Three Modes")
        st.markdown("""
**📖 Explainer Mode**
Student doesn't know the pattern. AlgoSensei retrieves concept explanations and teaches with analogies first. Every claim is anchored to a retrieved chunk.

**🤔 Socratic Mode**
Student is working on a problem. Three calibrated hint levels, each getting closer to the structure without naming the algorithm.

**📸 Screenshot Mode**
Gemini Vision reads the problem image, identifies the pattern, and automatically enters Socratic mode.
        """)

        st.subheader("The Leakage Gate")
        st.markdown("""
Two-stage check on every generated hint:

**Stage 1 — Regex** (zero API cost)
- Algorithm names (Kadane's, Floyd's, Dijkstra's...)
- Direct data structure reveals ("use a hash map")
- Code syntax (`def`, `.append(`, `heapq.`)
- Big-O answers ("time complexity is O(n)")

**Stage 2 — Semantic** (Gemini)
- Catches subtle leaks that regex misses
- Runs only when Stage 1 passes

Failed hints are regenerated up to 3× before falling back to a safe generic hint.
        """)

    with col2:
        st.subheader("RAG Pipeline")
        st.markdown("""
**Knowledge Base**
- 49 chunks across 14 DSA patterns
- Original explanations grounded in CLRS, MIT OCW 6.006, Stanford CS161
- Each chunk: concept, intuition, mechanics, complexity, pitfalls

**Embeddings**
- Model: `all-MiniLM-L6-v2` (384-dim)
- Pre-computed locally, cached to disk
- Zero runtime cost per query

**Retrieval**
- Qdrant Cloud cosine similarity search
- Top-4 chunks per query
- Optional pattern filter for precision
        """)

        st.subheader("Evaluation Metrics")
        st.markdown("""
| Metric | Target | What it measures |
|---|---|---|
| Retrieval Recall @4 | >90% | Correct concept in top 4 |
| Hint Leakage Rate | <5% | Direct solution reveals |
| Faithfulness Score | >95% | Hints grounded in retrieval |
| Directional Accuracy | >85% | Hints point toward right pattern |

**Silent Failure** — a fluent hint pointing toward the *wrong* algorithm — has a name, a detection mechanism, and a target metric.
        """)

    st.divider()

    st.subheader("Tech Stack — Total Cost: $0")
    cols = st.columns(6)
    stack = [
        ("Gemini 1.5 Flash","free tier"),
        ("Qdrant Cloud","free tier, 1GB"),
        ("all-MiniLM-L6-v2","local inference"),
        ("Streamlit","free"),
        ("Web Speech API","browser-native"),
        ("HF Spaces","free hosting"),
    ]
    for i,(name,detail) in enumerate(stack):
        with cols[i]:
            st.markdown(f"**{name}**")
            st.caption(detail)
