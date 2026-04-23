import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import streamlit as st
from streamlit.components.v1 import html as st_html

st.set_page_config(
    page_title="AlgoSensei",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

#MainMenu,footer,header,.stDeployButton{visibility:hidden!important;display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stSidebar"]{display:none!important;}
[data-testid="stAppViewContainer"]>.main{padding:0!important;}
*{box-sizing:border-box;margin:0;padding:0;}
html,body,.stApp{
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif!important;
  background:#1A1A1A!important;
  color:#EFF1F1!important;
}

/* ── Topnav ── */
.lc-nav{
  background:#282828;
  border-bottom:1px solid #3E3E3E;
  height:50px;
  display:flex;align-items:center;
  padding:0 20px;
  gap:0;
  position:sticky;top:0;z-index:100;
}
.lc-nav-logo{
  display:flex;align-items:center;gap:8px;
  font-size:1.1rem;font-weight:700;color:#FFA116;
  margin-right:32px;text-decoration:none;
  flex-shrink:0;
}
.lc-nav-logo span{color:#EFF1F1;}
.lc-nav-links{display:flex;align-items:center;gap:2px;flex:1;}
.lc-nav-btn{
  padding:6px 14px;border-radius:5px;
  font-size:.85rem;font-weight:500;color:#ADB0B1;
  background:transparent;border:none;cursor:pointer;
  transition:all .15s;white-space:nowrap;
}
.lc-nav-btn:hover{background:#3E3E3E;color:#EFF1F1;}
.lc-nav-btn.active{color:#FFA116;background:rgba(255,161,22,.08);}
.lc-nav-right{
  display:flex;align-items:center;gap:10px;margin-left:auto;
}
.lc-streak{
  display:flex;align-items:center;gap:5px;
  font-size:.78rem;color:#ADB0B1;
  background:#1A1A1A;border:1px solid #3E3E3E;
  border-radius:20px;padding:4px 12px;
}

/* ── Layout ── */
.lc-body{
  display:grid;
  grid-template-columns:360px 1fr;
  height:calc(100vh - 50px);
  overflow:hidden;
}
.lc-left{
  background:#282828;
  border-right:1px solid #3E3E3E;
  overflow-y:auto;
  display:flex;flex-direction:column;
}
.lc-right{
  background:#1A1A1A;
  overflow-y:auto;
  display:flex;flex-direction:column;
}

/* ── Problem header ── */
.prob-header{
  padding:18px 20px 14px;
  border-bottom:1px solid #3E3E3E;
}
.prob-title{
  font-size:1.05rem;font-weight:600;color:#EFF1F1;
  margin-bottom:10px;
}
.prob-tags{display:flex;gap:6px;flex-wrap:wrap;}
.tag{
  border-radius:4px;padding:3px 8px;
  font-size:.72rem;font-weight:500;
}
.tag-easy{background:rgba(44,187,93,.15);color:#2CBB5D;}
.tag-medium{background:rgba(255,161,22,.15);color:#FFA116;}
.tag-hard{background:rgba(255,55,95,.15);color:#FF375F;}
.tag-pattern{background:rgba(96,165,250,.1);color:#60A5FA;}

/* ── Tabs ── */
.lc-tabs{
  display:flex;
  border-bottom:1px solid #3E3E3E;
  background:#282828;
  flex-shrink:0;
}
.lc-tab{
  padding:12px 18px;font-size:.85rem;font-weight:500;
  color:#ADB0B1;border:none;background:transparent;
  cursor:pointer;border-bottom:2px solid transparent;
  transition:all .15s;white-space:nowrap;
}
.lc-tab:hover{color:#EFF1F1;}
.lc-tab.active{color:#EFF1F1;border-bottom-color:#FFA116;}

/* ── Description area ── */
.desc-area{
  padding:18px 20px;
  flex:1;
  font-size:.88rem;
  color:#ADB0B1;
  line-height:1.7;
}
.desc-area p{margin-bottom:12px;}
.desc-section{
  font-size:.72rem;font-weight:600;color:#EFF1F1;
  text-transform:uppercase;letter-spacing:.06em;
  margin:14px 0 6px;
}
.example-box{
  background:#1A1A1A;border:1px solid #3E3E3E;
  border-radius:6px;padding:12px 14px;
  font-family:'JetBrains Mono','Courier New',monospace;
  font-size:.8rem;color:#ADB0B1;margin-bottom:8px;
}

/* ── Hint panel ── */
.hint-panel{
  flex:1;padding:20px 24px;
}
.hint-toolbar{
  display:flex;align-items:center;gap:10px;
  margin-bottom:16px;flex-wrap:wrap;
}
.lc-hint-btn{
  padding:7px 16px;border-radius:5px;
  font-size:.82rem;font-weight:500;
  border:1px solid #3E3E3E;
  background:#282828;color:#ADB0B1;
  cursor:pointer;transition:all .15s;
  white-space:nowrap;
}
.lc-hint-btn:hover{background:#3E3E3E;color:#EFF1F1;border-color:#5C5C5C;}
.lc-hint-btn.primary{
  background:#FFA116;color:#1A1A1A;
  border-color:#FFA116;font-weight:600;
}
.lc-hint-btn.primary:hover{background:#FFB84D;border-color:#FFB84D;}

/* ── Hint output ── */
.hint-box{
  background:#282828;
  border:1px solid #3E3E3E;
  border-radius:8px;
  padding:18px 20px;
  margin-top:14px;
  font-size:.9rem;
  line-height:1.75;
  color:#EFF1F1;
  position:relative;
}
.hint-box-label{
  display:flex;align-items:center;gap:8px;
  margin-bottom:12px;
}
.hint-num{
  background:#FFA116;color:#1A1A1A;
  border-radius:4px;padding:2px 8px;
  font-size:.72rem;font-weight:700;
}
.safe-dot{
  width:7px;height:7px;background:#2CBB5D;
  border-radius:50%;display:inline-block;
}

/* ── Source cards ── */
.source-card{
  background:#1A1A1A;border:1px solid #3E3E3E;
  border-radius:6px;padding:10px 14px;margin-bottom:6px;
}
.source-title{font-size:.72rem;color:#60A5FA;font-weight:600;margin-bottom:4px;}
.source-body{font-size:.78rem;color:#ADB0B1;line-height:1.5;}

/* ── Status bar ── */
.status-bar{
  background:#282828;border-top:1px solid #3E3E3E;
  padding:8px 20px;
  display:flex;align-items:center;gap:16px;
  font-size:.75rem;color:#ADB0B1;
  flex-shrink:0;
}
.status-item{display:flex;align-items:center;gap:5px;}
.status-dot{width:7px;height:7px;border-radius:50%;}
.dot-green{background:#2CBB5D;}
.dot-orange{background:#FFA116;}

/* ── Streamlit widget overrides ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea{
  background:#1A1A1A!important;
  border:1px solid #3E3E3E!important;
  color:#EFF1F1!important;
  border-radius:5px!important;
  font-size:.88rem!important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus{
  border-color:#FFA116!important;
  box-shadow:0 0 0 2px rgba(255,161,22,.2)!important;
}
div[data-testid="stSelectbox"] > div > div{
  background:#1A1A1A!important;
  border:1px solid #3E3E3E!important;
  color:#EFF1F1!important;
  border-radius:5px!important;
}
.stButton>button{
  background:#FFA116!important;color:#1A1A1A!important;
  border:none!important;border-radius:5px!important;
  font-weight:600!important;font-size:.85rem!important;
  padding:8px 18px!important;
  transition:all .2s!important;
}
.stButton>button:hover{background:#FFB84D!important;transform:translateY(-1px)!important;}
.stButton>button[kind="secondary"]{
  background:#282828!important;color:#ADB0B1!important;
  border:1px solid #3E3E3E!important;
}
.stButton>button[kind="secondary"]:hover{
  background:#3E3E3E!important;color:#EFF1F1!important;
}
div[data-testid="stTabs"] [role="tablist"]{
  background:transparent!important;
  border-bottom:1px solid #3E3E3E!important;
  gap:0!important;
}
div[data-testid="stTabs"] button[role="tab"]{
  background:transparent!important;color:#ADB0B1!important;
  border-radius:0!important;font-weight:500!important;
  font-size:.85rem!important;padding:10px 18px!important;
  border:none!important;border-bottom:2px solid transparent!important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{
  color:#EFF1F1!important;border-bottom-color:#FFA116!important;
}
div[data-testid="stTabs"] [data-testid="stTabsContent"]{padding-top:16px!important;}
div[data-testid="stExpander"]{
  background:#282828!important;border:1px solid #3E3E3E!important;
  border-radius:6px!important;
}
div[data-testid="stExpander"] summary{color:#ADB0B1!important;font-size:.82rem!important;}
div[data-testid="stMetric"]{
  background:#282828!important;border:1px solid #3E3E3E!important;
  border-radius:8px!important;padding:14px!important;
}
div[data-testid="stMetricLabel"]{color:#ADB0B1!important;font-size:.78rem!important;}
div[data-testid="stMetricValue"]{color:#FFA116!important;font-size:1.5rem!important;font-weight:700!important;}
div[data-testid="stFileUploader"]{
  background:#282828!important;border:1px dashed #3E3E3E!important;
  border-radius:6px!important;
}
div[data-testid="stChatInput"] > div{
  background:#282828!important;border:1px solid #3E3E3E!important;
  border-radius:8px!important;
}
div[data-testid="stChatInput"] textarea{color:#EFF1F1!important;}
div[data-testid="stChatMessage"]{
  background:#282828!important;border:1px solid #3E3E3E!important;
  border-radius:8px!important;margin-bottom:6px!important;
}
div[data-testid="stAlert"]{border-radius:6px!important;}
hr{border-color:#3E3E3E!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:#1A1A1A;}
::-webkit-scrollbar-thumb{background:#3E3E3E;border-radius:4px;}
::-webkit-scrollbar-thumb:hover{background:#5C5C5C;}
label[data-testid="stWidgetLabel"]{color:#ADB0B1!important;font-size:.82rem!important;}
</style>
""", unsafe_allow_html=True)

# ── State ────────────────────────────────────────────────────
def init():
    for k,v in {
        "page":"tutor","engine":None,"messages":[],
        "problem":"","pattern":"","diff":"Medium",
        "last_hint":None,
    }.items():
        if k not in st.session_state: st.session_state[k]=v
init()

PATTERNS = ["arrays_hashing","two_pointers","sliding_window","stack","binary_search",
    "linked_list","trees","tries","heap_priority_queue","backtracking",
    "graphs","dynamic_programming_1d","dynamic_programming_2d","greedy"]
PAT_LABEL = {
    "arrays_hashing":"Arrays & Hashing","two_pointers":"Two Pointers",
    "sliding_window":"Sliding Window","stack":"Stack","binary_search":"Binary Search",
    "linked_list":"Linked List","trees":"Trees","tries":"Tries",
    "heap_priority_queue":"Heap/PQ","backtracking":"Backtracking","graphs":"Graphs",
    "dynamic_programming_1d":"DP 1D","dynamic_programming_2d":"DP 2D","greedy":"Greedy",
}

def keys_ok():
    from config import OPENROUTER_API_KEY,QDRANT_URL,QDRANT_API_KEY
    return bool(OPENROUTER_API_KEY and QDRANT_URL and QDRANT_API_KEY)

def engine():
    if st.session_state.engine is None:
        from engine.tutor import AlgoSenseiEngine
        st.session_state.engine = AlgoSenseiEngine()
    return st.session_state.engine

def stats():
    if st.session_state.engine:
        return st.session_state.engine.get_session_stats()
    return {"total_hints":0,"leakage_rate":0.0,"current_problem":"","hint_level":0,"mode_counts":{}}

# ── Topnav ───────────────────────────────────────────────────
s = stats()
st.markdown(f"""
<div class="lc-nav">
  <div class="lc-nav-logo">🧠 <span>AlgoSensei</span></div>
  <div class="lc-nav-links">
    <button class="lc-nav-btn {'active' if st.session_state.page=='tutor' else ''}"
      onclick="window.location.reload()">Tutor</button>
  </div>
  <div class="lc-nav-right">
    <div class="lc-streak">
      <span class="safe-dot"></span>
      Leakage: {s['leakage_rate']:.1%} &nbsp;|&nbsp; Hints: {s['total_hints']}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar nav ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 AlgoSensei")
    page = st.radio("", ["🎓 Tutor","📊 Metrics","🔬 How it works"],
        label_visibility="collapsed", key="page_radio")
    st.divider()
    if st.button("↺ New Session", use_container_width=True):
        st.session_state.engine=None
        st.session_state.messages=[]
        st.session_state.problem=""
        st.session_state.last_hint=None
        st.rerun()
    st.caption(f"Hints: **{s['total_hints']}** · Leakage: **{s['leakage_rate']:.1%}**")

# ══════════════════════════════════════════════════════════════
if "Tutor" in page:

    # ── Left panel ────────────────────────────────────────────
    left, right = st.columns([4, 5])

    with left:
        st.markdown('<div style="background:#282828;border-right:1px solid #3E3E3E;padding:0;">', unsafe_allow_html=True)

        # Problem setup
        st.markdown('<div style="padding:16px 16px 12px;border-bottom:1px solid #3E3E3E;">', unsafe_allow_html=True)
        problem = st.text_input("Problem", value=st.session_state.problem,
            placeholder="e.g. Two Sum", label_visibility="visible")
        if problem: st.session_state.problem = problem

        c1, c2 = st.columns(2)
        with c1:
            diff = st.selectbox("Difficulty", ["Easy","Medium","Hard"], index=1,
                label_visibility="visible")
            st.session_state.diff = diff
        with c2:
            pat_opts = ["auto"] + list(PAT_LABEL.values())
            pat_sel = st.selectbox("Pattern", pat_opts, label_visibility="visible")
            if pat_sel != "auto":
                st.session_state.pattern = PATTERNS[list(PAT_LABEL.values()).index(pat_sel)]
            else:
                st.session_state.pattern = ""

        if st.session_state.problem:
            diff_class = {"Easy":"tag-easy","Medium":"tag-medium","Hard":"tag-hard"}.get(diff,"tag-medium")
            pat_display = PAT_LABEL.get(st.session_state.pattern, "auto-detect")
            st.markdown(f"""
            <div class="prob-tags" style="margin-top:10px;">
              <span class="tag {diff_class}">{diff}</span>
              <span class="tag tag-pattern">{pat_display}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Tabs: Description / Hint / Explain
        tab_d, tab_h, tab_e = st.tabs(["📋 Problem", "💡 Hint", "📖 Explain"])

        with tab_d:
            st.markdown('<div style="padding:4px 4px;">', unsafe_allow_html=True)
            stuck = st.text_area("Where are you stuck?",
                placeholder="Describe what you've tried so far...",
                height=120, label_visibility="visible")

            c1,c2,c3 = st.columns(3)
            hint_level = None
            with c1:
                if st.button("Hint 1", use_container_width=True, help="Direction only"):
                    hint_level = 1
            with c2:
                if st.button("Hint 2", use_container_width=True, help="Structure"):
                    hint_level = 2
            with c3:
                if st.button("Hint 3", use_container_width=True, help="Near-solution"):
                    hint_level = 3

            if hint_level:
                if not st.session_state.problem:
                    st.warning("Enter a problem name above.")
                else:
                    with st.spinner(f"Generating hint {hint_level}..."):
                        r = engine().hint(
                            problem_title=st.session_state.problem,
                            difficulty=diff,
                            pattern=st.session_state.pattern,
                            student_context=stuck or "",
                            hint_level=hint_level,
                        )
                    st.session_state.last_hint = r
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_h:
            st.markdown('<div style="padding:4px;">', unsafe_allow_html=True)
            # Next hint button
            if st.session_state.problem:
                if st.button("➡ Next Hint", use_container_width=True):
                    with st.spinner("Generating..."):
                        r = engine().hint(
                            problem_title=st.session_state.problem,
                            difficulty=st.session_state.diff,
                            pattern=st.session_state.pattern,
                        )
                    st.session_state.last_hint = r
                    st.rerun()
            st.caption("Hints progress through levels 1→2→3 automatically.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_e:
            st.markdown('<div style="padding:4px;">', unsafe_allow_html=True)
            concept = st.text_input("Concept to explain",
                placeholder="e.g. dynamic programming, sliding window",
                label_visibility="visible")
            if st.button("Explain", use_container_width=True):
                if concept:
                    with st.spinner("Retrieving..."):
                        r = engine().explain(concept, pattern=st.session_state.pattern)
                    st.session_state.last_hint = r
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Right panel ───────────────────────────────────────────
    with right:
        if not keys_ok():
            st.markdown("""
            <div style="padding:40px 24px;">
              <div style="background:#282828;border:1px solid #FFA116;border-radius:8px;padding:24px;">
                <h3 style="color:#FFA116;margin-bottom:12px;">⚙️ Setup Required</h3>
                <p style="color:#ADB0B1;font-size:.88rem;line-height:1.6;">
                  Add your API keys to the <code>.env</code> file:<br/><br/>
                  <code>OPENROUTER_API_KEY=sk-or-v1-...</code><br/>
                  <code>QDRANT_URL=https://...</code><br/>
                  <code>QDRANT_API_KEY=...</code>
                </p>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            result = st.session_state.last_hint
            if result is None:
                # Welcome state
                st.markdown("""
                <div style="padding:48px 32px;text-align:center;">
                  <div style="font-size:3rem;margin-bottom:16px;">🧠</div>
                  <h2 style="color:#EFF1F1;font-size:1.3rem;font-weight:600;margin-bottom:10px;">
                    Ready to tackle a problem?
                  </h2>
                  <p style="color:#ADB0B1;font-size:.9rem;line-height:1.7;max-width:400px;margin:0 auto 24px;">
                    Enter a problem name on the left and click <strong style="color:#FFA116">Hint 1</strong> to get started.
                    AlgoSensei will guide you toward the answer — without giving it away.
                  </p>
                  <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
                    <div style="background:#282828;border:1px solid #3E3E3E;border-radius:8px;padding:12px 16px;text-align:left;min-width:160px;">
                      <div style="color:#FFA116;font-size:.72rem;font-weight:600;margin-bottom:4px;">HINT 1</div>
                      <div style="color:#ADB0B1;font-size:.8rem;">Direction only</div>
                    </div>
                    <div style="background:#282828;border:1px solid #3E3E3E;border-radius:8px;padding:12px 16px;text-align:left;min-width:160px;">
                      <div style="color:#FFA116;font-size:.72rem;font-weight:600;margin-bottom:4px;">HINT 2</div>
                      <div style="color:#ADB0B1;font-size:.8rem;">Structure hint</div>
                    </div>
                    <div style="background:#282828;border:1px solid #3E3E3E;border-radius:8px;padding:12px 16px;text-align:left;min-width:160px;">
                      <div style="color:#FFA116;font-size:.72rem;font-weight:600;margin-bottom:4px;">HINT 3</div>
                      <div style="color:#ADB0B1;font-size:.8rem;">Near-solution</div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                resp   = result.get("response","")
                mode   = result.get("mode","socratic")
                level  = result.get("hint_level","")
                leak   = result.get("leakage_result",{})
                chunks = result.get("retrieved_chunks",[])

                level_txt = f"Hint {level}/3" if level else mode.title()
                safe_txt  = "✓ Leakage check passed" if leak.get("safe") else "⚠ Regenerated"
                safe_col  = "#2CBB5D" if leak.get("safe") else "#FFA116"

                st.markdown(f"""
                <div style="padding:20px 24px;">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap;">
                    <span style="background:#FFA116;color:#1A1A1A;border-radius:4px;padding:3px 10px;font-size:.72rem;font-weight:700;">{level_txt}</span>
                    <span style="color:{safe_col};font-size:.75rem;">{safe_txt}</span>
                    <span style="color:#5C5C5C;font-size:.75rem;">· {len(chunks)} sources</span>
                  </div>
                  <div style="background:#282828;border:1px solid #3E3E3E;border-left:3px solid #FFA116;
                    border-radius:0 8px 8px 0;padding:18px 20px;
                    font-size:.92rem;line-height:1.8;color:#EFF1F1;">
                    {resp}
                  </div>
                </div>""", unsafe_allow_html=True)

                from multimodal.audio import get_speech_html
                st_html(get_speech_html(resp, "🔊 Listen"), height=55)

                if chunks:
                    with st.expander(f"📚 Retrieved sources ({len(chunks)})", expanded=False):
                        for i,c in enumerate(chunks,1):
                            st.markdown(f"""
                            <div class="source-card">
                              <div class="source-title">[{i}] {c['source']} · {c['score']}</div>
                              <div class="source-body">{c['text'][:200]}...</div>
                            </div>""", unsafe_allow_html=True)

        # ── Chat bar ──────────────────────────────────────────
        if keys_ok():
            st.markdown('<div style="padding:0 24px;">', unsafe_allow_html=True)
            if st.session_state.messages:
                with st.expander("💬 Session history", expanded=False):
                    for msg in st.session_state.messages[-4:]:
                        with st.chat_message(msg["role"]):
                            st.markdown(msg["content"])
            user_input = st.chat_input("Ask anything about DSA...")
            if user_input:
                st.session_state.messages.append({"role":"user","content":user_input})
                with st.spinner("Thinking..."):
                    r = engine().respond(message=user_input,
                        problem=st.session_state.problem,
                        pattern=st.session_state.pattern)
                resp = r.get("response","")
                st.session_state.last_hint = r
                st.session_state.messages.append({"role":"assistant","content":resp})
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Screenshot section ────────────────────────────────────
    st.divider()
    st.markdown("#### 📸 Upload a Screenshot")
    up_col, res_col = st.columns([1,1])
    with up_col:
        uploaded = st.file_uploader("", type=["png","jpg","jpeg"],
            label_visibility="collapsed")
    if uploaded and keys_ok():
        with up_col:
            st.image(uploaded, use_container_width=True)
        with res_col:
            with st.spinner("Analyzing..."):
                r = engine().analyze_screenshot(uploaded.read())
            if r.get("success"):
                diff_class = {"Easy":"tag-easy","Medium":"tag-medium","Hard":"tag-hard"}.get(r.get("difficulty",""),"tag-medium")
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                  <div style="font-size:1rem;font-weight:600;color:#EFF1F1;margin-bottom:8px;">
                    {r['problem_title']}
                  </div>
                  <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px;">
                    <span class="tag {diff_class}">{r['difficulty']}</span>
                    <span class="tag tag-pattern">{r['pattern']}</span>
                    <span class="tag" style="background:rgba(52,211,153,.1);color:#34D399;">{r['confidence']} confidence</span>
                  </div>
                </div>
                <div style="background:#282828;border:1px solid #3E3E3E;border-left:3px solid #FFA116;
                  border-radius:0 8px 8px 0;padding:16px 18px;font-size:.88rem;line-height:1.75;color:#EFF1F1;">
                  {r['response']}
                </div>""", unsafe_allow_html=True)
                from multimodal.audio import get_speech_html
                st_html(get_speech_html(r["response"]), height=55)
                st.session_state.problem = r["problem_title"]
                st.session_state.pattern = r["pattern"]
            else:
                st.warning(r.get("response","Could not analyze."))
                if r.get("error"): st.error(r["error"])


# ══════════════════════════════════════════════════════════════
elif "Metrics" in page:
    st.markdown('<div style="padding:24px;">', unsafe_allow_html=True)
    st.markdown("### 📊 Evaluation Metrics")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Retrieval Recall @4",">90%","target")
    with c2: st.metric("Hint Leakage Rate","<5%","target")
    with c3: st.metric("Faithfulness",">95%","target")
    with c4: st.metric("Directional",">85%","target")
    st.divider()
    if keys_ok() and st.button("▶ Run Evaluation", type="primary"):
        with st.spinner("Running..."):
            from evaluation.evaluator import evaluate_leakage_rate, evaluate_directional_accuracy
            l = evaluate_leakage_rate(None)
            d = evaluate_directional_accuracy()
        st.metric("Leakage Rate", f"{l['hint_leakage_rate']:.1%}", "PASS" if l["passed"] else "FAIL")
        st.metric("Directional",  f"{d['directional_accuracy']:.1%}", "PASS" if d["passed"] else "FAIL")
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
elif "How" in page:
    st.markdown('<div style="padding:24px;">', unsafe_allow_html=True)
    st.markdown("### 🔬 How AlgoSensei Works")
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div style="background:#282828;border:1px solid #3E3E3E;border-radius:8px;padding:18px;">
          <div style="font-size:.85rem;font-weight:600;color:#FFA116;margin-bottom:12px;">THE PIPELINE</div>
        """ + "".join([
            f"""<div style="display:flex;gap:12px;margin-bottom:12px;align-items:flex-start;">
              <span style="background:#FFA116;color:#1A1A1A;border-radius:4px;padding:2px 7px;font-size:.7rem;font-weight:700;flex-shrink:0;margin-top:1px;">{n}</span>
              <div>
                <div style="font-size:.84rem;font-weight:600;color:#EFF1F1;">{t}</div>
                <div style="font-size:.78rem;color:#ADB0B1;line-height:1.5;margin-top:2px;">{d}</div>
              </div>
            </div>"""
            for n,t,d in [
                ("1","Mode detection","Intent classified: Explainer, Socratic, or Screenshot."),
                ("2","Qdrant retrieval","Query embedded → top-4 KB chunks fetched via cosine similarity."),
                ("3","LLM generation","Hint generated using retrieved context as grounding."),
                ("4","Leakage gate","Regex + semantic check. Failed hints regenerate up to 3×."),
                ("5","Audio output","Web Speech API speaks the hint at 0.88× speed."),
            ]
        ]) + "</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="background:#282828;border:1px solid #3E3E3E;border-radius:8px;padding:18px;">
          <div style="font-size:.85rem;font-weight:600;color:#FFA116;margin-bottom:12px;">HINT LEVELS</div>
        """ + "".join([
            f"""<div style="background:#1A1A1A;border:1px solid #3E3E3E;border-radius:6px;padding:12px;margin-bottom:8px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">
                <span style="background:#FFA116;color:#1A1A1A;border-radius:3px;padding:1px 7px;font-size:.68rem;font-weight:700;">Level {n}</span>
                <span style="font-size:.82rem;font-weight:600;color:#EFF1F1;">{t}</span>
              </div>
              <div style="font-size:.78rem;color:#ADB0B1;line-height:1.5;">{d}</div>
            </div>"""
            for n,t,d in [
                (1,"Direction only","Points toward what to examine. No structure, no algorithm names."),
                (2,"Structure hint","Guides toward the type of operation needed."),
                (3,"Near-solution","Describes the abstract approach. Still no code, no algorithm names."),
            ]
        ]) + "</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)