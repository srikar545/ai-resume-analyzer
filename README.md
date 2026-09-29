# 📄 AI Resume Analyzer

An NLP-based web application that compares a resume with a job description
and identifies relevant and missing skills.

## 🚀 Features

- Resume vs Job Description text similarity
- TF-IDF based text analysis
- Cosine similarity scoring
- Skill extraction
- Matching skill detection
- Missing skill detection
- Skill coverage percentage
- Overall resume match score
- Personalized recommendations

## 🛠️ Tech Stack

- Python
- Streamlit
- Scikit-learn
- TF-IDF
- Cosine Similarity

## 📊 How It Works

The application analyzes two inputs:

1. Resume
2. Job Description

It calculates:

### Text Similarity

TF-IDF converts the text into numerical vectors and cosine similarity
measures how similar the two documents are.

### Skill Coverage

The application detects technical skills mentioned in the job description
and checks which of those skills appear in the resume.

### Overall Score

The current score combines:

- 60% Skill Coverage
- 40% Text Similarity

## ▶️ Run Locally

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>