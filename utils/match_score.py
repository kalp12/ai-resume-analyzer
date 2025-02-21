from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_skills, job_skills):
    """ Compare extracted resume skills with job description skills. """
    if not resume_skills or not job_skills:
        return 0, job_skills, ["No skills detected. Try improving keyword optimization."]

    vectorizer = CountVectorizer().fit_transform([" ".join(resume_skills), " ".join(job_skills)])
    similarity = cosine_similarity(vectorizer)[0][1] * 100  # Convert to %

    missing_skills = list(set(job_skills) - set(resume_skills))
    suggestions = ["Consider learning " + skill for skill in missing_skills]

    return round(similarity, 2), missing_skills, suggestions
