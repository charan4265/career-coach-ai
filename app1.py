import streamlit as st
import google.generativeai as genai
from io import StringIO
import PyPDF2 # New import for PDF support

# ... (Keep your API setup and get_ai_analysis function the same) ...

def main():
    st.set_page_config(page_title="AI Career Pro", layout="wide")
    st.title("🚀 AI Career Coach: Score & Cover Letter")

    if "analysis_report" not in st.session_state:
        st.session_state.analysis_report = ""

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Your Resume")
        uploaded_resume = st.file_uploader("Upload your resume (TXT or PDF)", type=["txt", "pdf"])
        
        resume_content = ""
        if uploaded_resume is not None:
            if uploaded_resume.type == "text/plain":
                # Handle TXT files
                resume_content = StringIO(uploaded_resume.getvalue().decode("utf-8")).read()
            elif uploaded_resume.type == "application/pdf":
                # Handle PDF files
                pdf_reader = PyPDF2.PdfReader(uploaded_resume)
                for page in pdf_reader.pages:
                    resume_content += page.extract_text()
            st.success("Resume loaded successfully!")
        
        # This box will automatically show the text from your PDF
        resume_input = st.text_area("Review extracted text:", value=resume_content, height=200)

    with col2:
        st.subheader("📋 Job Description")
        job_input = st.text_area("Paste Job Requirements", height=300)

    # Use the final content for the AI
    if st.button("Generate Score & Cover Letter"):
        if (resume_input or resume_content) and job_input:
            with st.spinner("AI is analyzing your profile..."):
                final_text = resume_input if resume_input else resume_content
                st.session_state.analysis_report = get_ai_analysis(final_text, job_input)
        else:
            st.error("Please provide both your resume and the job description!")

    # Display results
    if st.session_state.analysis_report:
        st.divider()
        st.markdown(st.session_state.analysis_report)
        st.download_button("📥 Download Report", st.session_state.analysis_report, "Career_Report.txt")

if __name__ == "__main__":
    main()