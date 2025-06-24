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
