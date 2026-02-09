import streamlit as st
import google.generativeai as genai
# Add this import at the very top of your file
from io import StringIO

# ... (keep your get_ai_analysis function the same) ...

def main():
    st.set_page_config(page_title="AI Career Pro", layout="wide")
    st.title("🚀 AI Career Coach: Score & Cover Letter")

    if "analysis_report" not in st.session_state:
        st.session_state.analysis_report = ""

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Your Resume")
        # NEW FEATURE: File Uploader
        uploaded_resume = st.file_uploader("Upload your resume (TXT or PDF)", type=["txt", "pdf"])
        
        resume_content = ""
        if uploaded_resume is not None:
            # Logic to read the uploaded file
            if uploaded_resume.type == "text/plain":
                resume_content = StringIO(uploaded_resume.getvalue().decode("utf-8")).read()
                st.success("Resume loaded successfully!")
            else:
                st.error("For PDF support, please ensure you have installed 'PyPDF2' or use a .txt file.")
        
        # Keep the text area as a backup or for quick edits
        resume_input = st.text_area("Or paste resume text here:", value=resume_content, height=200)

    with col2:
        st.subheader("📋 Job Description")
        job_input = st.text_area("Paste Job Requirements", height=300)

    # Use whichever input has content (uploaded file or pasted text)
    final_resume = resume_input if resume_input else resume_content

    if st.button("Generate Score & Cover Letter"):
        if final_resume and job_input:
            with st.spinner("AI is analyzing your profile..."):
                st.session_state.analysis_report = get_ai_analysis(final_resume, job_input)
        else:
            st.error("Please provide both your resume and the job description!")

    if st.session_state.analysis_report:
        st.divider()
        st.markdown(st.session_state.analysis_report)
        st.download_button("📥 Download Report", st.session_state.analysis_report, "Career_Report.txt")

if __name__ == "__main__":
    main()