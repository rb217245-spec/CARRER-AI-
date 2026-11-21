"""
CareerAI — Smart Resume Analyzer & Job Recommendation System (Streamlit Edition)
Run with: streamlit run app.py
"""
import copy
import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.sample_data import DEMO_RESUME_FILENAME, DEMO_RESUME_TEXT, SAMPLE_JOB_ROLES
from engine.exporter import generate_markdown_report, generate_pdf_report
from engine.parser import extract_text_from_file, parse_resume
from engine.recommender import analyze_skill_gap, generate_learning_roadmap, recommend_jobs
from engine.scoring import evaluate_resume
from engine.skills import all_known_skills, extract_skills, normalize_skill

# ---------------------------------------------------------------------------
# Page Configuration & Custom Modern SaaS Styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CareerAI — Smart Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Main container spacing */
.block-container {
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    max-width: 1240px;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    color: #F8FAFC;
}
section[data-testid="stSidebar"] * {
    color: #F1F5F9 !important;
}
section[data-testid="stSidebar"] .stRadio > div {
    gap: 0.35rem;
}
section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 0.55rem 0.85rem;
    transition: all 0.2s ease;
    cursor: pointer;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(59, 130, 246, 0.22);
    border-color: rgba(96, 165, 250, 0.5);
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.14);
}
section[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #2563EB 0%, #4F46E5 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* Hero Banner */
.hero-banner {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 55%, #2563EB 100%);
    padding: 1.75rem 2rem;
    border-radius: 18px;
    color: #FFFFFF;
    margin-bottom: 1.5rem;
    box-shadow: 0 12px 30px rgba(30, 58, 138, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.12);
}
.hero-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.15);
    color: #E0F2FE;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    letter-spacing: 0.04em;
    margin-bottom: 0.55rem;
}
.hero-title {
    font-size: 1.85rem;
    font-weight: 800;
    margin: 0 0 0.35rem 0;
    letter-spacing: -0.02em;
    color: #FFFFFF;
}
.hero-sub {
    font-size: 0.98rem;
    color: #CBD5E1;
    margin: 0;
}

/* KPI Metric Cards */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.15rem 1.25rem;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08);
}
.kpi-label {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748B;
    margin-bottom: 0.35rem;
}
.kpi-value {
    font-size: 1.75rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.15;
}
.kpi-delta {
    font-size: 0.82rem;
    font-weight: 500;
    margin-top: 0.35rem;
    color: #2563EB;
}

/* Content Cards */
.section-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
}

