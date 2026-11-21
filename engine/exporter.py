"""
Export utilities for CareerAI:
- Downloadable PDF Analysis Report (using fpdf2 with explicit page width to prevent FPDFException)
- Downloadable Markdown Action Plan
"""
from datetime import datetime
from typing import Dict, List
from fpdf import FPDF


def _clean_latin(text: str) -> str:
    replacements = {
        "—": "-", "–": "-", "•": "*", "·": "|",
        "’": "'", "‘": "'", "“": '"', "”": '"', "→": "->"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Break any ultra-long unbroken tokens (e.g., long URLs) so FPDF never overflows horizontally
    words = []
    for token in text.split(" "):
        if len(token) > 65:
            chunks = [token[i:i+65] for i in range(0, len(token), 65)]
            words.append(" ".join(chunks))
        else:
            words.append(token)
    safe = " ".join(words)
    return safe.encode("latin-1", "replace").decode("latin-1")


def _write_wrapped(pdf: FPDF, text: str, line_height: float = 5.5):
    pdf.set_x(pdf.l_margin)
    avail_w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.multi_cell(avail_w, line_height, _clean_latin(text))


def generate_pdf_report(
    parsed: Dict,
    score_report: Dict,
    skills: List[Dict],
    recommendations: List[Dict],
    target_role_title: str,
    roadmap_steps: List[Dict],
) -> bytes:
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header Banner
    pdf.set_fill_color(30, 58, 138)
    pdf.rect(0, 0, 210, 34, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 17)
    pdf.set_xy(15, 9)
    pdf.cell(0, 8, "CareerAI - Smart Resume & Career Analysis Report", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(15)
    pdf.cell(0, 6, f"Generated on {datetime.now().strftime('%d %b %Y, %I:%M %p')}", ln=True)

    pdf.ln(12)
    pdf.set_text_color(15, 23, 42)
    pdf.set_x(15)

    # 1. Candidate Overview
    pdf.set_font("Helvetica", "B", 13)
    _write_wrapped(pdf, "1. Candidate Profile & Overall Score", 8)
    pdf.set_font("Helvetica", "", 10)
    _write_wrapped(pdf, f"Name: {parsed['full_name']}   |   Email: {parsed['email']}   |   Phone: {parsed['phone']}", 6)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(37, 99, 235)
    _write_wrapped(pdf, f"Overall Resume Score: {score_report['overall_score']} / 100  (Word Count: {score_report['word_count']})", 7)
    pdf.set_text_color(15, 23, 42)
    pdf.ln(3)

    # 2. Score Breakdown
    pdf.set_font("Helvetica", "B", 12)
    _write_wrapped(pdf, "2. 100-Point Rubric Breakdown", 8)
    pdf.set_font("Helvetica", "", 9.5)
    for cat in score_report["categories"]:
        _write_wrapped(pdf, f"- {cat['category']}: {cat['earned']}/{cat['max']} pts -- {cat['rationale']}", 5.5)
    pdf.ln(3)

    # 3. Detected Skills
    pdf.set_font("Helvetica", "B", 12)
    _write_wrapped(pdf, f"3. Verified Skills ({len(skills)} Total)", 8)
    pdf.set_font("Helvetica", "", 9.5)
    skill_str = ", ".join(s["name"] for s in skills) if skills else "None detected"
    _write_wrapped(pdf, skill_str, 5.5)
    pdf.ln(3)

    # 4. Improvement Suggestions
    pdf.set_font("Helvetica", "B", 12)
    _write_wrapped(pdf, "4. Actionable Improvement Recommendations", 8)
    pdf.set_font("Helvetica", "", 9.5)
    for sug in score_report["suggestions"]:
        _write_wrapped(pdf, f"* {sug}", 5.5)
    pdf.ln(3)

    # 5. Top Job Matches
    pdf.set_font("Helvetica", "B", 12)
    _write_wrapped(pdf, "5. Top TF-IDF Role Recommendations", 8)
    pdf.set_font("Helvetica", "", 9.5)
    for rec in recommendations[:5]:
        _write_wrapped(pdf, f"- {rec['title']} ({rec['category']}): {rec['match_percentage']}% Match | TF-IDF Cosine: {rec['tfidf_cosine']}", 5.5)
    pdf.ln(3)

    # 6. Learning Roadmap
    pdf.set_font("Helvetica", "B", 12)
    _write_wrapped(pdf, f"6. Learning Roadmap for {target_role_title}", 8)
    pdf.set_font("Helvetica", "", 9.5)
    for step in roadmap_steps[:6]:
        _write_wrapped(pdf, f"Step {step['step']} [{step['priority']}] {step['skill']} ({step['duration']}): {step['objective']}", 5.5)

    import inspect
    sig = inspect.signature(pdf.output)
    if "dest" in sig.parameters:
        raw_out = pdf.output(dest="S")
    else:
        raw_out = pdf.output()
    return raw_out.encode("latin-1") if isinstance(raw_out, str) else bytes(raw_out)


def generate_markdown_report(
    parsed: Dict,
    score_report: Dict,
    skills: List[Dict],
    recommendations: List[Dict],
    target_role_title: str,
    roadmap_steps: List[Dict],
) -> str:
    lines = [
        "# CareerAI — Resume & Career Analysis Report",
        f"*Generated on {datetime.now().strftime('%d %b %Y, %I:%M %p')}*",
        "",
        "## 1. Candidate Overview",
        f"- **Full Name:** {parsed['full_name']}",
        f"- **Email:** {parsed['email']}",
        f"- **Phone:** {parsed['phone']}",
        f"- **Overall Resume Score:** **{score_report['overall_score']} / 100** ({score_report['word_count']} words)",
        "",
        "## 2. Rubric Score Breakdown",
        "| Category | Score | Rationale |",
        "| :--- | :---: | :--- |",
    ]
    for c in score_report["categories"]:
        lines.append(f"| {c['category']} | {c['earned']} / {c['max']} | {c['rationale']} |")

    lines.extend([
        "",
        "## 3. Verified Skills",
        ", ".join(f"`{s['name']}`" for s in skills) if skills else "_No skills detected_",
        "",
        "## 4. Improvement Suggestions",
    ])
    for s in score_report["suggestions"]:
        lines.append(f"- {s}")

    lines.extend([
        "",
        "## 5. Top Job Recommendations (TF-IDF + Skill Match)",
        "| Rank | Role | Category | Match % | TF-IDF Cosine | Missing Core Skills |",
        "| :---: | :--- | :--- | :---: | :---: | :--- |",
    ])
    for idx, r in enumerate(recommendations[:6], start=1):
        miss = ", ".join(r["missing_skills"]) if r["missing_skills"] else "None"
        lines.append(f"| #{idx} | {r['title']} | {r['category']} | {r['match_percentage']}% | {r['tfidf_cosine']} | {miss} |")

    lines.extend([
        "",
        f"## 6. Personalized Learning Roadmap — {target_role_title}",
    ])
    for st in roadmap_steps:
        lines.append(f"### Step {st['step']}: {st['skill']} ({st['priority']} · {st['duration']})")
        lines.append(f"- **Objective:** {st['objective']}")
        lines.append(f"- **Hands-on Project:** {st['project']}")
        lines.append("")

    return "\n".join(lines)
