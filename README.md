# 📄 AI Resume Screener (ATS System)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-F9AB00.svg)

An AI-powered Applicant Tracking System (ATS) built with **Streamlit**, **Scikit-Learn**, and **Python**. This smart web application helps job seekers and recruiters evaluate how well a resume matches a specific Job Description (JD) using Natural Language Processing (NLP).

🔗 **Live Demo:** https://ai-resume-screener-ats.streamlit.app/

---

## 🚀 Key Features

* **PDF Resume Parsing:** Seamlessly upload your CV/Resume in PDF format. The app instantly extracts and processes the text.
* **Smart ATS Matching:** Uses NLP techniques (TF-IDF Vectorization & Cosine Similarity) to mathematically compare the resume against the targeted Job Description.
* **ATS Match Score:** Instantly calculates a percentage score indicating how well your resume fits the job role.
* **Skill Gap Analysis:** Automatically identifies critical keywords and skills present in the Job Description but missing from your resume, providing actionable insights for optimization.

---

## 🛠️ Technology Stack

* **Frontend & Framework:** Streamlit
* **Text Extraction:** PyPDF2
* **Machine Learning & NLP:** Scikit-Learn (TF-IDF, Cosine Similarity)
* **Language:** Python

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
