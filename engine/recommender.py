"""
TF-IDF Vectorizer + Cosine Similarity Job Recommendation Engine
paired with Skill Gap Analysis and Personalized Learning Roadmap Generation.
"""
import math
import re
from typing import Dict, List
from engine.skills import canonical_skill_name, category_for

STOP_WORDS = {
    "and", "the", "for", "with", "that", "this", "from", "into", "your",
    "will", "have", "are", "using", "build", "work", "team", "role", "data"
}

SKILL_GUIDANCE_MAP = {
    "python": ("3–4 weeks", "Master Python syntax, data structures, OOP, virtual environments, and clean modular scripting.", "Build a CLI log analyzer and automated CSV data cleaner with unit tests."),
    "sql": ("2–3 weeks", "Practice JOINs, window functions, CTEs, aggregations, indexing, and query optimization.", "Design a relational retail analytics schema and write 15 KPI reporting queries."),
    "pandas": ("2 weeks", "Learn DataFrame cleaning, merging, groupby aggregations, missing-value handling, and time-series transforms.", "Perform exploratory data analysis on a public sales or healthcare dataset."),
    "numpy": ("1–2 weeks", "Understand vectorized array operations, broadcasting, linear algebra primitives, and performance profiling.", "Implement k-means clustering and cosine similarity from scratch using NumPy."),
    "scikit-learn": ("3 weeks", "Build end-to-end ML pipelines with preprocessing, cross-validation, classification/regression, and evaluation metrics.", "Train and compare Logistic Regression, Random Forest, and Gradient Boosting on a tabular dataset."),
    "machine learning": ("4–6 weeks", "Master supervised/unsupervised algorithms, bias-variance tradeoff, feature engineering, and model evaluation.", "Create an end-to-end churn prediction notebook with feature importance and confusion matrix analysis."),
    "deep learning": ("4–6 weeks", "Learn neural network architectures, backpropagation, regularization, CNNs, and transfer learning.", "Train an image or text classifier with validation curves and error analysis."),
    "tensorflow": ("3–4 weeks", "Build and train Keras Sequential/Functional models, custom callbacks, and saved model inference.", "Deploy a trained TensorFlow classifier behind a local REST endpoint."),
    "pytorch": ("3–4 weeks", "Understand tensors, autograd, Dataset/DataLoader, training loops, and model checkpointing.", "Fine-tune a pretrained model for sentiment or document classification."),
    "power bi": ("2 weeks", "Master Power Query data shaping, star-schema modeling, DAX measures, and executive dashboard design.", "Publish an interactive multi-page sales & cohort KPI dashboard in Power BI."),
    "tableau": ("2 weeks", "Build calculated fields, parameters, interactive filters, and clear executive data stories.", "Design an interactive regional revenue and customer retention dashboard."),
    "advanced excel": ("1–2 weeks", "Master PivotTables, XLOOKUP/INDEX-MATCH, Power Query, conditional formulas, and financial/KPI modeling.", "Create an automated monthly expense and cohort KPI workbook."),
    "nlp": ("3 weeks", "Learn tokenization, lemmatization, TF-IDF vectorization, NER, text classification, and embeddings.", "Build a resume-to-job semantic matcher and keyword extraction benchmark."),
    "statistics": ("2–3 weeks", "Solidify probability distributions, hypothesis testing, p-values, confidence intervals, and A/B test sizing.", "Run a complete A/B test statistical evaluation report on sample funnel conversion data."),
    "react": ("3–4 weeks", "Learn component composition, hooks, state management, routing, and accessible UI patterns.", "Build a responsive task and analytics dashboard consuming a REST API."),
    "javascript": ("2–3 weeks", "Master ES6+, closures, async/await, Promises, DOM events, and modular architecture.", "Create an interactive client-side Kanban board with local persistence."),
    "typescript": ("1–2 weeks", "Adopt static interfaces, generics, discriminated unions, and strict type checking.", "Refactor a JavaScript web app to strict TypeScript with typed API models."),
    "html": ("1 week", "Master semantic HTML5 tags, forms, validation, and WCAG accessibility fundamentals.", "Build a semantic, keyboard-accessible portfolio landing page."),
    "css": ("1–2 weeks", "Practice Flexbox, CSS Grid, responsive media queries, custom properties, and clean spacing systems.", "Recreate a responsive SaaS pricing and dashboard grid layout."),
    "node.js": ("2–3 weeks", "Build asynchronous HTTP servers, middleware, validation, authentication, and database integration.", "Create a RESTful bookmark API with JWT auth and SQLite persistence."),
    "fastapi": ("2 weeks", "Design typed Pydantic schemas, async endpoints, dependency injection, and OpenAPI documentation.", "Build a resume scoring microservice with FastAPI and automated pytest coverage."),
    "django": ("3 weeks", "Learn Django ORM, migrations, authentication, class-based views, and Django REST Framework.", "Create a multi-user project tracker backend with role-based permissions."),
    "rest api": ("1–2 weeks", "Understand HTTP verbs, status codes, pagination, error schemas, rate limiting, and API testing.", "Document and test a CRUD API contract using OpenAPI specifications."),
    "kotlin": ("3 weeks", "Master null safety, coroutines, Flows, sealed classes, data classes, and idiomatic Android architecture.", "Build a clean MVVM Kotlin module with unit-tested business logic."),
    "android development": ("4 weeks", "Learn Jetpack Compose, Material 3, Room persistence, ViewModel state, and lifecycle management.", "Build an offline-first productivity Android app with Room and Compose."),
    "java": ("3 weeks", "Strengthen OOP design, Collections, Streams, concurrency fundamentals, and exception handling.", "Implement a multithreaded order-processing service with JUnit tests."),
    "git": ("1 week", "Practice branching strategies, rebasing, pull requests, conflict resolution, and clean commit hygiene.", "Maintain a multi-branch feature workflow with clear commit history on GitHub."),
    "docker": ("1–2 weeks", "Write multi-stage Dockerfiles, manage images/volumes, and orchestrate services with Docker Compose.", "Containerize a backend API and database with a reproducible docker-compose.yml."),
    "cloud computing": ("2–3 weeks", "Learn IAM basics, compute/serverless hosting, managed databases, logging, and cost controls.", "Deploy a containerized API with environment-based secrets and health monitoring."),
    "communication": ("Ongoing (2 weeks focus)", "Practice structured technical storytelling, concise written summaries, and stakeholder alignment.", "Write an executive 1-page case study summarizing a technical project's architecture and impact.")
}


