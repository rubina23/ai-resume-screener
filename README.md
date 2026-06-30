# 📄 AI-Driven Resume Screener & ATS System

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-F9AB00.svg)

An enterprise-grade Applicant Tracking System (ATS) and Career Assistant built with Python, Streamlit, and Google Gemini AI. This application not only scores resumes against Job Descriptions but also features an interactive RAG-based chatbot, batch ranking for HRs, and automated web scraping.

🔗 **Live:** https://ai-resume-screener-ats.streamlit.app/

## 🚀 Features
* **Smart CV Analysis:** Calculates ATS match scores using TF-IDF & Cosine Similarity.
* **Anti-Bot Web Scraping:** Automatically fetches Job Descriptions from URLs, bypassing basic security protocols.
* **Keyword Gap Analysis:** Automatically identifies critical keywords and skills present in the Job Description but missing from your resume, providing actionable insights for optimization.
* **Advanced AI HR Review:** Integrates Google Gemini AI (`gemini-1.5-flash`) to generate detailed qualitative feedback, including candidate strengths, weaknesses, and actionable improvement tips.
* **Batch CV Ranking (HR Mode):** Upload multiple resumes (PDF/DOCX) and instantly generate a ranked leaderboard based on job fit.
* **Interactive AI Chat (RAG):** Chat directly with your resume! Ask the AI how to improve specific sections for the targeted role.
* **Cover Letter Generator:** Instantly drafts highly customized, professional cover letters.

---

## 🛠️ Technology Stack

* **Language:** Python
* **Frontend & Framework:** Streamlit
* **Data Processing:** Pandas, PyPDF2, docx2txt
* **Generative AI:** Google Gemini API (`gemini-1.5-flash`)
* **NLP & Scraping:** Scikit-Learn, BeautifulSoup4, Requests
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
