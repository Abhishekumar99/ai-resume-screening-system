from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from parser import extract_text_from_pdf
from nlp_processing import preprocess_text


def calculate_similarity(resume_text, job_description):
    
    documents = [resume_text, job_description]
    
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    return similarity_score[0][0]


def get_missing_skills(resume, job):
    resume_words = set(resume.split())
    job_words = set(job.split())
    
    missing = job_words - resume_words
    missing = [word for word in missing if len(word) > 3]
    
    return missing[:10]
def extract_skills(text):
    SKILLS = [
        "python", "machine", "learning", "sql", "react", "fastapi",
        "django", "api", "github", "numpy", "scikit", "data",
        "algorithm", "database", "backend", "frontend"
    ]
    
    words = text.split()
    
    extracted = [word for word in words if word in SKILLS]
    
    return " ".join(set(extracted))

# ================== MAIN CODE ==================
if __name__ == "__main__":
    
    resume_path = "data/sample_resume.pdf"
    
    job_description = """
We are looking for a Software Engineer / AI-ML Developer with strong knowledge of Python,
machine learning, and backend development.

Responsibilities:
- Develop and deploy scalable backend systems using FastAPI or Django
- Build machine learning models for prediction and optimization tasks
- Work with REST APIs and integrate third-party services such as GitHub APIs
- Design and implement full-stack applications using React and modern frontend tools
- Perform testing using pytest and ensure code quality

Required Skills:
- Strong proficiency in Python
- Knowledge of Machine Learning and Deep Learning concepts
- Experience with scikit-learn and NumPy
- Familiarity with Data Structures and Algorithms
- Experience in SQL and database management
- Experience with FastAPI or Django
- Understanding of REST APIs

Preferred Skills:
- Experience with React.js
- Knowledge of cloud deployment platforms like Render or AWS
- Familiarity with GitHub and version control systems
"""
    
    # 🔹 STEP 1: Extract text
    raw_text = extract_text_from_pdf(resume_path)
    
    # 🔹 STEP 2: Clean text
    clean_resume = preprocess_text(raw_text)
    clean_job = preprocess_text(job_description)

    # ✅ NEW STEP (ADD THIS)
    clean_resume = extract_skills(clean_resume)
    clean_job = extract_skills(clean_job)

    # ✅ STEP 3: PASTE HERE 👇 (IMPORTANT)
    print("\nCLEAN RESUME:\n", clean_resume[:300])
    print("\nCLEAN JOB:\n", clean_job[:300])

    # 🔹 STEP 4: Calculate similarity
    score = calculate_similarity(clean_resume, clean_job)
    
    print("\n🎯 MATCH SCORE:", round(score * 100, 2), "%")

    # 🔹 STEP 5: Missing skills
    missing_skills = get_missing_skills(clean_resume, clean_job)
    
    print("\n❌ Missing Skills:")
    for skill in missing_skills:
        print("-", skill)