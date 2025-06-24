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
