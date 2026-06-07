import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import google.generativeai as genai

# ওয়েবসাইটের সেটিং
st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

st.title("📄 AI Resume Screener & Smart Feedback System")
st.write("Upload your resume, paste the Job Description, and get detailed AI feedback powered by Gemini!")
st.write("---")

# সাইডবারে API Key নেওয়ার অপশন
#st.sidebar.title("🔑 API Key Setup")
#api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")
#st.sidebar.markdown("[Get your free API key here](https://aistudio.google.com/app/apikey)")

# Streamlit Secrets থেকে স্বয়ংক্রিয়ভাবে API Key নেওয়া
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.sidebar.title("🔑 API Key Setup")
    api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")
    st.sidebar.markdown("[Get your free API key here](https://aistudio.google.com/app/apikey)")

# ফাংশন: পিডিএফ থেকে টেক্সট পড়া
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text

# ফাংশন: ATS Score বের করা
def calculate_match_score(resume_text, jd_text):
    text_list = [resume_text, jd_text]
    cv = TfidfVectorizer()
    count_matrix = cv.fit_transform(text_list)
    match_percentage = cosine_similarity(count_matrix)[0][1] * 100
    return round(match_percentage, 2)

# ফাংশন: মিসিং কি-ওয়ার্ড বের করা
def get_missing_keywords(resume_text, jd_text):
    resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', jd_text.lower()))
    missing = jd_words - resume_words
    return list(missing)

# ফাংশন: Gemini AI দিয়ে ডিটেইলস ফিডব্যাক জেনারেট করা
def get_ai_feedback(resume_text, jd_text, api_key):
    genai.configure(api_key=api_key)
    # ফাংশন: Gemini AI দিয়ে ডিটেইলস ফিডব্যাক জেনারেট করা
def get_ai_feedback(resume_text, jd_text, api_key):
    genai.configure(api_key=api_key)
    
    # স্বয়ংক্রিয়ভাবে অ্যাকটিভ মডেল খুঁজে বের করা
    valid_model = None
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name.lower():
            # 'models/' অংশটুকু বাদ দিয়ে শুধু নাম নেওয়া
            valid_model = m.name.replace('models/', '') 
            break
            
    if not valid_model:
        return "Error: No supported Gemini model found for your API key."
        
    # খুঁজে পাওয়া মডেলটি ব্যবহার করা
    model = genai.GenerativeModel(valid_model)
    prompt = f"""
    Act as an expert HR Manager and ATS specialist. Review the following Resume against the Job Description.
    Job Description: {jd_text}
    Resume: {resume_text}
    
    Please provide:
    1. Candidate Profile Summary (2-3 lines).
    2. Strengths (What matches well with the JD).
    3. Weaknesses (What is missing or needs improvement).
    4. Actionable tips to improve the resume for this specific job role.
    """
    response = model.generate_content(prompt)
    return response.text
    response = model.generate_content(prompt)
    return response.text

# ইউজার ইন্টারফেস (UI)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Job Description")
    jd_input = st.text_area("Paste the Job Description (JD) here:", height=250)

with col2:
    st.subheader("📂 Upload Resume")
    uploaded_file = st.file_uploader("Upload your CV (PDF format only)", type=["pdf"])

if st.button("Analyze Resume with AI 🚀"):
    if uploaded_file is not None and jd_input.strip() != "":
        if api_key == "":
            st.error("⚠️ Please enter your Gemini API Key in the sidebar first!")
        else:
            with st.spinner("Analyzing your resume and generating AI feedback..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                match_score = calculate_match_score(resume_text, jd_input)
                missing_keywords = get_missing_keywords(resume_text, jd_input)
                
                st.write("---")
                st.header("📊 ATS Analysis Result")
                
                # স্কোর দেখানো
                if match_score >= 80:
                    st.success(f"### 🎉 Match Score: {match_score}% (Excellent Fit!)")
                elif match_score >= 60:
                    st.warning(f"### ⚠️ Match Score: {match_score}% (Good, but needs improvement)")
                else:
                    st.error(f"### ❌ Match Score: {match_score}% (Very Low Match)")
                    
                st.progress(match_score / 100)
                
                # মিসিং কি-ওয়ার্ড
                st.subheader("🔍 Missing Keywords:")
                if len(missing_keywords) > 0:
                    st.write(", ".join(missing_keywords[:15]))
                else:
                    st.success("Your resume covers almost all the keywords from the Job Description.")
                
                st.write("---")
                
                # জেমিনাই এআই এর ফিডব্যাক
                st.header("🤖 Advanced AI Feedback (HR Review)")
                try:
                    ai_feedback = get_ai_feedback(resume_text, jd_input, api_key)
                    st.write(ai_feedback)
                except Exception as e:
                    st.error(f"Error generating AI feedback. Please check your API key. ({e})")
    else:
        st.error("Please upload a PDF resume and paste the Job Description to proceed.")

st.write("---")
#st.caption("🚀 AI-Powered ATS Analyzer | Built by You 💡")
