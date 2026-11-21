"""
Sample Seed Data for CareerAI Streamlit Web App.
Clearly labeled DEMO DATA & SAMPLE JOB DATASET for demonstration and baseline TF-IDF matching.
"""

DEMO_RESUME_FILENAME = "Aarav_Sharma_BCA_DataScience_DEMO.pdf"

DEMO_RESUME_TEXT = """Aarav Sharma
aarav.sharma.demo@careerai.edu | +91 98765 43210 | github.com/aarav-demo | linkedin.com/in/aarav-demo

Professional Summary
Final-year BCA Data Science & Artificial Intelligence student passionate about machine learning, Python analytics, and full-stack data products. Built end-to-end NLP and predictive modeling applications using Python, Scikit-learn, Pandas, and SQL.

Education
Bachelor of Computer Applications (BCA) — Data Science & Artificial Intelligence
National Institute of Digital Studies, 2023 - 2026 | CGPA: 8.7/10

Technical Skills
Programming: Python, SQL, Java, JavaScript, Kotlin
Data Science: Machine Learning, Data Analysis, Pandas, NumPy, Scikit-learn, NLP, Power BI, Data Visualization, Statistics
Web & Tools: HTML, CSS, React, FastAPI, Git, REST API
Soft Skills: Problem Solving, Communication, Teamwork, Critical Thinking

Projects
Smart Resume Analyzer & Role Matcher (Final-Year Capstone)
- Built an NLP skill extraction and TF-IDF cosine similarity engine in Python and Kotlin to evaluate resumes against 12 sample tech job roles.
- Implemented structured section parsing and a transparent 100-point rubric with visual score breakdowns.

Customer Churn Prediction Dashboard
- Analyzed 7,000+ telecom customer records using Pandas, NumPy, and Scikit-learn classification models achieving 84% cross-validated accuracy.
- Visualized churn drivers and cohort retention trends in an interactive Power BI dashboard.

Campus Event Management Portal
- Developed a responsive web interface using React, HTML, CSS, and FastAPI REST endpoints backed by SQLite.

Work Experience
Data Analytics Intern — InsightGrid Labs (Demo Internship), Jun 2025 - Aug 2025
- Automated weekly SQL reporting queries and cleaned 15,000+ rows of sales logs using Python and Pandas, reducing manual spreadsheet preparation by 40%.
- Collaborated with a 4-member analytics team to build KPI dashboards for weekly sprint reviews.

Certifications
Google Data Analytics Professional Certificate (Coursework Completed)
Python for Data Science and Machine Learning — Coursera

Languages
English, Hindi"""

