# CareerAI — Smart Resume Analyzer & Job Recommendation System (Streamlit Edition)

An interactive, full-featured **Streamlit** web application converted from the CareerAI Android architecture. It parses PDF/TXT resumes, normalizes technical & soft skills via NLP matching, scores resumes transparently on a 100-point rubric, recommends best-fit roles using **TF-IDF + Cosine Similarity**, generates step-by-step upskilling roadmaps, and exports downloadable PDF/Markdown reports.

## Project Structure

```text
careerai_streamlit/
├── app.py                  # Main Streamlit application with multi-page sidebar navigation
├── requirements.txt        # Python dependencies
├── README.md               # Setup & usage guide
├── .streamlit/
│   └── config.toml         # Clean light theme & upload settings
├── data/
│   ├── __init__.py
│   └── sample_data.py      # Demo BCA Data Science resume + 12 benchmark tech job roles
└── engine/
    ├── __init__.py
    ├── parser.py           # PDF text extractor & section-aware resume parser
    ├── skills.py           # NLP skill taxonomy & alias normalizer
    ├── scoring.py          # Deterministic 100-point resume rubric engine
    ├── recommender.py      # TF-IDF + Cosine Similarity matcher, skill gap & roadmap builder
    └── exporter.py         # PDF (fpdf2) and Markdown report generator
```

## Quick Start (Run Locally)

1. **Extract the ZIP file** and open a terminal inside the `careerai_streamlit` folder.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
4. Open the local URL shown in your terminal (usually `http://localhost:8501`).

## Key Features

- **Sidebar Navigation:** Switch smoothly between *Overview Dashboard*, *Upload & Resume Analyzer*, *Job Role Matcher*, *Skill Gap & Roadmap*, *Export Report*, and *Role Catalog Studio*.
- **Instant Demo Mode:** Pre-loaded with a realistic BCA Data Science sample resume so every chart, score, and recommendation works immediately on launch.
- **Live Skill Tag Editor:** Add or remove extracted skills and watch your 100-point score and TF-IDF job rankings recalculate in real time.
- **Interactive Plotly Visuals:** Horizontal rubric score breakdown, skill domain donut chart, job match bar chart, and skill readiness radar chart.
- **One-Click Exports:** Download a formatted **PDF Report** or **Markdown Action Plan**.
