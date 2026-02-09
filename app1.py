import streamlit as st
import google.generativeai as genai

# 1. API Security
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# 2. Advanced AI Logic
def get_ai_analysis(resume_text, job_desc):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Combined Prompt for Scoring and Cover Letter
    prompt = f"""
    Act as a Senior HR Manager. Analyze this Resume against the Job Description.
    
    1. **Resume Score**: Give a match score out of 100 based on skills and experience.
    2. **Key Gaps**: Identify 3-5 missing keywords or skills.
    3. **Cover Letter**: Write a high-converting, professional 3-paragraph cover letter 
       that bridges the gap between the candidate's skills and the job requirements.
    
    Resume: {resume_text}
    Job Description: {job_desc}
    """
    response = model.generate_content(prompt)
    return response.text

def main():
    st.set_page_config(page_title="AI Career Pro", layout="wide")
    st.title("🚀 AI Career Coach: Score & Cover Letter")

    # Initialize Session State to keep results visible
    if "analysis_report" not in st.session_state:
        st.session_state.analysis_report = ""

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📄 Your Resume")
        resume_input = st.text_area("Paste Resume Content", height=300)
    with col2:
        st.subheader("📋 Job Description")
        job_input = st.text_area("Paste Job Requirements", height=300)

    # 3. Execution Button
    if st.button("Generate Score & Cover Letter"):
        if resume_input and job_input:
            with st.spinner("AI is analyzing your profile..."):
                # Save result to session state
                st.session_state.analysis_report = get_ai_analysis(resume_input, job_input)
        else:
            st.error("Please fill both boxes!")

    # 4. Display Results
    if st.session_state.analysis_report:
        st.divider()
        st.markdown(st.session_state.analysis_report)
        
        # 5. Professional Download Feature
        st.download_button(
            label="📥 Download Full Report & Cover Letter",
            data=st.session_state.analysis_report,
            file_name="Career_Coach_Report.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()