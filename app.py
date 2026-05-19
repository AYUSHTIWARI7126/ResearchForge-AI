import streamlit as st
import time
from agents import build_search_agent, writer_chain, critic_chain

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="ResearchForge AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: white;
}

.stApp {
    background: #0f1117;
    background-image:
        radial-gradient(circle at top left, rgba(255,140,50,0.12), transparent 40%),
        radial-gradient(circle at bottom right, rgba(255,90,26,0.10), transparent 40%);
}

/* Hide Streamlit */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* Hero */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 4rem;
    font-weight: 800;
    color: white;
    text-align: center;
    margin-bottom: 0.5rem;
}

.hero-title span {
    color: #ff8c32;
}

.hero-sub {
    text-align: center;
    color: #d0d0d0;
    font-size: 1.05rem;
    max-width: 700px;
    margin: auto;
    line-height: 1.8;
    margin-bottom: 2rem;
}

/* Section title */
.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

/* Input box */
.stTextInput input {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border: 1px solid rgba(255,140,50,0.3) !important;
    border-radius: 12px !important;
    padding: 0.9rem !important;
}

.stTextInput input::placeholder {
    color: #aaaaaa !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%);
    color: black;
    border: none;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    font-weight: 700;
    width: 100%;
    font-size: 1rem;
}

/* Cards */
.card {
    background: rgba(22,22,30,0.95);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}

/* Result panels */
.result-panel {
    background: rgba(22,22,30,0.97);
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid rgba(255,140,50,0.2);
    margin-top: 1rem;
}

/* Markdown */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    color: #f5f5f5 !important;
    line-height: 1.8 !important;
    font-size: 1rem !important;
}

[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    color: #ffb067 !important;
}

/* Remove white blocks */
[data-testid="stMarkdownContainer"] {
    background: transparent !important;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 3rem;
    color: #777;
    font-size: 0.8rem;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="hero-title">
        Research<span>Forge</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-sub">
        Autonomous multi-agent AI platform that searches,
        analyzes, synthesizes, and critiques information
        to generate high-quality research reports.
    </div>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────

if "results" not in st.session_state:
    st.session_state.results = {}

# ─────────────────────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────────────────────

left, right = st.columns([5, 4])

# LEFT

with left:

    st.markdown(
        '<div class="section-title">Research Topic</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "",
        placeholder="e.g. Future of AI agents in healthcare"
    )

    run_btn = st.button("⚡ Generate AI Research Report")

# RIGHT

with right:

    st.markdown(
        '<div class="section-title">Pipeline Status</div>',
        unsafe_allow_html=True
    )

    steps = [
        ("01", "Search Agent", "Searches latest information"),
        ("02", "Processing Layer", "Processes research content"),
        ("03", "Writer Chain", "Creates final report"),
        ("04", "Critic Chain", "Reviews report quality"),
    ]

    for num, title, desc in steps:

        st.markdown(
            f"""
            <div class="card">
                <h4>{num} · {title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────────────────────────
# RUN PIPELINE
# ─────────────────────────────────────────────────────────────

if run_btn:

    if not topic.strip():

        st.warning("Please enter a topic.")

    else:

        results = {}

        # SEARCH AGENT
        with st.spinner("🔍 Search Agent Working..."):

            search_agent = build_search_agent()

            sr = search_agent.invoke({
                "messages": [
                    ("user", f"Find detailed information about: {topic}")
                ]
            })

            results["search"] = sr["messages"][-1].content

        # SIMPLIFIED READER
        with st.spinner("📄 Processing Research Content..."):

            results["reader"] = results["search"][:600]

        # WRITER
        with st.spinner("✍️ Writing Research Report..."):

            combined = f"""
SEARCH RESULTS:
{results['search']}

PROCESSED CONTENT:
{results['reader']}
"""

            results["writer"] = writer_chain.invoke({
                "topic": topic,
                "research": combined
            })

        # CRITIC
        with st.spinner("🧐 Reviewing Report..."):

            results["critic"] = critic_chain.invoke({
                "report": results["writer"]
            })

        st.session_state.results = results

# ─────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────

r = st.session_state.results

if r:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">Final Research Report</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="result-panel">',
        unsafe_allow_html=True
    )

    st.markdown(r["writer"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        "⬇ Download Report",
        data=r["writer"],
        file_name=f"research_report_{int(time.time())}.md",
        mime="text/markdown"
    )

    st.markdown(
        '<div class="section-title" style="margin-top:2rem;">Critic Feedback</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="result-panel">',
        unsafe_allow_html=True
    )

    st.markdown(r["critic"])

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="footer">
        ResearchForge AI · Powered by Groq + LangChain + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)