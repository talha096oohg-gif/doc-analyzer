import streamlit as st
from groq import Groq
import PyPDF2

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="centered")
st.title("📄 Resume vs Job Description Analyzer")
st.caption("Upload your resume and paste the job description to get instant AI analysis!")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
resume_text = ""
if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        resume_text += page.extract_text() or ""

resume_input = st.text_area("Resume Text:", value=resume_text, height=150, placeholder="Your resume text will appear here after uploading PDF...")
jd_input = st.text_area("Job Description:", height=250, placeholder="Paste the full job description here...")

if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
    if not resume_input or not jd_input:
        st.warning("Please provide both resume and job description")
    else:
        with st.spinner("Analyzing your resume..."):
            prompt = f"RESUME: {resume_input} JOB DESCRIPTION: {jd_input} Give Match Score, Matched Skills, Missing Skills, 5 Improvements, Final Verdict."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
            st.success("Analysis Complete!")
            st.markdown(res.choices[0].message.content)
            st.download_button("Download Report", res.choices[0].message.content, "analysis.txt", use_container_width=True)
