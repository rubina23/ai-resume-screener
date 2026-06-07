# 📄 AI-Driven Resume Screener & Smart Feedback System (ATS System) 

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-F9AB00.svg)

An advanced Generative AI-backed Applicant Tracking System (ATS) built with Python, Streamlit, and Google Gemini AI. This application evaluates resumes against specific Job Descriptions, calculates a match score, identifies missing keywords, and provides comprehensive HR-level feedback using Large Language Models (LLMs).

🔗 **Live Demo:** https://ai-resume-screener-ats.streamlit.app/

## 🚀 Features
* **Resume Parsing:** Extracts text directly from uploaded PDF resumes.
* **Smart ATS Scoring:** Uses NLP techniques (TF-IDF & Cosine Similarity) to calculate a precise matching percentage.
* **Keyword Gap Analysis:** Automatically identifies critical keywords and skills present in the Job Description but missing from your resume, providing actionable insights for optimization.
* **Advanced AI HR Review:** Integrates Google Gemini AI (`gemini-1.5-flash`) to generate detailed qualitative feedback, including candidate strengths, weaknesses, and actionable improvement tips.

---

## 🛠️ Technology Stack

* **Language:** Python
* **Frontend & Framework:** Streamlit
* **Machine Learning / NLP:** Scikit-Learn, PyPDF2
* **Generative AI:** Google Gemini API (`google-generativeai`)

---

## ⚙️ How to Run Locally

Follow these simple steps to run the application on your local machine:

  **1. Clone the repository:**
  ```bash
  git clone https://github.com/rubina23/ai-resume-screener
  cd ai-resume-screener

```
  **2. Install the required dependencies:**
```
  pip install -r requirements.txt

```
  **3. Run the Streamlit app:**
```
  streamlit run app.py

```
## **Use Case:**

- **For Job Seekers:** Optimize your resume before applying to ensure it passes through corporate ATS filters.
- **For Recruiters:** Quickly screen and rank hundreds of resumes against a specific job role.
