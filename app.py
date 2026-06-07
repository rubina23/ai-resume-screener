# %%writefile app.py
import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# ওয়েবসাইটের সেটিং
st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

st.title("📄 AI Resume Screener (ATS System)")
st.write("Upload your resume and the Job Description to see your ATS Match Score!")
st.write("---")

# ১. পিডিএফ থেকে টেক্সট পড়ার ফাংশন
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text

# ২. ATS Score বের করার ফাংশন (TF-IDF & Cosine Similarity)
def calculate_match_score(resume_text, jd_text):
    text_list = [resume_text, jd_text]
    cv = TfidfVectorizer()
    count_matrix = cv.fit_transform(text_list)
    match_percentage = cosine_similarity(count_matrix)[0][1] * 100
    return round(match_percentage, 2)

# ৩. মিসিং কি-ওয়ার্ড বের করার ফাংশন
def get_missing_keywords(resume_text, jd_text):
    # টেক্সট থেকে শুধু শব্দগুলো (৩ অক্ষরের বড়) আলাদা করা
    resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', jd_text.lower()))
    
    # জব ডেসক্রিপশনে আছে কিন্তু সিভিতে নেই এমন শব্দগুলো বের করা
    missing = jd_words - resume_words
    return list(missing)

# ইউজার ইন্টারফেস (UI)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Job Description")
    jd_input = st.text_area("Paste the Job Description (JD) here:", height=300)

with col2:
    st.subheader("📂 Upload Resume")
    uploaded_file = st.file_uploader("Upload your CV (PDF format only)", type=["pdf"])

if st.button("Analyze Resume 🚀"):
    if uploaded_file is not None and jd_input.strip() != "":
        with st.spinner("Analyzing your resume..."):
            # টেক্সট এক্সট্রাক্ট করা
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # স্কোর ক্যালকুলেট করা
            match_score = calculate_match_score(resume_text, jd_input)
            
            # মিসিং কি-ওয়ার্ড বের করা
            missing_keywords = get_missing_keywords(resume_text, jd_input)
            
            # রেজাল্ট দেখানো
            st.write("---")
            st.header("📊 ATS Analysis Result")
            
            # স্কোরের ওপর ভিত্তি করে কালার এবং মেসেজ
            if match_score >= 80:
                st.success(f"### 🎉 Match Score: {match_score}% (Excellent Fit!)")
            elif match_score >= 60:
                st.warning(f"### ⚠️ Match Score: {match_score}% (Good, but needs improvement)")
            else:
                st.error(f"### ❌ Match Score: {match_score}% (Very Low Match)")
                
            st.progress(match_score / 100)
            
            # মিসিং কি-ওয়ার্ড দেখানো
            st.subheader("🔍 Keywords to Add in Your CV:")
            if len(missing_keywords) > 0:
                # প্রথম ২০টি গুরুত্বপূর্ণ মিসিং শব্দ দেখাবো
                st.write(", ".join(missing_keywords[:20]))
                st.info("💡 Pro Tip: Add some of these keywords to your resume to increase your ATS score!")
            else:
                st.success("Wow! Your resume covers almost all the keywords from the Job Description.")
    else:
        st.error("Please upload a PDF resume and paste the Job Description to proceed.")

st.write("---")
st.caption("🚀 Built with ❤️ using Streamlit, PyPDF2 & Scikit-Learn | AI Resume Screener")
