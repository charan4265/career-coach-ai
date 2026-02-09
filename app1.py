import streamlit as st
import google.generativeai as genai
from io import StringIO
import PyPDF2

# 1. API Security (Make sure "GEMINI_API_KEY" is in your Streamlit Secrets)
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# 2. AI Analysis Function (This was missing in your error screenshot!)
def get_ai_analysis(resume_text, job_desc):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a Senior HR Manager. Analyze this Resume against the Job Description.
        Provide the following in professional Markdown:
        1. **Match Score**: Give a score out of 100.
        2. **Key Gaps**: Identify 3-5 missing keywords or skills.
        3. **Cover Letter**: Write a professional 3-paragraph cover letter 
           tailored for this specific job.
        
        Resume: {resume_text}
        Job Description: {job_desc}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

# 3. Main Application Logic
def main():
    st.set_page_config(page_title="AI Career Pro", layout="wide")
    st.title("🚀 AI Career Coach: Score & Cover Letter")

    # Keep the report in memory so it doesn't disappear
    if "analysis_report" not in st.session_state:
        st.session_state.analysis_report = ""

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Your Resume")
        uploaded_resume = st.file_uploader("Upload your resume (TXT or PDF)", type=["txt", "pdf"])
        
        resume_content = ""
        if uploaded_resume is not None:
            if uploaded_resume.type == "text/plain":
                resume_content = StringIO(uploaded_resume.getvalue().decode("utf-8")).read()
            elif uploaded_resume.type == "application/pdf":
                pdf_reader = PyPDF2.PdfReader(uploaded_resume)
                for page in pdf_reader.pages:
                    resume_content += page.extract_text()
            st.success("Resume loaded successfully!")
        
        # Display extracted text for verification
        resume_input = st.text_area("Review extracted text:", value=resume_content, height=200)

    with col2:
        st.subheader("📋 Job Description")
        job_input = st.text_area("Paste Job Requirements", height=300)

    # Use the extracted text or the manually pasted text
    final_text = resume_input if resume_input else resume_content

    if st.button("Generate Score & Cover Letter"):
        if final_text.strip() and job_input.strip():
            with st.spinner("AI is analyzing your profile..."):
                # Calling the function defined in Step 2
                report = get_ai_analysis(final_text, job_input)
                st.session_state.analysis_report = report
        else:
            st.error("Please provide both your resume and the job description!")

    # Display results and download button
    if st.session_state.analysis_report:
        st.divider()
        st.markdown(st.session_state.analysis_report)
        st.download_button(
            label="📥 Download Full Report",
            data=st.session_state.analysis_report,
            file_name="Career_Analysis.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()