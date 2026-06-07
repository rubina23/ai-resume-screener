import streamlit as st
import PyPDF2
import docx2txt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import google.generativeai as genai
import time
import requests
from bs4 import BeautifulSoup

# ওয়েবসাইটের সেটিং
st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

st.title("📄 AI-Driven Resume Screener & ATS System")
st.write("Instantly analyze resumes, generate tailored cover letters, and rank top candidates with AI-driven precision!")
st.write("---")

# Streamlit Secrets থেকে API Key নেওয়া
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.sidebar.title("🔑 API Key Setup")
    api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")

# --- ফাংশনগুলো ---
def extract_text_from_file(uploaded_file):
    text = ""
    if uploaded_file.name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
    elif uploaded_file.name.endswith('.docx'):
        text = docx2txt.process(uploaded_file)
    return text

def calculate_match_score(resume_text, jd_text):
    text_list = [resume_text, jd_text]
    cv = TfidfVectorizer()
    count_matrix = cv.fit_transform(text_list)
    match_percentage = cosine_similarity(count_matrix)[0][1] * 100
    return round(match_percentage, 2)

def get_missing_keywords(resume_text, jd_text):
    resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', jd_text.lower()))
    missing = jd_words - resume_words
    return list(missing)

def get_gemini_model(api_key):
    genai.configure(api_key=api_key)
    valid_model = None
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods and '1.5-flash' in m.name.lower():
            valid_model = m.name.replace('models/', '') 
            break
    if not valid_model:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name.lower():
                valid_model = m.name.replace('models/', '') 
                break
    return genai.GenerativeModel(valid_model)

def get_ai_feedback(resume_text, jd_text, model):
    time.sleep(2)  
    prompt = f"""Act as an expert HR Manager. Review this Resume against the Job Description.
    JD: {jd_text}\nResume: {resume_text}
    Provide: 1. Candidate Summary, 2. Strengths, 3. Weaknesses, 4. Actionable tips."""
    return model.generate_content(prompt).text

def generate_cover_letter(resume_text, jd_text, model):
    time.sleep(2)
    prompt = f"""Act as an expert career coach. Write a customized Cover Letter.
    JD: {jd_text}\nResume: {resume_text}\nKeep it under 400 words."""
    return model.generate_content(prompt).text

