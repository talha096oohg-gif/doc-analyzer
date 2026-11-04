import streamlit as st
from groq import Groq
import PyPDF2

st.set_page_config(page_title="Resume vs JD Analyzer", page_icon="📄", layout="centered")
st.title("📄 Resume vs JD Analyzer")
st.caption("Upload your resume and paste job description to get instant AI analysis!")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
resume_text = ""
if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        resume_text += page.extract_text() or ""

resume_input = st.text_area("Resume Text:", value=resume_text, height=150, placeholder="Your resume text will appear here...")
jd_input = st.text_area("Job Description:", height=250, placeholder="Paste the full job description here...")

if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
    if not resume_input or not jd_input:
        st.warning("⚠️ Please provide both Resume and Job Description")
    else:
        with st.spinner("🤖 AI is analyzing your resume..."):
            prompt = f"""
            You are an expert ATS resume analyzer.
            RESUME: {resume_input}
            JOB DESCRIPTION: {jd_input}
            
            Provide analysis in this format:
            1. MATCH SCORE: /100%
            2. ✅ MATCHED SKILLS
            3. ❌ MISSING SKILLS
            4. 💡 5 IMPROVEMENTS
            5. FINAL VERDICT
            """
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content
            st.success("✅ Analysis Complete!")
            st.markdown(result)
            st.download_button("📥 Download Report", result, file_name="analysis.txt", use_container_width=True)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Groq AI")
