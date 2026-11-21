"""
Transparent, deterministic 100-point rule-based resume scoring engine.
Exact rubric:
 - Skills Relevance: 25 pts
 - Education: 15 pts
 - Projects: 15 pts
 - Work Experience: 15 pts
 - Resume Structure: 10 pts
 - Keywords & Impact: 10 pts
 - Certifications: 5 pts
 - Contact Information: 5 pts
"""
import re
from typing import Dict, List

ACTION_VERBS = [
    "built", "developed", "designed", "implemented", "analyzed", "created",
    "engineered", "optimized", "automated", "deployed", "trained", "evaluated",
    "led", "collaborated", "improved", "reduced", "increased", "architected",
    "integrated", "visualized", "managed", "delivered"
]

METRIC_PATTERN = re.compile(
    r"\b\d+(\.\d+)?(%|\+|x|k|m|ms|sec|hours|users|records|rows|accuracy|f1)\b",
    re.I
)


def evaluate_resume(raw_text: str, parsed: Dict, skills: List[Dict]) -> Dict:
    lower_text = raw_text.lower()
    word_count = len([w for w in raw_text.split() if w.strip()])

    # 1. Skills Relevance (25 points)
    technical_count = sum(1 for s in skills if s["category"] != "Soft Skills & Tools")
    soft_count = sum(1 for s in skills if s["category"] == "Soft Skills & Tools")
    categories_covered = len(set(s["category"] for s in skills))
    skills_pts = int(
        min(technical_count, 8) * 2.2
        + min(soft_count, 3) * 1.3
        + min(categories_covered, 4) * 0.9
    )
    skills_pts = max(0, min(25, skills_pts))
    skills_rationale = f"Detected {technical_count} technical and {soft_count} soft/tool skills across {categories_covered} categories."

    # 2. Education (15 points)
    has_edu = len(parsed["education"]) > 0
    has_degree = any(
        k in lower_text
        for k in ["bca", "mca", "b.tech", "b.sc", "m.sc", "m.tech", "bachelor", "master", "diploma", "computer science", "data science"]
    )
    has_year_or_gpa = bool(re.search(r"(20[12]\d|cgpa|gpa|\d{2}%)", " ".join(parsed["education"]), re.I))
    if has_edu and has_degree and has_year_or_gpa:
        edu_pts = 15
    elif has_edu and has_degree:
        edu_pts = 12
    elif has_edu:
        edu_pts = 9
    elif has_degree:
        edu_pts = 7
    else:
        edu_pts = 0

    if edu_pts >= 14:
        edu_rationale = "Complete education section with degree and academic timeline/score."
    elif edu_pts >= 9:
        edu_rationale = "Education detected; adding graduation year or CGPA increases clarity."
    else:
        edu_rationale = "No structured Education section found."

    # 3. Projects (15 points)
    project_lines = len(parsed["projects"])
    proj_joined = " ".join(parsed["projects"]).lower()
    proj_has_tech = any(s["name"].lower() in proj_joined for s in skills)
    if project_lines >= 4 and proj_has_tech:
        projects_pts = 15
    elif project_lines >= 2 and proj_has_tech:
        projects_pts = 12
    elif project_lines >= 2:
        projects_pts = 9
    elif project_lines == 1:
        projects_pts = 6
    else:
        projects_pts = 0

    if projects_pts >= 12:
        projects_rationale = f"Strong projects section ({project_lines} lines) demonstrating applied skills."
    elif projects_pts > 0:
        projects_rationale = "Projects found, but adding concrete tech stack and outcomes will strengthen impact."
    else:
        projects_rationale = "No Projects section detected."

    # 4. Work Experience (15 points)
    exp_lines = len(parsed["work_experience"])
    exp_has_metrics = bool(METRIC_PATTERN.search(" ".join(parsed["work_experience"])))
    if exp_lines >= 5 and exp_has_metrics:
        exp_pts = 15
    elif exp_lines >= 4:
        exp_pts = 13
    elif exp_lines >= 2:
        exp_pts = 10
    elif exp_lines == 1:
        exp_pts = 6
    else:
        exp_pts = 0

    if exp_pts >= 13:
        exp_rationale = f"Detailed work/internship history ({exp_lines} lines) with measurable outcomes."
    elif exp_pts > 0:
        exp_rationale = "Experience present; quantify accomplishments with metrics where factual."
    else:
        exp_rationale = "No Work Experience or Internship section detected."

    # 5. Resume Structure (10 points)
    structure_pts = 0
    if parsed["summary"] != "Not Found":
        structure_pts += 2
    if parsed["education"]:
        structure_pts += 2
    if parsed["projects"] or parsed["work_experience"]:
        structure_pts += 2
    if skills:
        structure_pts += 2
    if 160 <= word_count <= 1100:
        structure_pts += 2
    elif 80 <= word_count <= 159:
        structure_pts += 1
    structure_pts = min(10, structure_pts)
    structure_rationale = f"Word count: {word_count} words. Evaluated section headers, summary presence, and length balance."

    # 6. Keywords & Action Impact (10 points)
    matched_verbs = sum(1 for v in ACTION_VERBS if re.search(rf"\b{v}\b", lower_text))
    metrics_count = len(METRIC_PATTERN.findall(raw_text))
    keywords_pts = min(10, min(matched_verbs, 6) + min(metrics_count, 4))
    keywords_rationale = f"Found {matched_verbs} strong action verbs and {metrics_count} measurable indicators."

    # 7. Certifications (5 points)
    cert_count = len(parsed["certifications"])
    cert_pts = 5 if cert_count >= 2 else (3 if cert_count == 1 else 0)
    cert_rationale = f"Found {cert_count} certification entry/entries." if cert_pts > 0 else "No Certifications section found."

    # 8. Contact Information (5 points)
    contact_pts = 0
    if parsed["full_name"] != "Not Found":
        contact_pts += 1
    if parsed["email"] != "Not Found":
        contact_pts += 2
    if parsed["phone"] != "Not Found":
        contact_pts += 1
    if "linkedin" in lower_text or "github" in lower_text:
        contact_pts += 1
    contact_pts = min(5, contact_pts)
    contact_rationale = (
        f"Name: {'Yes' if parsed['full_name'] != 'Not Found' else 'Missing'}, "
        f"Email: {'Yes' if parsed['email'] != 'Not Found' else 'Missing'}, "
        f"Phone: {'Yes' if parsed['phone'] != 'Not Found' else 'Missing'}"
    )

    categories = [
        {"category": "Skills Relevance", "earned": skills_pts, "max": 25, "rationale": skills_rationale},
        {"category": "Education", "earned": edu_pts, "max": 15, "rationale": edu_rationale},
        {"category": "Projects", "earned": projects_pts, "max": 15, "rationale": projects_rationale},
        {"category": "Work Experience", "earned": exp_pts, "max": 15, "rationale": exp_rationale},
        {"category": "Resume Structure", "earned": structure_pts, "max": 10, "rationale": structure_rationale},
        {"category": "Keywords & Impact", "earned": keywords_pts, "max": 10, "rationale": keywords_rationale},
        {"category": "Certifications", "earned": cert_pts, "max": 5, "rationale": cert_rationale},
        {"category": "Contact Information", "earned": contact_pts, "max": 5, "rationale": contact_rationale},
    ]

    overall_score = min(100, sum(c["earned"] for c in categories))

    strengths = []
    weaknesses = []
    missing_sections = []
    suggestions = []

    if skills_pts >= 18:
        strengths.append(f"Strong technical skill breadth ({technical_count} core technical skills detected).")
    else:
        weaknesses.append(f"Limited technical keyword density ({technical_count} technical skills detected).")
        suggestions.append("Add a dedicated 'Technical Skills' section listing languages, frameworks, and tools you have genuinely used.")

    if edu_pts >= 12:
        strengths.append("Clear academic background with verifiable degree details.")
    elif edu_pts == 0:
        missing_sections.append("Education")
        suggestions.append("Include an Education section with your degree, institution name, and graduation year.")

    if projects_pts >= 12:
        strengths.append("Practical project portfolio reinforcing technical capabilities.")
    elif projects_pts == 0:
        missing_sections.append("Projects")
        suggestions.append("Add 2–3 key academic or personal projects with problem statement, tools used, and your specific role.")
    else:
        weaknesses.append("Project descriptions are brief or lack explicit technology tags.")
        suggestions.append("Expand each project with 2–3 concise bullet points naming the exact libraries/frameworks used.")

    if exp_pts >= 12:
        strengths.append("Relevant work or internship experience documented clearly.")
    elif exp_pts == 0:
        missing_sections.append("Work Experience / Internships")
        suggestions.append("Add internships, freelance work, or campus technical roles under an Experience heading if applicable.")

    if parsed["summary"] == "Not Found":
        missing_sections.append("Professional Summary")
        suggestions.append("Add a concise 2–3 line Professional Summary at the top highlighting your target role and top verified skills.")
    else:
        strengths.append("Includes an introductory Professional Summary.")

    if keywords_pts >= 7:
        strengths.append("Good usage of active engineering verbs and measurable context.")
    else:
        weaknesses.append(f"Low count of action verbs ({matched_verbs}) or measurable outcomes ({metrics_count}).")
        suggestions.append("Start bullet points with strong action verbs (e.g., Built, Analyzed, Automated) and quantify real results.")

    if cert_pts == 0:
        missing_sections.append("Certifications")
        suggestions.append("List verified technical courses or certifications in a dedicated Certifications section.")
    else:
        strengths.append("Certifications validate ongoing learning.")

    if contact_pts < 4:
        weaknesses.append("Incomplete contact block (check full name, email, phone, and GitHub/LinkedIn links).")
        suggestions.append("Ensure your top header displays full name, professional email, phone number, and GitHub/LinkedIn URLs.")
    else:
        strengths.append("Complete, recruiter-ready contact information.")

    if word_count < 160:
        weaknesses.append(f"Resume text is brief ({word_count} words), which may omit key skills and project context.")
    elif word_count > 1100:
        weaknesses.append(f"Resume is dense ({word_count} words); consider tightening to 1–2 focused pages.")

    if not strengths:
        strengths.append("Resume successfully parsed and structured.")
    if not suggestions:
        suggestions.append("Tailor your top skills and summary keywords to each target job description.")

    return {
        "overall_score": overall_score,
        "word_count": word_count,
        "categories": categories,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "missing_sections": missing_sections,
        "suggestions": suggestions,
    }