/* Skill Chips */
.chip-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-top: 0.4rem;
}
.skill-chip {
    display: inline-flex;
    align-items: center;
    padding: 0.3rem 0.72rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    border: 1px solid transparent;
}
.chip-prog { background: #EFF6FF; color: #1D4ED8; border-color: #BFDBFE; }
.chip-ds   { background: #F5F3FF; color: #6D28D9; border-color: #DDD6FE; }
.chip-web  { background: #ECFDF5; color: #047857; border-color: #A7F3D0; }
.chip-soft { background: #FFFBEB; color: #B45309; border-color: #FDE68A; }
.chip-miss { background: #FEF2F2; color: #B91C1C; border-color: #FECACA; }
.chip-have { background: #ECFDF5; color: #065F46; border-color: #6EE7B7; }

/* Job Card */
.job-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 5px solid #2563EB;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
}
.match-pill {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.85rem;
}
.match-high { background: #DCFCE7; color: #15803D; }
.match-mid  { background: #DBEAFE; color: #1D4ED8; }
.match-low  { background: #FEF3C7; color: #B45309; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------
def run_full_analysis(raw_text: str, filename: str, preserve_manual_skills: bool = False):
    parsed = parse_resume(raw_text)
    auto_skills = extract_skills(raw_text)
    if preserve_manual_skills and "skills" in st.session_state:
        manual_only = [s for s in st.session_state["skills"] if s.get("user_added")]
        existing_lower = {s["name"].lower() for s in auto_skills}
        for m in manual_only:
            if m["name"].lower() not in existing_lower:
                auto_skills.append(m)

    st.session_state["raw_text"] = raw_text
    st.session_state["filename"] = filename
    st.session_state["parsed"] = parsed
    st.session_state["skills"] = auto_skills
    recompute_downstream()


def recompute_downstream():
    raw_text = st.session_state["raw_text"]
    parsed = st.session_state["parsed"]
    skills = st.session_state["skills"]
    roles = st.session_state["job_roles"]

    score_report = evaluate_resume(raw_text, parsed, skills)
    recommendations = recommend_jobs(raw_text, skills, roles)

    st.session_state["score_report"] = score_report
    st.session_state["recommendations"] = recommendations

    if recommendations and "target_role_title" not in st.session_state:
        st.session_state["target_role_title"] = recommendations[0]["title"]


if "initialized" not in st.session_state:
    st.session_state["initialized"] = True
    st.session_state["job_roles"] = copy.deepcopy(SAMPLE_JOB_ROLES)
    st.session_state["completed_steps"] = set()
    run_full_analysis(DEMO_RESUME_TEXT, DEMO_RESUME_FILENAME)


# ---------------------------------------------------------------------------
# Sidebar Navigation & Quick Controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.4rem 0 0.8rem 0;">
            <div style="font-size: 1.55rem; font-weight: 800; letter-spacing: -0.02em;">
                🎯 CareerAI
            </div>
            <div style="font-size: 0.82rem; opacity: 0.78;">
                Smart Resume & Career Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    nav_page = st.radio(
        "NAVIGATION",
        options=[
            "📊 Overview Dashboard",
            "📄 Upload & Resume Analyzer",
            "💼 Job Role Matcher",
            "🧩 Skill Gap & Roadmap",
            "📥 Export Report",
            "⚙️ Role Catalog Studio",
        ],
        label_visibility="visible",
    )

    st.divider()
    st.markdown("**ACTIVE RESUME PROFILE**")
    parsed_now = st.session_state["parsed"]
    score_now = st.session_state["score_report"]
    st.caption(f"👤 **{parsed_now['full_name']}**")
    st.caption(f"📁 `{st.session_state['filename']}`")
    st.caption(f"⭐ Score: **{score_now['overall_score']}/100** · **{len(st.session_state['skills'])}** Skills")

    st.markdown("**📤 QUICK UPLOAD ANY RESUME**")
    sidebar_upload = st.file_uploader(
        "Upload PDF, DOCX, TXT, or MD",
        type=["pdf", "docx", "txt", "md"],
        key="sidebar_resume_uploader",
        label_visibility="collapsed",
    )
    if sidebar_upload is not None:
        file_sig = f"{sidebar_upload.name}:{sidebar_upload.size}"
        if st.session_state.get("last_uploaded_sig") != file_sig:
            text, doc_info, err = extract_text_from_file(sidebar_upload)
            if err:
                st.error(err)
            else:
                st.session_state["last_uploaded_sig"] = file_sig
                st.session_state["completed_steps"] = set()
                run_full_analysis(text, sidebar_upload.name)
                st.toast(f"Analyzed {sidebar_upload.name} ({doc_info})!", icon="🎉")
                st.rerun()

    if st.button("🔄 Load Sample BCA Demo Resume", use_container_width=True):
        st.session_state["completed_steps"] = set()
        st.session_state["last_uploaded_sig"] = None
        run_full_analysis(DEMO_RESUME_TEXT, DEMO_RESUME_FILENAME)
        st.toast("Loaded Aarav Sharma's sample BCA Data Science resume!", icon="✅")
        st.rerun()

    st.divider()
    st.caption("Built with Python, Streamlit, Plotly & TF-IDF Cosine Engine")


# ---------------------------------------------------------------------------
# Helper Components
# ---------------------------------------------------------------------------
def render_hero(badge: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-badge">{badge}</div>
            <div class="hero-title">{title}</div>
            <p class="hero-sub">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def skill_chip_class(category: str) -> str:
    return {
        "Programming": "chip-prog",
        "Data Science & AI": "chip-ds",
        "Web Development": "chip-web",
        "Soft Skills & Tools": "chip-soft",
    }.get(category, "chip-prog")


def render_skill_chips(skills_list):
    if not skills_list:
        st.info("No skills detected yet. Upload a resume or add skills manually.")
        return
    html = '<div class="chip-container">'
    for s in skills_list:
        cls = skill_chip_class(s["category"])
        tag = " ✦" if s.get("user_added") else ""
        html += f'<span class="skill-chip {cls}">{s["name"]}{tag}</span>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ===========================================================================
# PAGE 1: OVERVIEW DASHBOARD
# ===========================================================================
if nav_page == "📊 Overview Dashboard":
    render_hero(
        "CAREER INTELLIGENCE WORKSPACE",
        "Resume Strength & Role Readiness Dashboard",
        "Deterministic 100-point rubric evaluation paired with sublinear TF-IDF & Cosine Similarity role matching.",
    )

    parsed = st.session_state["parsed"]
    score_report = st.session_state["score_report"]
    skills = st.session_state["skills"]
    recs = st.session_state["recommendations"]

    top_match = recs[0] if recs else None
    overall = score_report["overall_score"]
    score_grade = (
        "Industry Ready" if overall >= 80
        else ("Competitive" if overall >= 65 else "Needs Polish")
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Resume Score</div>
                <div class="kpi-value">{overall} / 100</div>
                <div class="kpi-delta">Tier: {score_grade}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Verified Skills</div>
                <div class="kpi-value">{len(skills)}</div>
                <div class="kpi-delta">Across {len(set(s['category'] for s in skills))} skill domains</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        top_title = top_match["title"] if top_match else "N/A"
        top_pct = f"{top_match['match_percentage']}% Match" if top_match else ""
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Top Recommended Role</div>
                <div class="kpi-value" style="font-size: 1.35rem; padding-top: 0.25rem;">{top_title}</div>
                <div class="kpi-delta">{top_pct}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Resume Word Count</div>
                <div class="kpi-value">{score_report['word_count']}</div>
                <div class="kpi-delta">Target range: 160 – 1,100 words</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.25, 1])

    with col_left:
        st.subheader("100-Point Rubric Breakdown")
        cat_df = pd.DataFrame(score_report["categories"])
        cat_df["Percentage"] = (cat_df["earned"] / cat_df["max"] * 100).round(1)
        fig_bar = go.Figure()
        fig_bar.add_trace(
            go.Bar(
                y=cat_df["category"][::-1],
                x=cat_df["earned"][::-1],
                name="Earned Points",
                orientation="h",
                marker_color="#2563EB",
                text=[f"{e}/{m}" for e, m in zip(cat_df["earned"][::-1], cat_df["max"][::-1])],
                textposition="outside",
            )
        )
        fig_bar.update_layout(
            height=360,
            margin=dict(l=10, r=35, t=15, b=15),
            xaxis=dict(title="Points Earned", range=[0, 29], gridcolor="#E2E8F0"),
            yaxis=dict(title=""),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(family="Inter, sans-serif", size=12),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.subheader("Skill Domain Distribution")
        if skills:
            skill_df = pd.DataFrame(skills)
            domain_counts = skill_df["category"].value_counts().reset_index()
            domain_counts.columns = ["Domain", "Count"]
            fig_pie = px.pie(
                domain_counts,
                names="Domain",
                values="Count",
                hole=0.55,
                color_discrete_sequence=["#2563EB", "#7C3AED", "#059669", "#D97706"],
            )
            fig_pie.update_layout(
                height=360,
                margin=dict(l=10, r=10, t=15, b=15),
                paper_bgcolor="#FFFFFF",
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                font=dict(family="Inter, sans-serif", size=12),
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No skills detected to chart.")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.subheader("✅ Key Strengths")
        for item in score_report["strengths"]:
            st.success(item)
    with col_s2:
        st.subheader("💡 High-Impact Improvements")
        for item in score_report["suggestions"]:
            st.warning(item)

    if recs:
        st.subheader("Top 5 Role Compatibility Snapshot")
        top5_df = pd.DataFrame(recs[:5])[["title", "category", "match_percentage", "skill_overlap_pct", "tfidf_cosine"]]
        top5_df.columns = ["Role Title", "Domain", "Overall Match (%)", "Core Skill Coverage (%)", "TF-IDF Cosine"]
        st.dataframe(top5_df, use_container_width=True, hide_index=True)


# ===========================================================================
# PAGE 2: UPLOAD & RESUME ANALYZER
# ===========================================================================
elif nav_page == "📄 Upload & Resume Analyzer":
    render_hero(
        "NLP PARSER & RUBRIC EVALUATOR",
        "Upload & Analyze Your Resume",
        "Upload a PDF/TXT resume or paste raw resume text. Edit extracted skills live to see instant score & job match updates.",
    )

    tab_upload, tab_paste = st.tabs(["📤 Upload PDF / TXT File", "✍️ Paste or Edit Resume Text"])

    with tab_upload:
        uploaded = st.file_uploader(
            "Choose any resume file (PDF, Word DOCX, TXT, or Markdown — max 5 MB)",
            type=["pdf", "docx", "txt", "md"],
            key="main_resume_uploader",
        )
        if uploaded is not None:
            if st.button("🚀 Analyze Uploaded Resume", type="primary"):
                text, doc_info, err = extract_text_from_file(uploaded)
                if err:
                    st.error(err)
                else:
                    st.session_state["completed_steps"] = set()
                    run_full_analysis(text, uploaded.name)
                    st.success(f"Extracted {doc_info} from `{uploaded.name}` and updated all dashboards!")

    with tab_paste:
        edited_text = st.text_area(
            "Resume Content",
            value=st.session_state["raw_text"],
            height=260,
            help="Edit or paste resume text directly and click Re-Analyze.",
        )
        if st.button("⚡ Re-Analyze Edited Text", type="primary"):
            if edited_text.strip():
                st.session_state["completed_steps"] = set()
                run_full_analysis(edited_text, "Custom_Pasted_Resume.txt")
                st.success("Resume parsed and scored successfully!")
            else:
                st.error("Please enter resume text before analyzing.")

    st.divider()

    parsed = st.session_state["parsed"]
    score_report = st.session_state["score_report"]
    skills = st.session_state["skills"]

    st.subheader("1. Extracted Structured Profile")
    p1, p2, p3 = st.columns(3)
    p1.info(f"**Full Name:** {parsed['full_name']}")
    p2.info(f"**Email:** {parsed['email']}")
    p3.info(f"**Phone:** {parsed['phone']}")

    if parsed["summary"] != "Not Found":
        st.markdown(f"**Professional Summary:** {parsed['summary']}")
    else:
        st.caption("⚠️ Professional Summary: Not Found")

    sec_c1, sec_c2 = st.columns(2)
    with sec_c1:
        with st.expander(f"🎓 Education ({len(parsed['education'])} lines)", expanded=True):
            if parsed["education"]:
                for line in parsed["education"]:
                    st.markdown(f"- {line}")
            else:
                st.caption("Not Found")

        with st.expander(f"🚀 Projects ({len(parsed['projects'])} lines)", expanded=True):
            if parsed["projects"]:
                for line in parsed["projects"]:
                    st.markdown(f"- {line}")
            else:
                st.caption("Not Found")

    with sec_c2:
        with st.expander(f"💼 Work Experience ({len(parsed['work_experience'])} lines)", expanded=True):
            if parsed["work_experience"]:
                for line in parsed["work_experience"]:
                    st.markdown(f"- {line}")
            else:
                st.caption("Not Found")

        with st.expander(f"🏅 Certifications & Languages", expanded=True):
            if parsed["certifications"]:
                for cert in parsed["certifications"]:
                    st.markdown(f"- {cert}")
            else:
                st.caption("Certifications: Not Found")
            langs = ", ".join(parsed["languages"]) if parsed["languages"] else "Not Found"
            st.markdown(f"**Languages:** {langs}")

    st.divider()
    st.subheader("2. Interactive Skill Tag Editor")
    st.caption("NLP-extracted skills are grouped by category. Add missing skills or remove false positives to immediately recalculate your scores.")

    render_skill_chips(skills)
    st.markdown("<br>", unsafe_allow_html=True)

    sk_col1, sk_col2 = st.columns(2)
    with sk_col1:
        known_options = [s for s in all_known_skills() if s.lower() not in {x["name"].lower() for x in skills}]
        selected_preset = st.selectbox("Add from Skill Taxonomy", options=[""] + known_options)
        custom_skill_input = st.text_input("Or type a custom skill (e.g., Streamlit, LangChain, MongoDB)")
        if st.button("➕ Add Skill"):
            to_add = custom_skill_input.strip() or selected_preset.strip()
            if to_add:
                norm = normalize_skill(to_add, user_added=True)
                if norm["name"].lower() not in {x["name"].lower() for x in skills}:
                    st.session_state["skills"].append(norm)
                    recompute_downstream()
                    st.toast(f"Added {norm['name']} ({norm['category']})", icon="✨")
                    st.rerun()
                else:
                    st.warning(f"{norm['name']} is already in your skill list.")

    with sk_col2:
        current_names = [s["name"] for s in skills]
        to_remove = st.multiselect("Select skills to remove", options=current_names)
        if st.button("🗑️ Remove Selected Skills") and to_remove:
            remove_set = {r.lower() for r in to_remove}
            st.session_state["skills"] = [s for s in skills if s["name"].lower() not in remove_set]
            recompute_downstream()
            st.toast(f"Removed {len(to_remove)} skill(s)", icon="🗑️")
            st.rerun()

    st.divider()
    st.subheader("3. Detailed 100-Point Rubric Audit")
    for cat in score_report["categories"]:
        pct = cat["earned"] / cat["max"]
        col_a, col_b = st.columns([1.4, 2.6])
        with col_a:
            st.markdown(f"**{cat['category']}** — `{cat['earned']} / {cat['max']} pts`")
            st.progress(pct)
        with col_b:
            st.caption(cat["rationale"])


# ===========================================================================
# PAGE 3: JOB ROLE MATCHER
# ===========================================================================
elif nav_page == "💼 Job Role Matcher":
    render_hero(
        "TF-IDF + COSINE SIMILARITY ENGINE",
        "Intelligent Job Role Recommendations",
        "Ranked against 12 benchmark tech roles using sublinear TF-IDF vectorization and required-skill overlap.",
    )

    recs = st.session_state["recommendations"]

    f1, f2, f3 = st.columns([1.3, 1.2, 1])
    with f1:
        categories = ["All Domains"] + sorted(list({r["category"] for r in recs}))
        selected_cat = st.selectbox("Filter by Domain", options=categories)
    with f2:
        levels = ["All Levels"] + sorted(list({r["experience_level"] for r in recs}))
        selected_level = st.selectbox("Filter by Experience Level", options=levels)
    with f3:
        min_match = st.slider("Minimum Match %", min_value=0, max_value=90, value=0, step=5)

    filtered = [
        r for r in recs
        if (selected_cat == "All Domains" or r["category"] == selected_cat)
        and (selected_level == "All Levels" or r["experience_level"] == selected_level)
        and r["match_percentage"] >= min_match
    ]

    if not filtered:
        st.info("No roles match the selected filters. Try lowering the Minimum Match slider.")
    else:
        # Comparison Chart
        chart_df = pd.DataFrame(filtered)
        fig = px.bar(
            chart_df,
            x="match_percentage",
            y="title",
            color="category",
            orientation="h",
            text="match_percentage",
            labels={"match_percentage": "Blended Match (%)", "title": "Job Role", "category": "Domain"},
            color_discrete_sequence=["#2563EB", "#7C3AED", "#059669", "#D97706"],
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(
            height=max(320, len(filtered) * 36),
            yaxis=dict(autorange="reversed"),
            xaxis=dict(range=[0, 108], gridcolor="#E2E8F0"),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=10, r=30, t=15, b=15),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(f"Matched Role Breakdown ({len(filtered)} Roles)")
        for rank, rec in enumerate(filtered, start=1):
            mp = rec["match_percentage"]
            pill_cls = "match-high" if mp >= 75 else ("match-mid" if mp >= 50 else "match-low")

            matched_chips = "".join(
                f'<span class="skill-chip chip-have">✓ {s}</span>' for s in rec["matching_skills"]
            ) or '<span style="color:#64748B;font-size:0.85rem;">None yet</span>'

            missing_chips = "".join(
                f'<span class="skill-chip chip-miss">✕ {s}</span>' for s in rec["missing_skills"]
            ) or '<span style="color:#059669;font-size:0.85rem;font-weight:600;">All core skills covered!</span>'

            st.markdown(
                f"""
                <div class="job-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
                        <div>
                            <span style="font-size:1.15rem; font-weight:700; color:#0F172A;">#{rank} · {rec['title']}</span>
                            <span style="margin-left:0.6rem; font-size:0.82rem; color:#475569; background:#F1F5F9; padding:0.2rem 0.6rem; border-radius:6px;">
                                {rec['category']} · {rec['experience_level']}
                            </span>
                        </div>
                        <span class="match-pill {pill_cls}">{mp}% Overall Match</span>
                    </div>
                    <p style="margin:0.55rem 0; color:#334155; font-size:0.93rem;">{rec['role']['summary']}</p>
                    <div style="font-size:0.82rem; color:#475569; margin-bottom:0.6rem;">
                        <strong>Scoring Telemetry:</strong> Core Skill Overlap: <b>{rec['skill_overlap_pct']}%</b> · TF-IDF Cosine Similarity: <b>{rec['tfidf_cosine']}</b>
                    </div>
                    <div style="margin-bottom:0.4rem;">
                        <span style="font-size:0.8rem; font-weight:700; color:#065F46;">MATCHING SKILLS:</span>
                        <div class="chip-container">{matched_chips}</div>
                    </div>
                    <div>
                        <span style="font-size:0.8rem; font-weight:700; color:#991B1B;">MISSING CORE SKILLS:</span>
                        <div class="chip-container">{missing_chips}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ===========================================================================
# PAGE 4: SKILL GAP & LEARNING ROADMAP
# ===========================================================================
elif nav_page == "🧩 Skill Gap & Roadmap":
    render_hero(
        "TARGET ROLE READINESS & UPSKILLING PLAN",
        "Skill Gap Analysis & Personalized Learning Roadmap",
        "Select any target career track to inspect required vs. acquired skills and follow a step-by-step project roadmap.",
    )

    roles = st.session_state["job_roles"]
    role_titles = [r["title"] for r in roles]
    default_idx = (
        role_titles.index(st.session_state["target_role_title"])
        if st.session_state.get("target_role_title") in role_titles
        else 0
    )

    selected_title = st.selectbox("🎯 Select Target Career Role", options=role_titles, index=default_idx)
    st.session_state["target_role_title"] = selected_title
    target_role = next(r for r in roles if r["title"] == selected_title)

    gap_report = analyze_skill_gap(st.session_state["skills"], target_role)
    roadmap = generate_learning_roadmap(gap_report)

    g1, g2, g3 = st.columns(3)
    g1.metric("Core Skill Readiness", f"{gap_report['match_percentage']}%")
    g2.metric("Skills Already Acquired", len(gap_report["acquired_skills"]))
    g3.metric("Skills to Acquire", len(gap_report["missing_skills"]))

    st.divider()

    col_gap1, col_gap2 = st.columns([1.15, 1])
    with col_gap1:
        st.subheader("Skill Checklist Matrix")
        gap_df = pd.DataFrame(gap_report["items"])
        gap_df["Status"] = gap_df["acquired"].map({True: "✅ Acquired", False: "❌ Missing"})
        display_gap = gap_df[["skill", "type", "priority", "Status"]]
        display_gap.columns = ["Skill", "Requirement", "Priority", "Status"]
        st.dataframe(display_gap, use_container_width=True, hide_index=True)

    with col_gap2:
        st.subheader("Readiness Radar by Category")
        radar_df = gap_df.groupby("category")["acquired"].mean().reset_index()
        radar_df["Readiness %"] = (radar_df["acquired"] * 100).round(0)
        if len(radar_df) >= 3:
            fig_radar = go.Figure(
                data=go.Scatterpolar(
                    r=radar_df["Readiness %"],
                    theta=radar_df["category"],
                    fill="toself",
                    line_color="#2563EB",
                )
            )
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                height=320,
                margin=dict(l=30, r=30, t=25, b=25),
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            fig_small = px.bar(
                radar_df,
                x="category",
                y="Readiness %",
                range_y=[0, 100],
                color_discrete_sequence=["#2563EB"],
            )
            fig_small.update_layout(height=300, margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_small, use_container_width=True)

    st.divider()
    st.subheader(f"🗺️ Step-by-Step Upskilling Roadmap for {selected_title}")

    completed = st.session_state["completed_steps"]
    total_steps = len(roadmap)
    done_count = sum(1 for stp in roadmap if f"{selected_title}:{stp['skill']}" in completed)
    st.progress(done_count / total_steps if total_steps else 0.0, text=f"Roadmap Progress: {done_count} of {total_steps} milestones completed")

    for step in roadmap:
        step_key = f"{selected_title}:{step['skill']}"
        with st.container(border=True):
            top_r1, top_r2 = st.columns([3.5, 1])
            with top_r1:
                st.markdown(
                    f"#### Step {step['step']}: {step['skill']} "
                    f"(`{step['priority']}` · ⏱️ {step['duration']})"
                )
                st.markdown(f"**Learning Objective:** {step['objective']}")
                st.markdown(f"**🛠️ Hands-On Portfolio Project:** {step['project']}")
            with top_r2:
                checked = st.checkbox(
                    "Mark Completed",
                    value=(step_key in completed),
                    key=f"chk_{step_key}",
                )
                if checked:
                    completed.add(step_key)
                else:
                    completed.discard(step_key)


# ===========================================================================
# PAGE 5: EXPORT REPORT
# ===========================================================================
elif nav_page == "📥 Export Report":
    render_hero(
        "PORTABLE CAREER DELIVERABLES",
        "Export CareerAI Analysis Report",
        "Download a clean PDF dossier or Markdown summary containing your rubric scores, verified skills, role matches, and roadmap.",
    )

    roles = st.session_state["job_roles"]
    target_title = st.session_state.get("target_role_title", roles[0]["title"])
    target_role = next((r for r in roles if r["title"] == target_title), roles[0])
    gap_report = analyze_skill_gap(st.session_state["skills"], target_role)
    roadmap = generate_learning_roadmap(gap_report)

    pdf_bytes = generate_pdf_report(
        parsed=st.session_state["parsed"],
        score_report=st.session_state["score_report"],
        skills=st.session_state["skills"],
        recommendations=st.session_state["recommendations"],
        target_role_title=target_title,
        roadmap_steps=roadmap,
    )

    md_text = generate_markdown_report(
        parsed=st.session_state["parsed"],
        score_report=st.session_state["score_report"],
        skills=st.session_state["skills"],
        recommendations=st.session_state["recommendations"],
        target_role_title=target_title,
        roadmap_steps=roadmap,
    )

    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button(
            label="📄 Download Full PDF Report (.pdf)",
            data=pdf_bytes,
            file_name="CareerAI_Analysis_Report.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )
    with dl2:
        st.download_button(
            label="📝 Download Markdown Action Plan (.md)",
            data=md_text,
            file_name="CareerAI_Action_Plan.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.divider()
    st.subheader("Live Report Preview")
    with st.container(border=True):
        st.markdown(md_text)


# ===========================================================================
# PAGE 6: ROLE CATALOG STUDIO
# ===========================================================================
elif nav_page == "⚙️ Role Catalog Studio":
    render_hero(
        "CUSTOM BENCHMARK CONFIGURATION",
        "Job Role Catalog Studio",
        "Inspect existing benchmark job roles or add your own custom target job description to test your resume against it.",
    )

    with st.expander("➕ Add a Custom Target Job Role", expanded=True):
        with st.form("add_role_form"):
            r_col1, r_col2, r_col3 = st.columns(3)
            new_title = r_col1.text_input("Job Title *", placeholder="e.g., Generative AI Developer")
            new_cat = r_col2.selectbox(
                "Domain Category",
                ["AI & Machine Learning", "Data & Analytics", "Software Engineering", "Web Development", "Mobile Engineering"],
            )
            new_level = r_col3.selectbox("Experience Level", ["Entry / Junior", "Junior / Mid", "Mid / Senior"])
            new_summary = st.text_area("Role Summary *", placeholder="Describe core responsibilities and focus area...")
            new_req = st.text_input("Required Skills (comma-separated) *", placeholder="Python, NLP, FastAPI, REST API, Git")
            new_pref = st.text_input("Preferred Skills (comma-separated)", placeholder="Docker, Cloud Computing, PyTorch")

            submitted = st.form_submit_button("Save Custom Role & Re-Rank", type="primary")
            if submitted:
                if not new_title.strip() or not new_req.strip():
                    st.error("Job Title and Required Skills are mandatory.")
                else:
                    req_list = [s.strip() for s in new_req.split(",") if s.strip()]
                    pref_list = [s.strip() for s in new_pref.split(",") if s.strip()]
                    st.session_state["job_roles"].append({
                        "title": new_title.strip(),
                        "category": new_cat,
                        "experience_level": new_level,
                        "summary": new_summary.strip() or f"Custom benchmark role for {new_title.strip()}.",
                        "required_skills": req_list,
                        "preferred_skills": pref_list,
                        "responsibilities": [new_summary.strip() or "Deliver high-quality technical solutions."],
                    })
                    recompute_downstream()
                    st.success(f"Added '{new_title.strip()}' and updated TF-IDF rankings!")

    st.subheader(f"Active Benchmark Roles ({len(st.session_state['job_roles'])})")
    roles_table = pd.DataFrame([
        {
            "Title": r["title"],
            "Category": r["category"],
            "Level": r["experience_level"],
            "Required Skills": ", ".join(r["required_skills"]),
            "Preferred Skills": ", ".join(r["preferred_skills"]),
        }
        for r in st.session_state["job_roles"]
    ])
    st.dataframe(roles_table, use_container_width=True, hide_index=True)
