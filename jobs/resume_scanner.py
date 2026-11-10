import re

from pypdf import PdfReader


MAX_RESUME_PAGES = 20
MAX_RESUME_FILE_SIZE = 10 * 1024 * 1024
MAX_RESUME_TEXT_LENGTH = 100_000

SKILL_CATALOG = {
    "html": ("html",),
    "css": ("css",),
    "javascript": ("javascript", "js"),
    "typescript": ("typescript",),
    "react": ("react",),
    "node.js": ("node.js", "nodejs"),
    "django": ("django",),
    "flask": ("flask",),
    "python": ("python",),
    "java": ("java",),
    "spring": ("spring boot", "spring"),
    "sql": ("sql", "mysql", "postgresql", "sqlite"),
    "data analysis": ("data analysis", "data analytics"),
    "pandas": ("pandas",),
    "machine learning": ("machine learning", "scikit-learn", "tensorflow", "pytorch"),
    "figma": ("figma",),
    "ui/ux": ("ui/ux", "ui design", "ux design", "user experience"),
    "wireframing": ("wireframe", "wireframing"),
    "prototyping": ("prototype", "prototyping"),
    "cybersecurity": ("cybersecurity", "cyber security", "penetration testing"),
    "network security": ("network security",),
    "linux": ("linux",),
    "git": ("git", "github"),
    "rest api": ("rest api", "restful api"),
    "communication": ("communication",),
}

CATEGORY_SKILLS = {
    "web development": ("html", "css", "javascript", "react", "django", "node.js"),
    "python": ("python", "django", "flask", "pandas"),
    "ui/ux": ("figma", "ui/ux", "wireframing", "prototyping"),
    "java": ("java", "spring", "sql"),
    "cyber security": ("cybersecurity", "network security", "linux"),
    "data science": ("python", "data analysis", "pandas", "machine learning"),
}


def extract_resume_text(pdf_file):
    reader = PdfReader(pdf_file, strict=False)
    if reader.is_encrypted:
        raise ValueError("This PDF is password-protected and cannot be scanned.")
    if len(reader.pages) > MAX_RESUME_PAGES:
        raise ValueError(
            f"PDFs must contain no more than {MAX_RESUME_PAGES} pages."
        )

    text = " ".join(
        page.extract_text() or ""
        for page in reader.pages
    )
    text = text[:MAX_RESUME_TEXT_LENGTH]
    if not text.strip():
        raise ValueError(
            "No selectable text was found. Scanned-image PDFs are not supported."
        )
    return text


def _find_skills(text):
    normalized_text = text.casefold()
    found = []
    for skill, aliases in SKILL_CATALOG.items():
        if any(
            re.search(
                rf"(?<!\w){re.escape(alias.casefold())}(?!\w)",
                normalized_text,
            )
            for alias in aliases
        ):
            found.append(skill)
    return found


def analyze_resume(text, job, profile):
    resume_skills = _find_skills(text)
    profile_skills = _find_skills(
        " ".join(
            (
                profile.skills or "",
                profile.bio or "",
                profile.user.skills or "",
                profile.user.experience or "",
                profile.user.education or "",
            )
        )
    )
    candidate_skills = list(dict.fromkeys(resume_skills + profile_skills))

    job_text = " ".join((job.title or "", job.category or "", job.description or ""))
    job_skills = _find_skills(job_text)
    category_skills = CATEGORY_SKILLS.get((job.category or "").casefold(), ())
    required_skills = job_skills or list(category_skills)
    matched_skills = [skill for skill in required_skills if skill in candidate_skills]
    missing_skills = [skill for skill in required_skills if skill not in candidate_skills]

    if required_skills:
        fit_score = round(100 * len(matched_skills) / len(required_skills))
        if fit_score >= 70:
            fit_summary = "Strong keyword match"
        elif fit_score >= 40:
            fit_summary = "Partial keyword match"
        else:
            fit_summary = "Limited keyword match"
        summary = (
            f"{fit_summary} for {job.title}: "
            f"{len(matched_skills)} of {len(required_skills)} relevant skills "
            "were found in the resume or student profile."
        )
    else:
        fit_score = None
        summary = (
            "The job description does not mention enough recognized skills "
            "to calculate a keyword match."
        )

    return {
        "summary": summary,
        "fit_score": fit_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": resume_skills,
    }
