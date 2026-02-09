import streamlit as st
import google.generativeai as genai
from io import StringIO
import PyPDF2

# 1. API Security (Make sure "GEMINI_API_KEY" is in your Streamlit Secrets)
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# 2. AI Analysis Function (This was missing in your error screenshot!)
# --- REPLACE THIS ENTIRE SECTION ---
def get_ai_analysis(resume_text, job_desc):
    try:
        # We change '1.5-flash' to '2.5-flash' here
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Act as a Senior HR Manager. Analyze this Resume against the Job Description.
        1. **Match Score**: Give a score out of 100.
        2. **Key Gaps**: Identify missing keywords.
        3. **Cover Letter**: Write a 3-paragraph professional letter.

        Resume: {resume_text}
        Job Description: {job_desc}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # This will show you the exact error on the website if it fails
        return f"AI Error: {str(e)}"
# ----------------------------------

# 3. Main Application Logic
def main():
    st.set_page_config(page_title="AI Career Pro", layout="wide")
    st.title("🚀 AI Career Coach: Score & Cover Letter")
    def main():
    st.set_page_config(page_title="AI Career Pro", layout="wide")
    st.title("🚀 AI Career Coach: Score & Cover Letter")

    # --- ADD THIS SIDEBAR SECTION HERE ---
    with st.sidebar:
        st.header("💡 Quick Resume Tips")
        st.info("""
        - **Use Action Verbs**: Start bullets with 'Managed', 'Developed', or 'Solved'.
        - **Quantify Results**: Use numbers (e.g., 'Increased efficiency by 20%').
        - **Keywords**: Ensure your resume contains words found in the Job Description.
        """)
        # You can even add a helpful video link for users
        st.markdown("---")
        st.markdown("### 🎥 Watch: How to beat ATS")
        st.video("https://www.youtube.com/watch?v=Tt08KmFfIYQ")
    # -------------------------------------

    # ... keep the rest of your code (Session State, Columns, etc.) exactly the same ...

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