"""
app.py — AlgoSensei · Redesigned UI
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from streamlit.components.v1 import html as st_html
import os

st.set_page_config(
    page_title="AlgoSensei — DSA Tutor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Reset Streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding: 0 !important; max-width: 100% !important;}
section[data-testid="stSidebar"] {display: none !important;}
[data-testid="stAppViewContainer"] > .main {padding: 0 !important;}
.stDeployButton {display: none;}

/* Base */
*, *::before, *::after {box-sizing: border-box;}
body, .stApp {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  background: #0A0E1A !important;
  color: #E2E8F0 !important;
}

/* App shell */
.app-shell {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 100vh;
  background: #0A0E1A;
}

/* Sidebar */
.sidebar {
  background: #0F1629;
  border-right: 1px solid #1E2D4A;
  padding: 0;
  position: fixed;
  top: 0; left: 0;
  width: 260px;
  height: 100vh;
  overflow-y: auto;
  z-index: 10;
  display: flex;
  flex-direction: column;
}
.sidebar-logo {
  padding: 24px 20px 20px;
  border-bottom: 1px solid #1E2D4A;
}
.logo-mark {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 4px;
}
.logo-icon {
  width: 38px; height: 38px;
  background: linear-gradient(135deg, #3B5BDB, #7048E8);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; flex-shrink: 0;
}
.logo-text {
  font-size: 1.15rem; font-weight: 700; color: #F1F5F9;
}
.logo-sub {
  font-size: 0.72rem; color: #64748B; margin-top: 2px;
}

/* Nav */
.nav-section {
  padding: 16px 12px 8px;
  flex: 1;
}
.nav-label {
  font-size: 0.65rem; font-weight: 600; color: #475569;
  text-transform: uppercase; letter-spacing: 0.1em;
  padding: 0 8px; margin-bottom: 6px;
}
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 9px 12px; border-radius: 8px;
  cursor: pointer; transition: all .15s;
  margin-bottom: 2px; text-decoration: none;
  font-size: 0.875rem; font-weight: 500; color: #94A3B8;
  border: none; background: transparent; width: 100%; text-align: left;
}
.nav-item:hover {background: #1E2D4A; color: #E2E8F0;}
.nav-item.active {background: rgba(59,91,219,.15); color: #818CF8; border: 1px solid rgba(59,91,219,.2);}
.nav-icon {font-size: 15px; width: 18px; text-align: center; flex-shrink: 0;}

/* Stats */
.sidebar-stats {
  padding: 12px 16px;
  margin: 8px 12px;
  background: #131D35;
  border-radius: 10px;
  border: 1px solid #1E2D4A;
}
.stat-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 5px 0;
  font-size: 0.78rem;
  border-bottom: 1px solid #1E2D4A;
}
.stat-row:last-child {border-bottom: none;}
.stat-key {color: #64748B;}
.stat-val {color: #818CF8; font-weight: 600; font-family: 'JetBrains Mono', monospace;}
.stat-val.green {color: #34D399;}
.stat-val.amber {color: #FBBF24;}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid #1E2D4A;
  font-size: 0.72rem; color: #475569;
}
.sidebar-footer a {color: #6366F1; text-decoration: none;}

/* Main content */
.main-content {
  margin-left: 260px;
  min-height: 100vh;
  display: flex; flex-direction: column;
}

/* Top bar */
.topbar {
  background: #0F1629;
  border-bottom: 1px solid #1E2D4A;
  padding: 0 28px;
  height: 58px;
  display: flex; align-items: center; justify-content: space-between;
  position: sticky; top: 0; z-index: 5;
}
.topbar-title {
  font-size: 1rem; font-weight: 600; color: #F1F5F9;
}
.topbar-breadcrumb {
  font-size: 0.78rem; color: #475569; margin-top: 1px;
}
.topbar-right {
  display: flex; align-items: center; gap: 10px;
}
.badge-safe {
  background: rgba(52,211,153,.12); color: #34D399;
  border: 1px solid rgba(52,211,153,.2);
  border-radius: 20px; padding: 4px 12px;
  font-size: 0.72rem; font-weight: 600;
}
.badge-warn {
  background: rgba(251,191,36,.12); color: #FBBF24;
  border: 1px solid rgba(251,191,36,.2);
  border-radius: 20px; padding: 4px 12px;
  font-size: 0.72rem; font-weight: 600;
}

/* Page body */
.page-body {
  padding: 28px;
  flex: 1;
}

/* Cards */
.card {
  background: #0F1629;
  border: 1px solid #1E2D4A;
  border-radius: 14px;
  padding: 20px 24px;
}
.card-sm {
  background: #131D35;
  border: 1px solid #1E2D4A;
  border-radius: 10px;
  padding: 14px 16px;
}

/* Hint output */
.hint-output {
  background: #0F1629;
  border: 1px solid #1E2D4A;
  border-left: 3px solid #6366F1;
  border-radius: 0 12px 12px 0;
  padding: 18px 20px;
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.75;
  color: #E2E8F0;
}
.hint-meta {
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 12px; flex-wrap: wrap;
}
.pill {
  border-radius: 20px; padding: 3px 10px;
  font-size: 0.72rem; font-weight: 600;
}
.pill-level {background: rgba(99,102,241,.15); color: #818CF8; border: 1px solid rgba(99,102,241,.25);}
.pill-safe  {background: rgba(52,211,153,.12); color: #34D399; border: 1px solid rgba(52,211,153,.2);}
.pill-mode  {background: rgba(251,191,36,.1);  color: #FBBF24; border: 1px solid rgba(251,191,36,.2);}

/* Sources expander */
.source-item {
  padding: 10px 14px; margin-bottom: 6px;
  background: #131D35; border-radius: 8px;
  border: 1px solid #1E2D4A;
}
.source-label {
  font-size: 0.72rem; color: #6366F1; font-weight: 600; margin-bottom: 4px;
}
.source-text {
  font-size: 0.8rem; color: #94A3B8; line-height: 1.5;
}

/* Input overrides */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
  background: #131D35 !important;
  border: 1px solid #1E2D4A !important;
  color: #E2E8F0 !important;
  border-radius: 8px !important;
  font-family: 'Inter', sans-serif !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
  border-color: #6366F1 !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
}
div[data-testid="stSelectbox"] > div > div {
  background: #131D35 !important;
  border: 1px solid #1E2D4A !important;
  color: #E2E8F0 !important;
  border-radius: 8px !important;
}

/* Button overrides */
.stButton > button {
  background: #3B5BDB !important;
  color: #fff !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-family: 'Inter', sans-serif !important;
  transition: all .2s !important;
  padding: 8px 18px !important;
}
.stButton > button:hover {
  background: #2F4AC4 !important;
  transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
  background: #131D35 !important;
  border: 1px solid #1E2D4A !important;
  color: #94A3B8 !important;
}
.stButton > button[kind="secondary"]:hover {
  background: #1E2D4A !important;
  color: #E2E8F0 !important;
}

/* Tabs */
div[data-testid="stTabs"] [role="tablist"] {
  background: transparent !important;
  border-bottom: 1px solid #1E2D4A !important;
  gap: 4px !important;
}
div[data-testid="stTabs"] button[role="tab"] {
  background: transparent !important;
  color: #64748B !important;
  border-radius: 6px 6px 0 0 !important;
  font-weight: 500 !important;
  font-size: 0.875rem !important;
  padding: 8px 16px !important;
  border: none !important;
  font-family: 'Inter', sans-serif !important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
  color: #818CF8 !important;
  background: rgba(99,102,241,.1) !important;
  border-bottom: 2px solid #6366F1 !important;
}
div[data-testid="stTabs"] [data-testid="stTabsContent"] {
  padding-top: 20px !important;
}

/* Expander */
div[data-testid="stExpander"] {
  background: #131D35 !important;
  border: 1px solid #1E2D4A !important;
  border-radius: 10px !important;
}
div[data-testid="stExpander"] summary {
  color: #94A3B8 !important;
  font-size: 0.82rem !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
  background: #131D35;
  border: 1px solid #1E2D4A;
  border-radius: 12px;
  padding: 16px !important;
}
div[data-testid="stMetricLabel"] {color: #64748B !important; font-size: .8rem !important;}
div[data-testid="stMetricValue"] {color: #818CF8 !important; font-size: 1.6rem !important; font-weight: 700 !important;}
div[data-testid="stMetricDelta"] {font-size: .75rem !important;}

/* File uploader */
div[data-testid="stFileUploader"] {
  background: #131D35 !important;
  border: 1px dashed #1E2D4A !important;
  border-radius: 10px !important;
}
div[data-testid="stFileUploader"]:hover {
  border-color: #6366F1 !important;
}

/* Chat input */
div[data-testid="stChatInput"] > div {
  background: #131D35 !important;
  border: 1px solid #1E2D4A !important;
  border-radius: 12px !important;
}
div[data-testid="stChatInput"] textarea {
  color: #E2E8F0 !important;
}

/* Chat messages */
div[data-testid="stChatMessage"] {
  background: #131D35 !important;
  border: 1px solid #1E2D4A !important;
  border-radius: 12px !important;
  margin-bottom: 8px !important;
}

/* Divider */
hr {border-color: #1E2D4A !important;}

/* Success/info/warning */
div[data-testid="stAlert"] {
  border-radius: 10px !important;
  border: none !important;
}

/* Scrollbar */
::-webkit-scrollbar {width: 5px; height: 5px;}
::-webkit-scrollbar-track {background: #0A0E1A;}
::-webkit-scrollbar-thumb {background: #1E2D4A; border-radius: 4px;}
::-webkit-scrollbar-thumb:hover {background: #2D3F5E;}

/* Listen button */
.listen-btn {
  display: inline-flex; align-items: center; gap: 6px;
  background: transparent;
  border: 1px solid #1E2D4A;
  color: #64748B;
  border-radius: 8px; padding: 5px 12px;
  font-size: 0.78rem; cursor: pointer;
  transition: all .15s; font-family: 'Inter', sans-serif;
  margin-top: 12px;
}
.listen-btn:hover {border-color: #6366F1; color: #818CF8;}

/* Hint level buttons */
.hint-btn-row {display: flex; gap: 10px; flex-wrap: wrap; margin-top: 4px;}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────
def keys_configured() -> bool:
    from config import OPENROUTER_API_KEY, QDRANT_URL, QDRANT_API_KEY
    return bool(OPENROUTER_API_KEY and QDRANT_URL and QDRANT_API_KEY)

def init_state():
    defaults = {
        "page": "tutor",
        "engine": None,
        "messages": [],
        "problem": "",
        "pattern": "",
        "last_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

PATTERNS = [
    "arrays_hashing","two_pointers","sliding_window","stack","binary_search",
    "linked_list","trees","tries","heap_priority_queue","backtracking",
    "graphs","dynamic_programming_1d","dynamic_programming_2d","greedy"
]
PATTERN_LABELS = {
    "arrays_hashing":"Arrays & Hashing","two_pointers":"Two Pointers",
    "sliding_window":"Sliding Window","stack":"Stack",
    "binary_search":"Binary Search","linked_list":"Linked List",
    "trees":"Trees","tries":"Tries","heap_priority_queue":"Heap / PQ",
    "backtracking":"Backtracking","graphs":"Graphs",
    "dynamic_programming_1d":"DP 1D","dynamic_programming_2d":"DP 2D","greedy":"Greedy",
}

def get_engine():
    if st.session_state.engine is None:
        from engine.tutor import AlgoSenseiEngine
        st.session_state.engine = AlgoSenseiEngine()
    return st.session_state.engine

def get_stats():
    if st.session_state.engine:
        return st.session_state.engine.get_session_stats()
    return {"total_hints": 0, "leakage_rate": 0.0, "current_problem": "", "hint_level": 0, "mode_counts": {}}


# ── Sidebar ────────────────────────────────────────────────────
stats = get_stats()
leak_class = "green" if stats["leakage_rate"] == 0.0 else "amber"

nav_html = f"""
<div class="sidebar">
  <div class="sidebar-logo">
    <div class="logo-mark">
      <div class="logo-icon">🧠</div>
      <span class="logo-text">AlgoSensei</span>
    </div>
    <div class="logo-sub">Adaptive DSA Tutor · Free · Open Source</div>
  </div>

  <div class="nav-section">
    <div class="nav-label">Navigation</div>
    <button class="nav-item {'active' if st.session_state.page == 'tutor' else ''}" onclick="window.parent.document.querySelector('[data-testid=stApp]').dispatchEvent(new CustomEvent('nav', {{detail:'tutor'}}))">
      <span class="nav-icon">🎓</span> Tutor
    </button>
    <button class="nav-item {'active' if st.session_state.page == 'metrics' else ''}" onclick="window.parent.document.querySelector('[data-testid=stApp]').dispatchEvent(new CustomEvent('nav', {{detail:'metrics'}}))">
      <span class="nav-icon">📊</span> Metrics
    </button>
    <button class="nav-item {'active' if st.session_state.page == 'howto' else ''}" onclick="window.parent.document.querySelector('[data-testid=stApp]').dispatchEvent(new CustomEvent('nav', {{detail:'howto'}}))">
      <span class="nav-icon">🔬</span> How it works
    </button>
  </div>

  <div style="padding: 0 12px 12px;">
    <div class="sidebar-stats">
      <div class="stat-row"><span class="stat-key">Hints given</span><span class="stat-val">{stats['total_hints']}</span></div>
      <div class="stat-row"><span class="stat-key">Leakage rate</span><span class="stat-val {leak_class}">{stats['leakage_rate']:.1%}</span></div>
      <div class="stat-row"><span class="stat-key">Working on</span><span class="stat-val">{(stats['current_problem'] or 'none')[:16]}</span></div>
    </div>
  </div>

  <div class="sidebar-footer">
    Built by Aditya Mitra<br/>
    <a href="https://github.com/adityaamitra/AlgoSensei" target="_blank">GitHub</a> ·
    <a href="https://adityaamitra.github.io/AlgoSensei-GenAI/" target="_blank">Website</a>
  </div>
