
import streamlit as st
from parser import extract_text_from_pdf
from nlp_processing import preprocess_text
from model import calculate_similarity, get_missing_skills

st.set_page_config(page_title="AI Resume Screener", layout="centered")
st.markdown("---")
st.set_page_config(page_title="AI Resume Screener", layout="centered")



# Skill extractor (same as model)
def extract_skills(text):
    SKILLS = [
        "python", "machine", "learning", "sql", "react", "fastapi",
        "django", "api", "github", "numpy", "scikit", "data",
        "algorithm", "database", "backend", "frontend"
    ]
    
    words = text.split()
    extracted = [word for word in words if word in SKILLS]
    
    return " ".join(set(extracted))


# UI Title
st.title("🧠 AI Resume Screening System")

# Upload Resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job Description Input
job_description = st.text_area("Paste Job Description")

# Button
if st.button("Analyze Resume"):
    with st.spinner("Analyzing resume..."):
    
     if uploaded_file is not None and job_description != "":
        
        # Save uploaded file
        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.read())
        
        # Extract text
        raw_text = extract_text_from_pdf("temp_resume.pdf")
        
        # Preprocess
        clean_resume = preprocess_text(raw_text)
        clean_job = preprocess_text(job_description)
        
        # Extract skills
        clean_resume = extract_skills(clean_resume)
        clean_job = extract_skills(clean_job)
        
        # Similarity
        score = calculate_similarity(clean_resume, clean_job)
        
        # Missing skills
        missing_skills = get_missing_skills(clean_resume, clean_job)
        
        # Display results
        st.subheader("🎯 Match Score")

        percentage = round(score * 100, 2)

        st.progress(int(percentage))
        st.success(f"{percentage} %")
        
        st.subheader("❌ Missing Skills")
        
        if missing_skills:
           for skill in missing_skills:
              st.error(skill)
        else:
           st.success("No major missing skills 🎉")
           
    
     else:
        st.warning("Please upload resume and enter job description")

