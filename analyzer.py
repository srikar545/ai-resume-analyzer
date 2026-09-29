from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "streamlit",
    "fastapi",
    "flask",
    "django",
    "docker",
    "aws",
    "azure",
    "git",
    "github",
    "rest api",
    "javascript",
    "html",
    "css",
    "react",
    "node.js",
    "mysql",
    "mongodb",
    "linux"
]


def calculate_match_score(resume, job_description):
    documents = [resume, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    return round(similarity * 100, 2)


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills


def analyze_skills(resume, job_description):
    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job_description)

    matching_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    if job_skills:
        coverage = (len(matching_skills) / len(job_skills)) * 100
    else:
        coverage = 0

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "coverage": round(coverage, 2)
    }


if __name__ == "__main__":
    resume = "Python SQL Machine Learning Git"
    job = "Python SQL Machine Learning Docker AWS"

    print("Match Score:", calculate_match_score(resume, job))
    print("Skill Analysis:", analyze_skills(resume, job))