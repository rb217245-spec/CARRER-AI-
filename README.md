# CareerAI — Smart Resume Analyzer & Job Recommendation System 

An interactive, full-featured **Streamlit** web application for resume evaluation and career intelligence. It parses **PDF, Word (DOCX), TXT, and Markdown** resumes, normalizes technical & soft skills via NLP matching, scores resumes transparently on a **100-point rubric**, recommends best-fit roles using **TF-IDF + Cosine Similarity**, generates step-by-step upskilling roadmaps, and exports downloadable **PDF / Markdown** reports

## Project Structure

```text
careerai_streamlit/
├── app.py                   # Main Streamlit application with multi-page sidebar navigation
├── requirements.txt         # Python dependencies
├── README.md                # Setup & usage guide
├── .env.example             # Safe environment variable template
├── .gitignore               # Git ignore rules for secrets, venv, cache & local resumes
├── .streamlit/
│   └── config.toml          # Clean light theme & upload settings
├── data/
│   ├── __init__.py
│   └── sample_data.py       # Demo BCA Data Science resume + 12 benchmark tech job roles
└── engine/
    ├── __init__.py
    ├── parser.py            # Multi-format text extractor & section-aware resume parser
    ├── skills.py            # NLP skill taxonomy & alias normalizer
    ├── scoring.py           # Deterministic 100-point resume rubric engine
    ├── recommender.py       # TF-IDF + Cosine Similarity matcher, skill gap & roadmap builder
    └── exporter.py          # PDF (fpdf2) and Markdown report generator
