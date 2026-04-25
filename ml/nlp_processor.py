import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

SKILL_KEYWORDS = {
    "programming": ["python", "java", "javascript", "c++", "react", "node", "sql", "html", "css", "typescript"],
    "data": ["machine learning", "data analysis", "statistics", "tableau", "power bi", "excel", "pandas", "numpy", "tensorflow"],
    "management": ["leadership", "project management", "agile", "scrum", "team lead", "strategy", "planning", "budgeting"],
    "design": ["figma", "photoshop", "illustrator", "ux", "ui", "wireframe", "prototyping", "design thinking"],
    "communication": ["presentation", "negotiation", "stakeholder", "client", "writing", "documentation"],
    "devops": ["aws", "docker", "kubernetes", "ci/cd", "linux", "git", "jenkins", "azure", "gcp"],
    "finance": ["accounting", "financial analysis", "forecasting", "auditing", "taxation", "erp", "sap"],
    "marketing": ["seo", "sem", "social media", "content", "branding", "analytics", "campaigns", "crm"],
}

def extract_skills_from_resume(text):
    if not text:
        return []

    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)

    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [t for t in tokens if t not in stop_words and len(t) > 2]

    found_skills = []
    text_lower = text

    for category, keywords in SKILL_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_skills.append(keyword)

    found_skills = list(set(found_skills))
    return found_skills


def build_employee_profile(form_data, resume_skills=None):
    profile = {
        "name": form_data.get("name", ""),
        "experience_years": int(form_data.get("experience_years", 0)),
        "performance_score": float(form_data.get("performance_score", 5.0)),
        "current_role": form_data.get("current_role", ""),
        "preferred_role": form_data.get("preferred_role", ""),
        "skills": form_data.getlist("skills") if hasattr(form_data, 'getlist') else form_data.get("skills", []),
        "education_level": form_data.get("education_level", "Bachelor's"),
        "department": form_data.get("department", ""),
    }

    if resume_skills:
        combined = list(set(profile["skills"] + resume_skills))
        profile["skills"] = combined
        profile["resume_skills_extracted"] = resume_skills

    return profile