# নতুন ফাংশন: Job URL Scraping
def scrape_job_description(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'} 
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # অপ্রয়োজনীয় স্ক্রিপ্ট ও স্টাইল বাদ দেওয়া
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        return ""

# --- ইউজার ইন্টারফেস (UI) - Tab System ---
tab1, tab2, tab3 = st.tabs(["👤 Single CV Analyzer", "🏆 Batch CV Ranking", "💬 Interactive AI Chat"])

# ----------------- TAB 1: Single CV Analysis -----------------
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📝 Job Description")
        jd_choice = st.radio("How do you want to provide the JD?", ("Paste Text", "Paste URL Link"))
        
        jd_input = ""
        if jd_choice == "Paste Text":
            jd_input = st.text_area("Paste the Job Description (JD) here:", height=200, key="jd_text_input")
        else:
            job_url = st.text_input("Enter Job URL (e.g., from company website):")
            if st.button("Fetch Job Details"):
                with st.spinner("Scraping job details..."):
                    scraped_text = scrape_job_description(job_url)
                    if scraped_text:
                        st.success("Successfully fetched job details!")
                        jd_input = st.text_area("Review Fetched JD:", value=scraped_text[:2000] + "... (truncated)", height=150, key="jd_scraped_input")
                    else:
                        st.error("Could not read URL. Some sites (like LinkedIn) block bots. Please paste text instead.")
                        
    with col2:
        st.subheader("📂 Upload Resume")
        uploaded_file = st.file_uploader("Upload your CV", type=["pdf", "docx"], key="cv_single")

    if st.button("Analyze Resume with AI 🚀"):
        if uploaded_file and jd_input.strip():
            if not api_key:
                st.error("⚠️ Please check your API Key setup!")
            else:
                with st.spinner("Analyzing your resume and extracting insights..."):
                    resume_text = extract_text_from_file(uploaded_file)
                    st.session_state['resume_text'] = resume_text 
                    st.session_state['jd_input'] = jd_input
                    
                    match_score = calculate_match_score(resume_text, jd_input)
                    missing_keywords = get_missing_keywords(resume_text, jd_input)
                    model = get_gemini_model(api_key)
                    st.session_state['ai_model'] = model
                    
                    st.write("---")
                    st.header("📊 ATS Analysis Result")
                    if match_score >= 80: st.success(f"### 🎉 Match Score: {match_score}% (Excellent Fit!)")
                    elif match_score >= 60: st.warning(f"### ⚠️ Match Score: {match_score}% (Good, needs improvement)")
                    else: st.error(f"### ❌ Match Score: {match_score}% (Very Low Match)")
                    st.progress(match_score / 100)
                    
                    st.subheader("🔍 Missing Keywords:")
                    st.write(", ".join(missing_keywords[:15]) if missing_keywords else "No major missing keywords found!")
                    
                    st.write("---")
                    st.header("🤖 Advanced AI Feedback")
                    try:
                        ai_feedback = get_ai_feedback(resume_text, jd_input, model)
                        st.write(ai_feedback)
                        st.download_button("📥 Download AI Feedback Report", data=ai_feedback, file_name="AI_HR_Review.txt", mime="text/plain")
                    except Exception as e:
                        st.info("📌 The AI server is busy. Your ATS Score above is 100% accurate.")
        else:
            st.error("Please upload a resume and provide the Job Description.")

    st.write("---")
    if st.button("✍️ Generate Custom Cover Letter"):
        if 'resume_text' in st.session_state:
            with st.spinner("AI is writing a perfect cover letter..."):
                try:
                    cover_letter = generate_cover_letter(st.session_state['resume_text'], st.session_state['jd_input'], st.session_state['ai_model'])
                    st.subheader("✉️ Your Customized Cover Letter")
                    st.write(cover_letter)
                    st.download_button(label="📥 Download Cover Letter", data=cover_letter, file_name="Cover_Letter.txt", mime="text/plain")
                except:
                    st.error("AI is busy. Please try again.")
        else:
            st.warning("Please analyze your resume first!")

# ----------------- TAB 2: Batch CV Ranking -----------------
with tab2:
    st.subheader("🏆 Rank Multiple Candidates")
    st.write("Upload multiple resumes to instantly see who matches the Job Description best.")
    jd_batch = st.text_area("Paste the Job Description (JD):", height=150, key="jd_batch")
    batch_files = st.file_uploader("Upload Multiple CVs", type=["pdf", "docx"], accept_multiple_files=True)

    if st.button("Rank Candidates 🏅"):
        if batch_files and jd_batch.strip():
            with st.spinner("Scanning and ranking all resumes..."):
                ranking_data = []
                for file in batch_files:
                    text = extract_text_from_file(file)
                    score = calculate_match_score(text, jd_batch)
                    ranking_data.append({"Candidate File": file.name, "ATS Score (%)": score})
                df = pd.DataFrame(ranking_data).sort_values(by="ATS Score (%)", ascending=False).reset_index(drop=True)
                df.index = df.index + 1
                st.success("Ranking Complete! Here is the top candidates list:")
                st.dataframe(df, use_container_width=True)
        else:
            st.error("Please upload at least one CV and paste the Job Description.")

# ----------------- TAB 3: Interactive Chat (RAG) -----------------
with tab3:
    st.subheader("💬 Chat with AI HR Assistant")
    st.write("Ask any questions about your resume and how it fits the Job Description!")
    
    if 'resume_text' in st.session_state and 'jd_input' in st.session_state:
        # চ্যাট হিস্ট্রি সেটআপ
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello! I have reviewed your CV. What would you like to know?"}]

        # আগের চ্যাটগুলো দেখানো
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # ইউজারের ইনপুট
        if prompt := st.chat_input("E.g., How can I improve my experience section?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    context = f"Resume: {st.session_state['resume_text']}\nJob Description: {st.session_state['jd_input']}\nQuestion: {prompt}\nAnswer as an expert HR coach."
                    try:
                        response = st.session_state['ai_model'].generate_content(context)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except:
                        st.error("AI is currently busy. Please wait a moment and try again.")
    else:
        st.warning("⚠️ Please analyze a resume in the 'Single CV Analyzer' tab first so I can read it!")
