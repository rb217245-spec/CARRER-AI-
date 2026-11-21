"""
Structured Resume Parser & Multi-Format Extractor (PDF, DOCX, TXT, MD).
Never fabricates missing data: unavailable fields are explicitly marked as "Not Found".
"""
import re
from typing import Dict, List, Optional, Tuple
from pypdf import PdfReader

try:
    import docx
except ImportError:
    docx = None

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"(?:\+?\d{1,3}[\s.\-]?)?(?:\(?\d{3}\)?[\s.\-]?)?\d{3}[\s.\-]?\d{4}")

SECTION_HEADER_PATTERNS = {
    "SUMMARY": re.compile(r"^(professional\s+summary|summary|profile|career\s+objective|objective|about\s+me)\s*:?$", re.I),
    "EDUCATION": re.compile(r"^(education|academic\s+background|qualifications|academics)\s*:?$", re.I),
    "EXPERIENCE": re.compile(r"^(work\s+experience|experience|employment\s+history|professional\s+experience|internships?|career\s+history)\s*:?$", re.I),
    "PROJECTS": re.compile(r"^(projects|academic\s+projects|personal\s+projects|key\s+projects|selected\s+projects)\s*:?$", re.I),
    "SKILLS": re.compile(r"^(skills|technical\s+skills|core\s+competencies|technologies|skills\s*&\s*tools)\s*:?$", re.I),
    "CERTIFICATIONS": re.compile(r"^(certifications?|licenses?\s*&\s*certifications?|courses?\s*&\s*certifications?|credentials)\s*:?$", re.I),
    "LANGUAGES": re.compile(r"^(languages|spoken\s+languages|languages\s+known)\s*:?$", re.I),
}

KNOWN_HUMAN_LANGUAGES = [
    "English", "Hindi", "Spanish", "French", "German", "Mandarin",
    "Japanese", "Korean", "Arabic", "Portuguese", "Russian", "Italian",
    "Bengali", "Tamil", "Telugu", "Marathi", "Gujarati", "Kannada", "Punjabi"
]

HEADER_STOP_WORDS = {
    "resume", "curriculum vitae", "cv", "profile", "summary",
    "contact", "email", "phone", "address", "linkedin", "github"
}


def extract_text_from_pdf(uploaded_file) -> Tuple[str, int, Optional[str]]:
    """Extracts text from a PDF file stream safely."""
    try:
        reader = PdfReader(uploaded_file)
        pages_text = []
        for page in reader.pages:
            txt = page.extract_text() or ""
            if txt.strip():
                pages_text.append(txt)
        full_text = "\n".join(pages_text).strip()
        if not full_text:
            return "", len(reader.pages), "No selectable text found in PDF (it may be a scanned image)."
        return full_text, len(reader.pages), None
    except Exception as exc:
        return "", 0, f"Failed to read PDF: {exc}"


def extract_text_from_docx(uploaded_file) -> Tuple[str, int, Optional[str]]:
    """Extracts paragraphs and table rows from a Word (.docx) resume."""
    if docx is None:
        return "", 0, "python-docx is not installed. Run: pip install python-docx"
    try:
        document = docx.Document(uploaded_file)
        lines = []
        for para in document.paragraphs:
            if para.text.strip():
                lines.append(para.text.strip())
        for table in document.tables:
            for row in table.rows:
                row_vals = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_vals:
                    lines.append(" | ".join(dict.fromkeys(row_vals)))
        full_text = "\n".join(lines).strip()
        if not full_text:
            return "", 1, "No readable text found inside the DOCX file."
        return full_text, 1, None
    except Exception as exc:
        return "", 0, f"Failed to read DOCX: {exc}"


def extract_text_from_file(uploaded_file) -> Tuple[str, str, Optional[str]]:
    """Unified extractor supporting PDF, DOCX, TXT, and MD resumes."""
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        text, pages, err = extract_text_from_pdf(uploaded_file)
        return text, f"{pages} PDF page(s)", err
    elif name.endswith(".docx"):
        text, _, err = extract_text_from_docx(uploaded_file)
        return text, "Word DOCX document", err
    else:
        try:
            raw = uploaded_file.read().decode("utf-8", errors="ignore").strip()
            if not raw:
                return "", "Text file", "The uploaded text file is empty."
            return raw, "Plain text file", None
        except Exception as exc:
            return "", "Text file", f"Failed to read text file: {exc}"


