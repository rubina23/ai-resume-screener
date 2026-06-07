import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Settings
st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

st.title("📄 AI Resume Screener (ATS System)")
st.write("Upload your resume and the Job Description to see your ATS Match Score!")
st.write("---")

# 1. Read text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text

# 2. Find ATS Score (TF-IDF & Cosine Similarity)
def calculate_match_score(resume_text, jd_text):
    text_list = [resume_text, jd_text]
    cv = TfidfVectorizer()
    count_matrix = cv.fit_transform(text_list)
    match_percentage = cosine_similarity(count_matrix)[0][1] * 100
    return round(match_percentage, 2)

# 3. Find missing keyword 
def get_missing_keywords(resume_text, jd_text):
    # tokenize words 
    resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', jd_text.lower()))
    
    # find word missing on the cv 
    missing = jd_words - resume_words
    return list(missing)

# user Input (UI)
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
            # Extract text
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # Calculate score স্
            match_score = calculate_match_score(resume_text, jd_input)
            
            # find missing words
            missing_keywords = get_missing_keywords(resume_text, jd_input)
            
            # result
            st.write("---")
            st.header("📊 ATS Analysis Result")
            
            #  message & color 
            if match_score >= 80:
                st.success(f"### 🎉 Match Score: {match_score}% (Excellent Fit!)")
            elif match_score >= 60:
                st.warning(f"### ⚠️ Match Score: {match_score}% (Good, but needs improvement)")
            else:
                st.error(f"### ❌ Match Score: {match_score}% (Very Low Match)")
                
            st.progress(match_score / 100)
            
            # show missing keyword 
            st.subheader("🔍 Keywords to Add in Your CV:")
            if len(missing_keywords) > 0:
                # shown first 20 important missing word 
                st.write(", ".join(missing_keywords[:20]))
                st.info("💡 Pro Tip: Add some of these keywords to your resume to increase your ATS score!")
            else:
                st.success("Wow! Your resume covers almost all the keywords from the Job Description.")
    else:
        st.error("Please upload a PDF resume and paste the Job Description to proceed.")

st.write("---")
st.caption("Developed by Rubina Begum | Powered by Streamlit & NLP")
