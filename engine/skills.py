"""
NLP Keyword Extraction and Alias Normalization Engine.
Maps abbreviations, variants, and phrase tokens to canonical skill names and categories.
"""
import re
from typing import Dict, List

SKILL_TAXONOMY = [
    # Programming
    ("Python", "Programming", ["python", "python3", "py"]),
    ("Java", "Programming", ["java", "core java", "jdk"]),
    ("C++", "Programming", ["c++", "cpp"]),
    ("JavaScript", "Programming", ["javascript", "js", "es6", "ecmascript"]),
    ("SQL", "Programming", ["sql", "mysql", "postgresql", "postgres", "sqlite", "tsql", "pl/sql", "mssql"]),
    ("Kotlin", "Programming", ["kotlin", "jetpack compose", "android sdk"]),
    ("TypeScript", "Programming", ["typescript", "ts"]),
    ("R", "Programming", ["r programming", "rstudio"]),
    ("C#", "Programming", ["c#", "csharp", ".net"]),
    ("Go", "Programming", ["golang"]),

    # Data Science & AI
    ("Machine Learning", "Data Science & AI", ["machine learning", "ml", "supervised learning", "unsupervised learning"]),
    ("Deep Learning", "Data Science & AI", ["deep learning", "neural networks", "cnn", "rnn", "transformers"]),
    ("Data Analysis", "Data Science & AI", ["data analysis", "data analytics", "exploratory data analysis", "eda"]),
    ("Pandas", "Data Science & AI", ["pandas"]),
    ("NumPy", "Data Science & AI", ["numpy"]),
    ("Scikit-learn", "Data Science & AI", ["scikit-learn", "scikit learn", "sklearn"]),
    ("TensorFlow", "Data Science & AI", ["tensorflow", "keras"]),
    ("PyTorch", "Data Science & AI", ["pytorch"]),
    ("Power BI", "Data Science & AI", ["power bi", "powerbi", "dax"]),
    ("Tableau", "Data Science & AI", ["tableau"]),
    ("NLP", "Data Science & AI", ["nlp", "natural language processing", "spacy", "nltk", "tf-idf", "tfidf"]),
    ("Statistics", "Data Science & AI", ["statistics", "statistical modeling", "hypothesis testing", "probability"]),
    ("Advanced Excel", "Data Science & AI", ["excel", "ms excel", "advanced excel", "pivot tables", "vlookup"]),
    ("Data Visualization", "Data Science & AI", ["data visualization", "matplotlib", "seaborn", "plotly"]),

    # Web & Mobile Development
    ("HTML", "Web Development", ["html", "html5"]),
    ("CSS", "Web Development", ["css", "css3", "scss", "sass"]),
    ("React", "Web Development", ["react", "react.js", "reactjs"]),
    ("Node.js", "Web Development", ["node.js", "nodejs", "express.js", "expressjs"]),
    ("FastAPI", "Web Development", ["fastapi"]),
    ("Django", "Web Development", ["django", "drf"]),
    ("Flask", "Web Development", ["flask"]),
    ("REST API", "Web Development", ["rest api", "restful", "restful apis", "graphql"]),
    ("Tailwind CSS", "Web Development", ["tailwind", "tailwind css", "tailwindcss"]),
    ("Android Development", "Web Development", ["android", "android studio", "jetpack compose", "room database"]),

    # Soft Skills & Tools
    ("Communication", "Soft Skills & Tools", ["communication", "presentation skills", "verbal communication", "written communication"]),
    ("Leadership", "Soft Skills & Tools", ["leadership", "team lead", "mentoring", "mentored"]),
    ("Problem Solving", "Soft Skills & Tools", ["problem solving", "problem-solving", "analytical thinking", "debugging"]),
    ("Teamwork", "Soft Skills & Tools", ["teamwork", "collaboration", "cross-functional", "team player"]),
    ("Critical Thinking", "Soft Skills & Tools", ["critical thinking", "decision making", "strategic thinking"]),
    ("Git", "Soft Skills & Tools", ["git", "github", "gitlab", "version control"]),
    ("Docker", "Soft Skills & Tools", ["docker", "containers", "kubernetes"]),
    ("Cloud Computing", "Soft Skills & Tools", ["aws", "gcp", "google cloud", "azure", "cloud computing"]),
    ("Agile", "Soft Skills & Tools", ["agile", "scrum", "kanban", "jira"]),
]

NORMALIZED_LOOKUP: Dict[str, tuple] = {}
for canonical, category, aliases in SKILL_TAXONOMY:
    NORMALIZED_LOOKUP[canonical.lower()] = (canonical, category)
    for alias in aliases:
        NORMALIZED_LOOKUP[alias.lower()] = (canonical, category)


def _matches_token(lower_text: str, alias: str) -> bool:
    if any(sym in alias for sym in ["+", "#", "."]):
        escaped = re.escape(alias)
        return bool(re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", lower_text))
    return bool(re.search(rf"\b{re.escape(alias)}\b", lower_text))


def extract_skills(raw_text: str) -> List[Dict]:
    if not raw_text or not raw_text.strip():
        return []
    lower_text = raw_text.lower()
    detected = []
    seen = set()
    for canonical, category, aliases in SKILL_TAXONOMY:
        if any(_matches_token(lower_text, alias) for alias in aliases):
            if canonical not in seen:
                seen.add(canonical)
                detected.append({
                    "name": canonical,
                    "category": category,
                    "user_added": False
                })
    return detected


def infer_category(skill: str) -> str:
    lower = skill.lower()
    if any(k in lower for k in ["data", "ml", "ai", "spark", "bi", "streamlit"]):
        return "Data Science & AI"
    if any(k in lower for k in ["web", "react", "vue", "angular", "api", "css"]):
        return "Web Development"
    if any(k in lower for k in ["lang", "rust", "swift", "php", "scala"]):
        return "Programming"
    return "Soft Skills & Tools"


def normalize_skill(raw_skill: str, user_added: bool = True) -> Dict:
    trimmed = raw_skill.strip()
    known = NORMALIZED_LOOKUP.get(trimmed.lower())
    if known:
        return {"name": known[0], "category": known[1], "user_added": user_added}
    formatted = trimmed[0].upper() + trimmed[1:] if trimmed else trimmed
    return {"name": formatted, "category": infer_category(trimmed), "user_added": user_added}


def canonical_skill_name(skill: str) -> str:
    known = NORMALIZED_LOOKUP.get(skill.strip().lower())
    return known[0] if known else skill.strip()


def category_for(skill: str) -> str:
    known = NORMALIZED_LOOKUP.get(skill.strip().lower())
    return known[1] if known else infer_category(skill)


def all_known_skills() -> List[str]:
    return [item[0] for item in SKILL_TAXONOMY]
