import streamlit as st
from groq import Groq
import PyPDF2

st.set_page_config(page_title="Resume Analyzer", layout="centered")
st.title("📄 Resume vs JD Analyzer")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
resume_text = ""
if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        resume_text += page.extract_text() or ""

resume_input = st.text_area("Resume Text:", value=resume_text, height=150)
jd_input = st.text_area("Job Description:", height=250)

if st.button("🔍 Analyze Resume", type="primary"):
    if not resume_input or not jd_input:
        st.warning("Please provide both Resume and JD")
    else:
        with st.spinner("AI Analyzing..."):
            prompt = f"Resume: {resume_input}\nJD: {jd_input}\nGive: Match Score %, Matched Skills, Missing Skills, 5 Improvements, Final Verdict."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
            st.success("Done!")
            st.markdown(res.choices[0].message.content)
            st.download_button("Download Analysis", res.choices[0].message.content, "analysis.txt")
