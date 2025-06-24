### Streamlit App for AI-Powered Resume Ranker

# app.py
import streamlit as st
from utils.parser import extract_text
from utils.matcher import match_resume_to_job
from utils.ranker import rank_resume
from utils.suggester import generate_suggestions
import json
import os

st.set_page_config(page_title="AI Resume Ranker", layout="wide")
st.title("📄 AI-Powered Resume Ranker with Feedback")

st.markdown("""
Upload your resume and compare it against popular job descriptions or your own custom job role input. Get a score and personalized feedback.
""")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
input_method = st.radio("Choose how you want to provide the job description:", ("Select from predefined roles", "Enter your own job description"))

if input_method == "Select from predefined roles":
    with open("data/job_descriptions.json") as f:
        jd_data = json.load(f)
    job_role = st.selectbox("Select Job Role", list(jd_data.keys()))
    job_desc = jd_data[job_role]
else:
    job_desc = st.text_area("Paste your custom job description below:")

if uploaded_file and job_desc:
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Resume uploaded!")

    resume_text = extract_text(file_path)
    matched, missing = match_resume_to_job(resume_text, job_desc)
    score = rank_resume(matched, job_desc)
    suggestions = generate_suggestions(missing, resume_text)

    col1, col2 = st.columns(2)
    col1.metric("Resume Score", f"{score}/100")
    col2.metric("Matched Keywords", f"{len(matched)}")

    st.subheader("✅ Matched Skills")
    st.write(", ".join(matched) if matched else "None")

    st.subheader("❌ Missing Skills")
    st.write(", ".join(missing) if missing else "None")

    st.subheader("📌 Suggestions for Improvement")
    for s in suggestions:
        st.markdown(f"- {s}")

### utils/parser.py
import docx2txt
import fitz  # PyMuPDF

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        return "".join(page.get_text() for page in doc)
    elif file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    return ""

### utils/matcher.py
import spacy

nlp = spacy.load("en_core_web_sm")

def match_resume_to_job(resume_text, job_desc):
    resume_doc = nlp(resume_text.lower())
    job_doc = nlp(job_desc.lower())

    resume_tokens = set(token.lemma_ for token in resume_doc if token.is_alpha)
    job_tokens = set(token.lemma_ for token in job_doc if token.is_alpha)

    matched = resume_tokens & job_tokens
    missing = job_tokens - resume_tokens

    return list(matched), list(missing)

### utils/ranker.py
def rank_resume(matched, job_desc):
    total = len(job_desc.split())
    return min(int((len(matched) / total) * 100), 100)

### utils/suggester.py
def generate_suggestions(missing_keywords, resume_text):
    suggestions = []

    if "python" in missing_keywords:
        suggestions.append("Consider adding Python experience.")
    if "sql" in missing_keywords:
        suggestions.append("Include your SQL/database experience.")
    if "project" not in resume_text.lower():
        suggestions.append("Add a 'Projects' section with hands-on examples.")
    if "summary" not in resume_text.lower():
        suggestions.append("Include a Professional Summary at the top.")
    if not any(tool in resume_text.lower() for tool in ["matplotlib", "tableau", "seaborn"]):
        suggestions.append("Mention data visualization tools you've used.")

    return suggestions