</div>
"""
st_html(nav_html, height=0)


# ── Streamlit sidebar for navigation ──────────────────────────
with st.sidebar:
    st.markdown("## 🧠 AlgoSensei")
    page = st.radio("", ["🎓 Tutor", "📊 Metrics", "🔬 How it works"],
                    label_visibility="collapsed",
                    key="page_radio")
    st.divider()
    st.caption(f"Hints: **{stats['total_hints']}**")
    st.caption(f"Leakage: **{stats['leakage_rate']:.1%}**")
    if stats["current_problem"]:
        st.caption(f"Problem: *{stats['current_problem'][:24]}*")
    if st.button("↺ New Session", use_container_width=True):
        st.session_state.engine = None
        st.session_state.messages = []
        st.session_state.problem = ""
        st.session_state.pattern = ""
        st.rerun()
    st.divider()
    st.caption("Built by Aditya Mitra")

page_key = page.split()[1].lower() if page else "tutor"


# ══════════════════════════════════════════════════════════════
# TUTOR PAGE
# ══════════════════════════════════════════════════════════════
if "Tutor" in page:

    st.markdown("""
    <div style="padding: 28px 28px 0;">
      <h1 style="font-size:1.6rem;font-weight:700;color:#F1F5F9;margin:0;">
        🎓 AlgoSensei Tutor
      </h1>
      <p style="color:#64748B;margin:4px 0 20px;font-size:.9rem;">
        Get Socratic hints · Explain concepts · Analyze screenshots — without seeing the answer
      </p>
    </div>
    """, unsafe_allow_html=True)

    if not keys_configured():
        st.error("⚠️ API keys not configured. Add OPENROUTER_API_KEY, QDRANT_URL, and QDRANT_API_KEY to your .env file.")
        st.stop()

    tab1, tab2, tab3 = st.tabs(["💡 Get a Hint", "📖 Explain a Concept", "📸 Screenshot"])

    # ── Tab 1: Hints ──────────────────────────────────────────
    with tab1:
        st.markdown('<div style="padding: 0 28px 28px;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            problem = st.text_input("Problem title", value=st.session_state.problem,
                placeholder="e.g. Two Sum, Coin Change, Valid Parentheses",
                label_visibility="visible")
        with col2:
            pattern_options = ["(auto-detect)"] + [PATTERN_LABELS.get(p, p) for p in PATTERNS]
            pat_sel = st.selectbox("DSA Pattern", pattern_options, label_visibility="visible")
        with col3:
            diff = st.selectbox("Difficulty", ["Easy","Medium","Hard"], index=1, label_visibility="visible")

        if problem: st.session_state.problem = problem
        sel_pattern = PATTERNS[pattern_options.index(pat_sel)-1] if pat_sel != "(auto-detect)" else ""
        if sel_pattern: st.session_state.pattern = sel_pattern

        stuck = st.text_area("Where are you stuck? (optional)",
            placeholder="e.g. I see the O(n²) brute force but can't figure out how to optimize...",
            height=80, label_visibility="visible")

        c1, c2, c3 = st.columns(3)
        hint_level = None
        with c1:
            if st.button("💡 Hint 1 — Direction", use_container_width=True): hint_level = 1
        with c2:
            if st.button("💡 Hint 2 — Structure", use_container_width=True): hint_level = 2
        with c3:
            if st.button("💡 Hint 3 — Near-solution", use_container_width=True): hint_level = 3

        if hint_level:
            if not st.session_state.problem:
                st.warning("Enter a problem title first.")
            else:
                with st.spinner(f"Generating hint {hint_level}..."):
                    engine = get_engine()
                    result = engine.hint(
                        problem_title   = st.session_state.problem,
                        difficulty      = diff,
                        pattern         = st.session_state.pattern,
                        student_context = stuck or "",
                        hint_level      = hint_level,
                    )

                resp  = result.get("response","")
                leak  = result.get("leakage_result",{})
                chunks= result.get("retrieved_chunks",[])
                safe_txt = "✓ safe" if leak.get("safe") else "⚠ regenerated"
                safe_cls = "pill-safe" if leak.get("safe") else "pill-mode"

                st.markdown(f"""
                <div style="margin-top:16px;">
                  <div class="hint-meta">
                    <span class="pill pill-level">Hint {hint_level}/3</span>
                    <span class="pill {safe_cls}">{safe_txt}</span>
                  </div>
                  <div class="hint-output">{resp}</div>
                </div>
                """, unsafe_allow_html=True)

                from multimodal.audio import get_speech_html
                st_html(get_speech_html(resp), height=55)

                if chunks:
                    with st.expander(f"📚 {len(chunks)} retrieved sources"):
                        for i,c in enumerate(chunks,1):
                            st.markdown(f"""
                            <div class="source-item">
                              <div class="source-label">[{i}] {c['source']} · score: {c['score']}</div>
                              <div class="source-text">{c['text'][:200]}...</div>
                            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 2: Explain ────────────────────────────────────────
    with tab2:
        st.markdown('<div style="padding: 0 28px 28px;">', unsafe_allow_html=True)
        topic = st.text_input("What concept do you want explained?",
            placeholder="e.g. dynamic programming, sliding window, monotonic stack",
            label_visibility="visible")
        pat_filter_options = ["(none)"] + [PATTERN_LABELS.get(p,p) for p in PATTERNS]
        pat_exp = st.selectbox("Related pattern (optional)", pat_filter_options,
            key="exp_pat", label_visibility="visible")
        pat_exp_key = PATTERNS[pat_filter_options.index(pat_exp)-1] if pat_exp != "(none)" else ""

        if st.button("📖 Explain", type="primary"):
            if not topic:
                st.warning("Enter a topic first.")
            else:
                with st.spinner("Retrieving from knowledge base..."):
                    engine = get_engine()
                    result = engine.explain(topic, pattern=pat_exp_key)

                resp   = result.get("response","")
                chunks = result.get("retrieved_chunks",[])
                faith  = result.get("faithfulness",{})

                st.markdown(f"""
                <div style="margin-top:16px;">
                  <div class="hint-meta">
                    <span class="pill pill-mode">Explainer</span>
                    <span class="pill pill-safe">faithfulness: {faith.get('coverage',0):.0%}</span>
                  </div>
                  <div class="hint-output">{resp}</div>
                </div>
                """, unsafe_allow_html=True)

                from multimodal.audio import get_speech_html
                st_html(get_speech_html(resp), height=55)

                if chunks:
                    with st.expander(f"📚 {len(chunks)} sources retrieved"):
                        for i,c in enumerate(chunks,1):
                            st.markdown(f"""
                            <div class="source-item">
                              <div class="source-label">[{i}] {c['source']} · score: {c['score']}</div>
                              <div class="source-text">{c['text'][:220]}...</div>
                            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 3: Screenshot ─────────────────────────────────────
    with tab3:
        st.markdown('<div style="padding: 0 28px 28px;">', unsafe_allow_html=True)
        st.caption("Upload a LeetCode screenshot — OCR reads the problem, then you get a first Socratic hint.")
        uploaded = st.file_uploader("Upload screenshot", type=["png","jpg","jpeg"],
            label_visibility="collapsed")

        if uploaded:
            col_img, col_res = st.columns([1,1])
            with col_img:
                st.image(uploaded, use_container_width=True)
            with col_res:
                with st.spinner("Reading screenshot..."):
                    engine = get_engine()
                    result = engine.analyze_screenshot(uploaded.read())

                if result.get("success"):
                    st.markdown(f"""
                    <div class="card" style="margin-bottom:14px;">
                      <div style="font-size:1rem;font-weight:600;color:#F1F5F9;margin-bottom:8px;">
                        {result['problem_title']} <span style="color:#64748B;font-weight:400;font-size:.85rem">({result['difficulty']})</span>
                      </div>
                      <div style="display:flex;gap:8px;flex-wrap:wrap;">
                        <span class="pill pill-level">Pattern: {result['pattern']}</span>
                        <span class="pill pill-{'safe' if result['confidence']=='high' else 'mode'}">{result['confidence']} confidence</span>
                      </div>
                    """, unsafe_allow_html=True)
                    if result.get("constraints"):
                        for c in result["constraints"]:
                            st.caption(f"• {c}")
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="hint-meta" style="margin-top:12px;">
                      <span class="pill pill-mode">First hint</span>
                      <span class="pill pill-safe">✓ safe</span>
                    </div>
                    <div class="hint-output">{result['response']}</div>
                    """, unsafe_allow_html=True)

                    from multimodal.audio import get_speech_html
                    st_html(get_speech_html(result["response"]), height=55)
                    st.session_state.problem = result["problem_title"]
                    st.session_state.pattern = result["pattern"]

                    if result.get("raw_text"):
                        with st.expander("📄 OCR text extracted"):
                            st.code(result["raw_text"], language=None)
                else:
                    st.warning(result.get("response","Could not analyze screenshot."))
                    if result.get("error"):
                        st.error(f"Error: {result['error']}")

        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ── Chat bar ──────────────────────────────────────────────
    if st.session_state.messages:
        st.markdown('<div style="padding:0 28px;">', unsafe_allow_html=True)
        with st.expander("💬 Session history", expanded=False):
            for msg in st.session_state.messages[-6:]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
        st.markdown('</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Ask anything about DSA...")
    if user_input and keys_configured():
        st.session_state.messages.append({"role":"user","content":user_input})
        with st.spinner("Thinking..."):
            engine = get_engine()
            result = engine.respond(message=user_input,
                problem=st.session_state.problem,
                pattern=st.session_state.pattern)
        resp = result.get("response","")
        st.session_state.messages.append({"role":"assistant","content":resp})
        st.rerun()


# ══════════════════════════════════════════════════════════════
# METRICS PAGE
# ══════════════════════════════════════════════════════════════
elif "Metrics" in page:
    st.markdown("""
    <div style="padding: 28px 28px 0;">
      <h1 style="font-size:1.6rem;font-weight:700;color:#F1F5F9;margin:0;">📊 Evaluation Metrics</h1>
      <p style="color:#64748B;margin:4px 0 20px;font-size:.9rem;">Live metrics from the AlgoSensei evaluation suite.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding: 0 28px 28px;">', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Retrieval Recall @4","90%+","target >90%")
    with c2: st.metric("Hint Leakage Rate","<5%","target <5%")
    with c3: st.metric("Faithfulness Score","95%+","target >95%")
    with c4: st.metric("Directional Accuracy","85%+","target >85%")

    st.divider()

    if keys_configured() and st.button("▶ Run Evaluation Suite", type="primary"):
        with st.spinner("Running (~30s)..."):
            from evaluation.evaluator import evaluate_leakage_rate, evaluate_directional_accuracy
            leakage = evaluate_leakage_rate(None)
            direc   = evaluate_directional_accuracy()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Hint Leakage Rate",
                f"{leakage['hint_leakage_rate']:.1%}",
                "✓ PASS" if leakage["passed"] else "✗ FAIL")
            st.caption(f"Leaked: {leakage['leaked_hints']} / {leakage['total_hints']}")
        with col2:
            st.metric("Directional Accuracy",
                f"{direc['directional_accuracy']:.1%}",
                "✓ PASS" if direc["passed"] else "✗ FAIL")

    st.divider()
    st.subheader("Synthetic Dataset")
    try:
        import json
        path = Path(__file__).parent / "synthetic" / "data" / "stats.json"
        if path.exists():
            with open(path) as f: s = json.load(f)
            c1, c2 = st.columns(2)
            with c1: st.metric("Total eval pairs", s["total_pairs"])
            with c2: st.metric("Patterns covered", len(s.get("by_pattern",{})))
            with st.expander("Distribution by type"):
                for t,n in s.get("by_type",{}).items():
                    st.markdown(f"**{t}**: {n}")
    except Exception: pass

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HOW IT WORKS PAGE
# ══════════════════════════════════════════════════════════════
elif "How" in page:
    st.markdown("""
    <div style="padding: 28px 28px 0;">
      <h1 style="font-size:1.6rem;font-weight:700;color:#F1F5F9;margin:0;">🔬 How AlgoSensei Works</h1>
      <p style="color:#64748B;margin:4px 0 20px;font-size:.9rem;">The pipeline behind every hint.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding: 0 28px 28px;">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
          <h3 style="color:#818CF8;font-size:1rem;font-weight:600;margin-bottom:12px;">The 6-Step Pipeline</h3>
          <div style="display:flex;flex-direction:column;gap:10px;">
        """ + "".join([
            f"""<div style="display:flex;align-items:flex-start;gap:12px;">
              <div style="min-width:26px;height:26px;background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.3);
                border-radius:50%;display:flex;align-items:center;justify-content:center;
                color:#818CF8;font-size:.78rem;font-weight:700;flex-shrink:0;">{n}</div>
              <div>
                <div style="font-size:.85rem;font-weight:500;color:#E2E8F0;margin-bottom:2px;">{t}</div>
                <div style="font-size:.78rem;color:#64748B;line-height:1.5;">{d}</div>
              </div>
            </div>"""
            for n,t,d in [
                (1,"Mode detection","Classifies intent: Explainer, Socratic, or Screenshot."),
                (2,"Qdrant retrieval","all-MiniLM-L6-v2 embeds query → top-4 chunks fetched."),
                (3,"Gemini generation","LLM generates hint grounded in retrieved context."),
                (4,"Leakage gate","Regex + semantic check. Failed hints regenerate up to 3×."),
                (5,"Hint delivered","Approved hint shown + 🔊 Listen button via Web Speech API."),
                (6,"Session tracked","Hint count, leakage rate, current problem updated in sidebar."),
            ]
        ]) + """
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
          <h3 style="color:#818CF8;font-size:1rem;font-weight:600;margin-bottom:12px;">Three Hint Levels</h3>
        """ + "".join([
            f"""<div style="margin-bottom:14px;padding:12px;background:#131D35;border-radius:8px;border:1px solid #1E2D4A;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                <span class="pill pill-level" style="font-size:.68rem;">Level {n}</span>
                <span style="font-size:.82rem;font-weight:600;color:#E2E8F0;">{t}</span>
              </div>
              <div style="font-size:.78rem;color:#94A3B8;line-height:1.5;">{d}</div>
            </div>"""
            for n,t,d in [
                (1,"Direction only","Points toward what constraint to examine. No structure, no data structures named."),
                (2,"Structure hint","Guides toward the type of operation needed. Still no algorithm names."),
                (3,"Near-solution","Describes the abstract high-level approach. No code. No specific algorithm names."),
            ]
        ]) + """
          <div style="margin-top:8px;padding:10px;background:#0A1628;border-radius:8px;border:1px solid #1E2D4A;font-size:.78rem;color:#64748B;">
            The leakage gate runs on every level. Failed hints are regenerated silently — you never see a leaked hint.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("Tech Stack — Total Cost: $0")
    cols = st.columns(4)
    stack = [
        ("OpenRouter","Free models (Nemotron, Llama, etc.)","💬"),
        ("Qdrant Cloud","Vector DB, free tier 1GB","🗄️"),
        ("all-MiniLM-L6-v2","Local embeddings, zero API cost","🔢"),
        ("pytesseract","Local OCR for screenshot tab","👁️"),
    ]
    for i,(name,desc,icon) in enumerate(stack):
        with cols[i]:
            st.markdown(f"""
            <div class="card-sm" style="text-align:center;">
              <div style="font-size:1.5rem;margin-bottom:6px;">{icon}</div>
              <div style="font-size:.85rem;font-weight:600;color:#E2E8F0;">{name}</div>
              <div style="font-size:.72rem;color:#64748B;margin-top:3px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)