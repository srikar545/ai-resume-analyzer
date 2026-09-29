import streamlit as st
from pypdf import PdfReader

from analyzer import calculate_match_score, analyze_skills


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

    /* Main page */
    .stApp {
        background: #0b1120;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .hero {
        text-align: center;
        padding: 20px 0 35px 0;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #94a3b8;
    }

    /* Input labels */
    .input-label {
        font-size: 16px;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 8px;
    }

    /* Text areas */
    textarea {
        background-color: #111827 !important;
        color: #e5e7eb !important;
        border: 1px solid #263449 !important;
        border-radius: 12px !important;
    }

    textarea:focus {
        border: 1px solid #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }

    /* Analyze button */
    .stButton > button {
        width: 100%;
        height: 48px;
        border-radius: 10px;
        border: none;
        background: #2563eb;
        color: white;
        font-size: 16px;
        font-weight: 600;
        margin-top: 12px;
    }

    .stButton > button:hover {
        background: #1d4ed8;
        color: white;
    }

    /* Section heading */
    .section-title {
        font-size: 24px;
        font-weight: 650;
        color: #f8fafc;
        margin-top: 30px;
        margin-bottom: 18px;
    }

    /* Metric cards */
    .metric-card {
        background: #111827;
        border: 1px solid #263449;
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        min-height: 125px;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 30px;
        font-weight: 700;
    }

    /* Skill cards */
    .skill-card {
        background: #111827;
        border: 1px solid #263449;
        border-radius: 14px;
        padding: 20px;
        min-height: 150px;
    }

    .skill-title {
        color: #f8fafc;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .skill-item {
        display: inline-block;
        background: #172554;
        color: #93c5fd;
        border: 1px solid #1d4ed8;
        padding: 6px 10px;
        border-radius: 20px;
        margin: 4px;
        font-size: 13px;
    }

    .missing-item {
        display: inline-block;
        background: #3f1d1d;
        color: #fca5a5;
        border: 1px solid #7f1d1d;
        padding: 6px 10px;
        border-radius: 20px;
        margin: 4px;
        font-size: 13px;
    }

    /* Recommendation */
    .recommendation {
        background: #111827;
        border-left: 4px solid #3b82f6;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        color: #cbd5e1;
    }

    /* Divider */
    hr {
        border-color: #263449;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">📄 AI Resume Analyzer</div>
    <div class="hero-subtitle">
        Analyze your resume against a job description using NLP
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        '<div class="input-label">📄 Your Resume</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload your Resume",
        type=["pdf"],
        help="Upload your resume as a PDF file."
    )




with col2:
    st.markdown(
        '<div class="input-label">💼 Job Description</div>',
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "Job Description",
        height=300,
        placeholder="Paste the job description here...",
        label_visibility="collapsed"
    )


resume = ""

if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    for page in reader.pages:

        text = page.extract_text()

        if text:
            resume += text
            
analyze = st.button("Analyze Resume")


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

if analyze:

    if not resume.strip() or not job_description.strip():

        st.warning(
            "Please provide both your resume and the job description."
        )

    else:

        text_similarity = calculate_match_score(
            resume,
            job_description
        )

        analysis = analyze_skills(
            resume,
            job_description
        )

        skill_coverage = analysis["coverage"]

        overall_score = (
            skill_coverage * 0.60
            + text_similarity * 0.40
        )

        # --------------------------------------------------
        # SCORE SECTION
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">📊 Analysis Overview</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Overall Score</div>
                <div class="metric-value">{overall_score:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Skill Coverage</div>
                <div class="metric-value">{skill_coverage:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Text Similarity</div>
                <div class="metric-value">{text_similarity:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)


        # --------------------------------------------------
        # SKILL SECTION
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">🧠 Skill Analysis</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            matching_html = ""

            for skill in analysis["matching_skills"]:
                matching_html += (
                    f'<span class="skill-item">✓ {skill}</span>'
                )

            if not matching_html:
                matching_html = "No matching skills detected."

            st.markdown(f"""
            <div class="skill-card">
                <div class="skill-title">✅ Matching Skills</div>
                {matching_html}
            </div>
            """, unsafe_allow_html=True)


        with col2:

            missing_html = ""

            for skill in analysis["missing_skills"]:
                missing_html += (
                    f'<span class="missing-item">✗ {skill}</span>'
                )

            if not missing_html:
                missing_html = "No missing skills detected."

            st.markdown(f"""
            <div class="skill-card">
                <div class="skill-title">⚠️ Missing Skills</div>
                {missing_html}
            </div>
            """, unsafe_allow_html=True)


        # --------------------------------------------------
        # RECOMMENDATIONS
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">💡 Recommendations</div>',
            unsafe_allow_html=True
        )

        if analysis["missing_skills"]:

            for skill in analysis["missing_skills"]:

                st.markdown(
                    f"""
                    <div class="recommendation">
                        Consider adding experience, coursework, or a project
                        demonstrating <strong>{skill.upper()}</strong>.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.markdown(
                """
                <div class="recommendation">
                    Your resume contains all detected skills from the job
                    description.
                </div>
                """,
                unsafe_allow_html=True
            )


        # --------------------------------------------------
        # DISCLAIMER
        # --------------------------------------------------

        st.markdown("---")

        st.caption(
            "Note: The score is an automated NLP-based indicator and "
            "does not represent the probability of getting the job."
        )