SAMPLE_JOB_ROLES = [
    {
        "title": "Python Developer",
        "category": "Software Engineering",
        "experience_level": "Entry / Junior",
        "summary": "Build backend services, automation scripts, and scalable APIs using Python ecosystems and clean software design.",
        "required_skills": ["Python", "SQL", "REST API", "Git", "Problem Solving"],
        "preferred_skills": ["FastAPI", "Django", "Docker", "Cloud Computing"],
        "responsibilities": [
            "Design and maintain modular Python backend services and data utilities.",
            "Write unit tests and optimize relational SQL queries.",
            "Collaborate with frontend and data teams via clean REST contracts."
        ]
    },
    {
        "title": "Data Analyst",
        "category": "Data & Analytics",
        "experience_level": "Entry / Junior",
        "summary": "Transform raw operational datasets into clear KPI reports, interactive BI dashboards, and actionable business insights.",
        "required_skills": ["SQL", "Python", "Data Analysis", "Pandas", "Power BI", "Advanced Excel"],
        "preferred_skills": ["Tableau", "Statistics", "Data Visualization", "Communication"],
        "responsibilities": [
            "Clean, join, and audit multi-source datasets using SQL and Python.",
            "Build interactive executive dashboards in Power BI or Tableau.",
            "Present clear trend summaries and anomaly findings to stakeholders."
        ]
    },
    {
        "title": "Data Scientist",
        "category": "Data & Analytics",
        "experience_level": "Junior / Mid",
        "summary": "Apply statistical modeling, exploratory analysis, and supervised machine learning to solve forecasting and classification problems.",
        "required_skills": ["Python", "Machine Learning", "Pandas", "NumPy", "Scikit-learn", "SQL", "Statistics"],
        "preferred_skills": ["Deep Learning", "NLP", "Data Visualization", "Tableau"],
        "responsibilities": [
            "Perform exploratory data analysis and feature engineering on large datasets.",
            "Train, cross-validate, and evaluate predictive ML models in Scikit-learn.",
            "Communicate model limitations and trade-offs transparently."
        ]
    },
    {
        "title": "Machine Learning Engineer",
        "category": "AI & Machine Learning",
        "experience_level": "Junior / Mid",
        "summary": "Productionize machine learning pipelines, model evaluation workflows, and scalable inference APIs.",
        "required_skills": ["Python", "Machine Learning", "Scikit-learn", "TensorFlow", "Docker", "Git"],
        "preferred_skills": ["PyTorch", "Deep Learning", "FastAPI", "Cloud Computing", "SQL"],
        "responsibilities": [
            "Build reproducible model training, validation, and packaging pipelines.",
            "Serve trained models behind low-latency FastAPI/REST endpoints.",
            "Monitor model drift, inference latency, and data quality."
        ]
    },
    {
        "title": "AI Engineer",
        "category": "AI & Machine Learning",
        "experience_level": "Junior / Mid",
        "summary": "Build applied AI products combining NLP, deep learning, semantic retrieval, and modern API engineering.",
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "NLP", "REST API", "FastAPI"],
        "preferred_skills": ["TensorFlow", "PyTorch", "Docker", "Cloud Computing", "Git"],
        "responsibilities": [
            "Design NLP pipelines, text classification, and semantic matching systems.",
            "Evaluate model accuracy, edge cases, and latency systematically.",
            "Integrate AI services safely into user-facing applications."
        ]
    },
    {
        "title": "Software Developer",
        "category": "Software Engineering",
        "experience_level": "Entry / Junior",
        "summary": "Develop reliable cross-tier applications with strong data structures, clean architecture, and collaborative version control.",
        "required_skills": ["Java", "Python", "SQL", "Git", "Problem Solving", "Teamwork"],
        "preferred_skills": ["C++", "JavaScript", "REST API", "Agile", "Docker"],
        "responsibilities": [
            "Implement tested application modules following clean architecture principles.",
            "Debug issues, review pull requests, and maintain technical documentation.",
            "Work in agile sprints to ship reliable user features."
        ]
    },
    {
        "title": "Frontend Developer",
        "category": "Web Development",
        "experience_level": "Entry / Junior",
        "summary": "Craft responsive, accessible, high-performance web user interfaces with modern component frameworks.",
        "required_skills": ["HTML", "CSS", "JavaScript", "React", "Git"],
        "preferred_skills": ["TypeScript", "Tailwind CSS", "REST API", "Communication"],
        "responsibilities": [
            "Build modular React components and responsive multi-device layouts.",
            "Integrate backend REST APIs with clean loading and error states.",
            "Ensure accessibility, semantic markup, and smooth UI transitions."
        ]
    },
    {
        "title": "Backend Developer",
        "category": "Web Development",
        "experience_level": "Junior / Mid",
        "summary": "Architect secure APIs, relational data schemas, authentication flows, and high-throughput server workloads.",
        "required_skills": ["Python", "SQL", "REST API", "FastAPI", "Git"],
        "preferred_skills": ["Node.js", "Django", "Docker", "Cloud Computing", "Java"],
        "responsibilities": [
            "Design normalized database schemas and efficient SQL queries.",
            "Implement secure authentication, input validation, and structured logging.",
            "Containerize and monitor backend API services."
        ]
    },
    {
        "title": "Full Stack Developer",
        "category": "Web Development",
        "experience_level": "Junior / Mid",
        "summary": "Own features end-to-end across modern web frontends, backend APIs, and relational databases.",
        "required_skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "Git"],
        "preferred_skills": ["TypeScript", "Python", "FastAPI", "Tailwind CSS", "Docker"],
        "responsibilities": [
            "Build responsive frontend views connected to typed backend endpoints.",
            "Model persistent database tables and enforce authorization checks.",
            "Write integration tests and streamline CI/CD delivery."
        ]
    },
    {
        "title": "Business Analyst",
        "category": "Data & Analytics",
        "experience_level": "Entry / Junior",
        "summary": "Bridge business requirements and data insights through structured KPI modeling, reporting, and stakeholder alignment.",
        "required_skills": ["Data Analysis", "SQL", "Advanced Excel", "Power BI", "Communication", "Critical Thinking"],
        "preferred_skills": ["Tableau", "Agile", "Leadership", "Python"],
        "responsibilities": [
            "Translate business goals into clear functional requirements and KPIs.",
            "Analyze operational metrics and deliver executive slide decks and dashboards.",
            "Coordinate between engineering, product, and operations teams."
        ]
    },
    {
        "title": "SQL Developer",
        "category": "Data & Analytics",
        "experience_level": "Entry / Junior",
        "summary": "Design relational schemas, stored procedures, ETL pipelines, and performance-tuned analytical SQL queries.",
        "required_skills": ["SQL", "Data Analysis", "Problem Solving", "Git"],
        "preferred_skills": ["Python", "Power BI", "Advanced Excel", "Cloud Computing"],
        "responsibilities": [
            "Write complex JOINs, CTEs, window functions, and indexed views.",
            "Maintain data integrity constraints and automated ETL quality checks.",
            "Optimize slow reporting queries for BI dashboards."
        ]
    },
    {
        "title": "Android Developer",
        "category": "Mobile Engineering",
        "experience_level": "Entry / Junior",
        "summary": "Build native Kotlin & Jetpack Compose Android apps with offline persistence, Material 3 UX, and MVVM architecture.",
        "required_skills": ["Kotlin", "Android Development", "Git", "REST API", "SQL"],
        "preferred_skills": ["Java", "Problem Solving", "Agile", "Teamwork"],
        "responsibilities": [
            "Develop responsive Material 3 Jetpack Compose interfaces for phones and tablets.",
            "Manage reactive state with ViewModels, Coroutines, Flows, and Room.",
            "Ensure accessibility, edge-to-edge layouts, and crash-free error handling."
        ]
    }
]
