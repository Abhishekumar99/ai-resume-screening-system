# 🎨 Streamlit UI Upgrade for AI Resume Screening System


import streamlit as st
from parser import extract_text_from_pdf
from nlp_processing import preprocess_text
from model import calculate_similarity, get_missing_skills

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1 {
    text-align: center;
    color: white;
    font-size: 52px !important;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #A0A0A0;
    font-size: 18px;
    margin-bottom: 20px;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #4F46E5, #9333EA);
    color: white;
    border-radius: 12px;
    height: 3.2em;
    font-size: 18px;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #4338CA, #7E22CE);
    color: white;
}

.result-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #1E293B;
    margin-top: 20px;
}

.skill-box {
    background-color: #111827;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ================= FUNCTIONS =================
def extract_skills(text):
    SKILLS = [
        "python", "machine", "learning", "sql", "react", "fastapi",
        "django", "api", "github", "numpy", "scikit", "data",
        "algorithm", "database", "backend", "frontend"
    ]

    words = text.split()
    extracted = [word for word in words if word in SKILLS]

    return " ".join(set(extracted))


# ================= HEADER =================
st.markdown(
    """
    <style>
    .hero-container {
        background: linear-gradient(90deg, #1E3A8A, #2563EB);
        padding: 40px 20px;
        border-radius: 22px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.35);
    }

    .hero-title {
        color: white;
        font-weight: 800;
        line-height: 1.2;
        margin: 0;
        font-size: 64px;
    }

    .hero-subtitle {
        color: #E0E7FF;
        font-size: 20px;
        margin-top: 12px;
    }

    @media (max-width: 768px) {
        .hero-title {
            font-size: 42px;
        }

        .hero-subtitle {
            font-size: 16px;
        }

        .hero-container {
            padding: 30px 15px;
        }
    }
    </style>

    <div class="hero-container">
        <h1 class="hero-title">🧠 AI Resume Screening System</h1>
        <div class="hero-subtitle">AI-Powered ATS Resume Analyzer</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ================= INPUT SECTION =================
with st.container(border=True):
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

    job_description = st.text_area(
        "📝 Paste Job Description",
        height=220,
        placeholder="Paste job description here..."
    )


# ================= ANALYZE BUTTON =================
if st.button("🚀 Analyze Resume"):

    if uploaded_file is not None and job_description != "":

        with st.spinner("Analyzing resume with AI..."):

            # Save uploaded file
            with open("temp_resume.pdf", "wb") as f:
                f.write(uploaded_file.read())

            # Extract text
            raw_text = extract_text_from_pdf("temp_resume.pdf")

            # Preprocess text
            clean_resume = preprocess_text(raw_text)
            clean_job = preprocess_text(job_description)

            # Extract skills
            clean_resume = extract_skills(clean_resume)
            clean_job = extract_skills(clean_job)

            # Similarity score
            score = calculate_similarity(clean_resume, clean_job)
            percentage = round(score * 100, 2)

            # Missing skills
            missing_skills = get_missing_skills(clean_resume, clean_job)


        # ================= RESULTS =================
        st.markdown("---")

        st.subheader("🎯 Match Score")
        st.progress(int(percentage))

        st.markdown(
            f"""
            <div class='result-box'>
                <h2 style='color:#22C55E;'>📊 {percentage}% Match</h2>
            </div>
            """,
            unsafe_allow_html=True
        )


        # ================= FEEDBACK =================
        st.subheader("💡 AI Feedback")

        if percentage >= 75:
            st.success("Excellent match! Your resume is highly aligned with the job description.")
        elif percentage >= 50:
            st.warning("Good match. Adding a few more relevant skills can improve compatibility.")
        else:
            st.error("Low match score. Improve resume keywords and required skills.")


        # ================= MISSING SKILLS =================
        st.subheader("❌ Missing Skills")

        if missing_skills:
            for skill in missing_skills:
                st.markdown(
                    f"<div class='skill-box'>⚡ {skill}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.success("No major missing skills detected 🎉")

    else:
        st.warning("Please upload a resume and paste a job description.")


# ================= FOOTER =================
st.markdown("---")
st.caption("Built with ❤️ using Python, NLP, Scikit-learn, and Streamlit")