def _tokenize(text: str) -> List[str]:
    cleaned = re.sub(r"[^a-z0-9+#.\s]", " ", text.lower())
    return [tok for tok in cleaned.split() if len(tok) >= 2 and tok not in STOP_WORDS]


def _compute_tfidf_vectors(documents: List[List[str]]) -> List[Dict[str, float]]:
    doc_count = float(len(documents))
    df: Dict[str, int] = {}
    for tokens in documents:
        for term in set(tokens):
            df[term] = df.get(term, 0) + 1

    vectors = []
    for tokens in documents:
        term_counts: Dict[str, int] = {}
        for term in tokens:
            term_counts[term] = term_counts.get(term, 0) + 1

        weights: Dict[str, float] = {}
        norm_sq = 0.0
        for term, count in term_counts.items():
            tf = 1.0 + math.log(float(count))
            idf = math.log((doc_count + 1.0) / (df.get(term, 1) + 1.0)) + 1.0
            w = tf * idf
            weights[term] = w
            norm_sq += w * w

        norm = max(math.sqrt(norm_sq), 1e-9)
        vectors.append({k: v / norm for k, v in weights.items()})
    return vectors


def _cosine_similarity(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    if not v1 or not v2:
        return 0.0
    smaller, larger = (v1, v2) if len(v1) <= len(v2) else (v2, v1)
    return sum(w1 * larger[term] for term, w1 in smaller.items() if term in larger)


def recommend_jobs(resume_text: str, detected_skills: List[Dict], job_roles: List[Dict]) -> List[Dict]:
    if not job_roles:
        return []

    user_skill_names = {canonical_skill_name(s["name"]) for s in detected_skills}
    user_skill_lower = {s.lower() for s in user_skill_names}

    resume_doc = resume_text + " " + (" ".join(user_skill_names) + " ") * 3
    job_docs = []
    for role in job_roles:
        doc = (
            f"{role['title']} {role['category']} {role['summary']} "
            + (" ".join(role["required_skills"]) + " ") * 3
            + " ".join(role["preferred_skills"]) + " "
            + " ".join(role["responsibilities"])
        )
        job_docs.append(doc)

    tokenized = [_tokenize(resume_doc)] + [_tokenize(d) for d in job_docs]
    vectors = _compute_tfidf_vectors(tokenized)
    candidate_vec = vectors[0]

    recommendations = []
    for idx, role in enumerate(job_roles):
        role_vec = vectors[idx + 1]
        cosine = max(0.0, min(1.0, _cosine_similarity(candidate_vec, role_vec)))

        req_canonical = [canonical_skill_name(s) for s in role["required_skills"]]
        matching = [s for s in req_canonical if s.lower() in user_skill_lower]
        missing = [s for s in req_canonical if s.lower() not in user_skill_lower]

        skill_overlap = round((len(matching) / len(req_canonical)) * 100) if req_canonical else 0
        tfidf_scaled = min(100.0, cosine * 135.0)
        blended_match = max(5, min(99, round((skill_overlap * 0.55) + (tfidf_scaled * 0.45))))

        if matching:
            reason = f"Matches {len(matching)}/{len(req_canonical)} core skills ({', '.join(matching[:4])}) · TF-IDF cosine: {cosine:.2f}"
        else:
            reason = f"Aligned via resume terminology & domain context · TF-IDF cosine: {cosine:.2f}"

        pref_missing = [
            canonical_skill_name(s)
            for s in role["preferred_skills"]
            if canonical_skill_name(s).lower() not in user_skill_lower
        ]
        next_to_learn = list(dict.fromkeys(missing + pref_missing))[:4]

        recommendations.append({
            "role": role,
            "title": role["title"],
            "category": role["category"],
            "experience_level": role["experience_level"],
            "match_percentage": blended_match,
            "tfidf_cosine": round(cosine, 3),
            "skill_overlap_pct": skill_overlap,
            "matching_skills": matching,
            "missing_skills": missing,
            "reason_summary": reason,
            "skills_to_learn_next": next_to_learn,
        })

    recommendations.sort(key=lambda x: (x["match_percentage"], x["tfidf_cosine"]), reverse=True)
    return recommendations


def analyze_skill_gap(detected_skills: List[Dict], target_role: Dict) -> Dict:
    user_lower = {canonical_skill_name(s["name"]).lower() for s in detected_skills}
    items = []

    for idx, skill in enumerate(target_role["required_skills"]):
        canonical = canonical_skill_name(skill)
        acquired = canonical.lower() in user_lower
        priority = "High Priority" if idx < 3 else "Medium Priority"
        items.append({
            "skill": canonical,
            "category": category_for(canonical),
            "type": "Core Required",
            "acquired": acquired,
            "priority": priority,
        })

    existing_names = {i["skill"].lower() for i in items}
    for skill in target_role["preferred_skills"]:
        canonical = canonical_skill_name(skill)
        if canonical.lower() not in existing_names:
            items.append({
                "skill": canonical,
                "category": category_for(canonical),
                "type": "Preferred",
                "acquired": canonical.lower() in user_lower,
                "priority": "Nice to Have",
            })

    req_acquired = sum(
        1 for s in target_role["required_skills"]
        if canonical_skill_name(s).lower() in user_lower
    )
    match_pct = round((req_acquired / len(target_role["required_skills"])) * 100) if target_role["required_skills"] else 0

    return {
        "target_role": target_role,
        "match_percentage": match_pct,
        "acquired_skills": [i["skill"] for i in items if i["acquired"]],
        "missing_skills": [i["skill"] for i in items if not i["acquired"]],
        "items": items,
    }


def generate_learning_roadmap(gap_report: Dict) -> List[Dict]:
    role_title = gap_report["target_role"]["title"]
    missing_items = [i for i in gap_report["items"] if not i["acquired"]]

    if not missing_items:
        return [{
            "step": 1,
            "skill": "Portfolio Capstone & System Design",
            "priority": "Medium Priority",
            "duration": "2–3 weeks",
            "objective": f"You already cover the baseline skills for {role_title}. Focus on production code quality, testing, and measurable portfolio case studies.",
            "project": f"Build and document an end-to-end {role_title} capstone project with clean README, architecture diagram, and automated tests."
        }]

    steps = []
    for idx, item in enumerate(missing_items, start=1):
        guide = SKILL_GUIDANCE_MAP.get(item["skill"].lower())
        default_dur = (
            "2–3 weeks" if item["priority"] == "High Priority"
            else ("1–2 weeks" if item["priority"] == "Medium Priority" else "1 week")
        )
        steps.append({
            "step": idx,
            "skill": item["skill"],
            "category": item["category"],
            "priority": item["priority"],
            "duration": guide[0] if guide else default_dur,
            "objective": guide[1] if guide else f"Build practical fluency in {item['skill']} and apply it to real-world {role_title} workflows.",
            "project": guide[2] if guide else f"Create a documented mini-project demonstrating {item['skill']} in a {role_title} use case.",
        })
    return steps
