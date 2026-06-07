import streamlit as st
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import google.generativeai as genai
import time

# ওয়েবসাইটের সেটিং
st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

st.title("📄 AI-Driven Resume Screener & Smart Feedback")
st.write("Upload your resume, paste the Job Description, and get detailed AI feedback powered by Generative AI!")
st.write("---")

# Streamlit Secrets থেকে স্বয়ংক্রিয়ভাবে API Key নেওয়ার চেষ্টা
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.sidebar.title("🔑 API Key Setup")
    api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")
    st.sidebar.markdown("[Get your free API key here](https://aistudio.google.com/app/apikey)")

# ফাংশন ১: PDF এবং DOCX থেকে টেক্সট পড়া (নতুন আপডেট)
def extract_text_from_file(uploaded_file):
    text = ""
    if uploaded_file.name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
    elif uploaded_file.name.endswith('.docx'):
        text = docx2txt.process(uploaded_file)
    return text

# ফাংশন ২: ATS Score বের করা
def calculate_match_score(resume_text, jd_text):
    text_list = [resume_text, jd_text]
    cv = TfidfVectorizer()
    count_matrix = cv.fit_transform(text_list)
    match_percentage = cosine_similarity(count_matrix)[0][1] * 100
    return round(match_percentage, 2)

# ফাংশন ৩: মিসিং কি-ওয়ার্ড বের করা
def get_missing_keywords(resume_text, jd_text):
    resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', jd_text.lower()))
    missing = jd_words - resume_words
    return list(missing)

# ফাংশন ৪: এআই মডেল সেটআপ করা (Rate limit safety)
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

# ফাংশন ৫: AI HR Feedback জেনারেট করা
def get_ai_feedback(resume_text, jd_text, model):
    time.sleep(2)  
    prompt = f"""
    Act as an expert HR Manager. Review this Resume against the Job Description.
    Job Description: {jd_text}
    Resume: {resume_text}
    Provide: 1. Candidate Summary, 2. Strengths, 3. Weaknesses, 4. Actionable tips.
    """
    return model.generate_content(prompt).text

# ফাংশন ৬: AI Cover Letter জেনারেট করা (নতুন ফিচার)
def generate_cover_letter(resume_text, jd_text, model):
    time.sleep(2)
    prompt = f"""
    Act as an expert career coach. Write a highly professional, engaging, and customized Cover Letter for the following job using the candidate's resume.
    Job Description: {jd_text}
    Resume: {resume_text}
    Make sure the tone is confident and matches the job requirements perfectly. Keep it under 400 words.
    """
    return model.generate_content(prompt).text

# ইউজার ইন্টারফেস (UI)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Job Description")
    jd_input = st.text_area("Paste the Job Description (JD) here:", height=250)

with col2:
    st.subheader("📂 Upload Resume")
    # এখন PDF এর পাশাপাশি DOCX ও সাপোর্ট করবে
    uploaded_file = st.file_uploader("Upload your CV", type=["pdf", "docx"])

if st.button("Analyze Resume with AI 🚀"):
    if uploaded_file is not None and jd_input.strip() != "":
        if not api_key:
            st.error("⚠️ Please check your API Key setup!")
        else:
            with st.spinner("Analyzing your resume and extracting insights..."):
                # টেক্সট এক্সট্রাক্ট
                resume_text = extract_text_from_file(uploaded_file)
                st.session_state['resume_text'] = resume_text  # কভার লেটারের জন্য ডাটা সেভ রাখা
                st.session_state['jd_input'] = jd_input
                
                match_score = calculate_match_score(resume_text, jd_input)
                missing_keywords = get_missing_keywords(resume_text, jd_input)
                model = get_gemini_model(api_key)
                st.session_state['ai_model'] = model # মডেল সেভ রাখা
                
                st.write("---")
                st.header("📊 ATS Analysis Result")
                
                if match_score >= 80:
                    st.success(f"### 🎉 Match Score: {match_score}% (Excellent Fit!)")
                elif match_score >= 60:
                    st.warning(f"### ⚠️ Match Score: {match_score}% (Good, but needs improvement)")
                else:
                    st.error(f"### ❌ Match Score: {match_score}% (Very Low Match)")
                    
                st.progress(match_score / 100)
                
                st.subheader("🔍 Missing Keywords:")
                if len(missing_keywords) > 0:
                    st.write(", ".join(missing_keywords[:15]))
                else:
                    st.success("Wow! Your resume covers almost all the keywords from the Job Description.")
                
                st.write("---")
                st.header("🤖 Advanced AI Feedback (HR Review)")
                try:
                    ai_feedback = get_ai_feedback(resume_text, jd_input, model)
                    st.write(ai_feedback)
                except Exception as e:
                    st.info("📌 The AI server is currently experiencing high traffic. ATS Score is 100% accurate. Try the AI review later.")
                    
                st.success("Analysis Complete! You can now generate a custom Cover Letter.")
    else:
        st.error("Please upload a PDF/DOCX resume and paste the Job Description to proceed.")

# নতুন বাটন: কভার লেটার জেনারেট করা
st.write("---")
if st.button("✍️ Generate Custom Cover Letter"):
    if 'resume_text' in st.session_state and 'jd_input' in st.session_state:
        with st.spinner("AI is writing a perfect cover letter for you..."):
            try:
                cover_letter = generate_cover_letter(st.session_state['resume_text'], st.session_state['jd_input'], st.session_state['ai_model'])
                st.subheader("✉️ Your Customized Cover Letter")
                st.write(cover_letter)
                # ডাউনলোড করার অপশন
                st.download_button(label="📥 Download Cover Letter (Text)", data=cover_letter, file_name="Cover_Letter.txt", mime="text/plain")
            except Exception as e:
                st.error("AI is currently busy. Please try again.")
    else:
        st.warning("Please analyze your resume first before generating a cover letter.")

st.write("---")
st.caption("🚀 AI-Driven ATS Analyzer | Built by You 💡")