def _extract_phone(text: str) -> Optional[str]:
    for match in PHONE_REGEX.finditer(text):
        candidate = match.group(0).strip()
        digits = "".join(ch for ch in candidate if ch.isdigit())
        if 10 <= len(digits) <= 15 and not re.match(r"^(19|20)\d{2}.*", candidate):
            return candidate
    return None


def _extract_full_name(lines: List[str]) -> Optional[str]:
    for line in lines[:6]:
        lower = line.lower()
        if lower in HEADER_STOP_WORDS:
            continue
        if "@" in line or "http" in lower or "linkedin.com" in lower or "github.com" in lower:
            continue
        if any(ch.isdigit() for ch in line):
            continue
        if any(rx.match(line) for rx in SECTION_HEADER_PATTERNS.values()):
            continue

        words = [w for w in line.split() if w]
        if 2 <= len(words) <= 4 and all(
            all(ch.isalpha() or ch in ".-'" for ch in w) for w in words
        ):
            return line
    return None


def _partition_sections(lines: List[str]) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    current_section: Optional[str] = None

    for line in lines:
        cleaned_header = line.rstrip(":-—| ").strip()
        matched_section = next(
            (key for key, rx in SECTION_HEADER_PATTERNS.items() if rx.match(cleaned_header)),
            None
        )
        if matched_section:
            current_section = matched_section
            result.setdefault(matched_section, [])
            continue

        if ":" in line:
            left, right = line.split(":", 1)
            if right.strip():
                inline_key = next(
                    (key for key, rx in SECTION_HEADER_PATTERNS.items() if rx.match(left.strip())),
                    None
                )
                if inline_key:
                    result.setdefault(inline_key, []).append(right.strip())
                    continue

        if current_section:
            result.setdefault(current_section, []).append(line)

    return result


def _extract_fallback_lines(lines: List[str], hints: List[str]) -> List[str]:
    seen = set()
    out = []
    for line in lines:
        lower = line.lower()
        if any(h in lower for h in hints) and line not in seen:
            seen.add(line)
            out.append(line)
            if len(out) >= 6:
                break
    return out


def _extract_languages(section_lines: List[str], raw_text: str) -> List[str]:
    found = []
    if section_lines:
        joined = ", ".join(section_lines)
        for lang in KNOWN_HUMAN_LANGUAGES:
            if re.search(rf"\b{re.escape(lang)}\b", joined, re.I):
                if lang not in found:
                    found.append(lang)
        if not found:
            for item in re.split(r"[,|•/]", joined):
                item = item.strip()
                if 2 <= len(item) <= 24 and all(ch.isalpha() or ch in " ()" for ch in item):
                    if item not in found:
                        found.append(item)
    else:
        if "language" in raw_text.lower():
            for lang in KNOWN_HUMAN_LANGUAGES:
                if re.search(rf"\b{re.escape(lang)}\b", raw_text, re.I):
                    if lang not in found:
                        found.append(lang)
    return found


def parse_resume(raw_text: str) -> Dict:
    cleaned_lines = [
        line.strip()
        for line in raw_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        if line.strip()
    ]
    if not cleaned_lines:
        return {
            "full_name": "Not Found",
            "email": "Not Found",
            "phone": "Not Found",
            "summary": "Not Found",
            "education": [],
            "work_experience": [],
            "projects": [],
            "certifications": [],
            "languages": [],
        }

    email_match = EMAIL_REGEX.search(raw_text)
    email = email_match.group(0).strip() if email_match else "Not Found"
    phone = _extract_phone(raw_text) or "Not Found"
    full_name = _extract_full_name(cleaned_lines) or "Not Found"

    sections = _partition_sections(cleaned_lines)

    summary_lines = sections.get("SUMMARY", [])
    summary = " ".join(summary_lines)[:600] if summary_lines else "Not Found"

    education = sections.get("EDUCATION", []) or _extract_fallback_lines(
        cleaned_lines, ["b.tech", "b.sc", "bca", "mca", "m.tech", "bachelor", "master", "university", "college", "cgpa", "gpa"]
    )
    experience = sections.get("EXPERIENCE", [])
    projects = sections.get("PROJECTS", [])
    certifications = sections.get("CERTIFICATIONS", []) or _extract_fallback_lines(
        cleaned_lines, ["certified", "certification", "coursera", "udemy", "aws certified", "google data analytics", "microsoft certified"]
    )
    languages = _extract_languages(sections.get("LANGUAGES", []), raw_text)

    return {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "summary": summary,
        "education": education[:12],
        "work_experience": experience[:20],
        "projects": projects[:16],
        "certifications": certifications[:10],
        "languages": languages,
    }
