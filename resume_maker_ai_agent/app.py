# import PyPDF2

# from docx import Document
# from docx.shared import Inches
import streamlit as st

# import tempfile
from resume_maker_ai_agent.services.app_service import run


def main() -> None:
    st.set_page_config(page_title="Resume Maker AI", page_icon="📄")

    st.title("Resume Maker AI")
    st.write("Customize your resume for specific job descriptions using AI")

    # File upload
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

    # Job description input
    job_description = st.text_area("Enter the job description:", height=200)

    if st.button("Customize Resume") and uploaded_file is not None and job_description:
        with st.spinner("Customizing your resume..."):
            try:
                # Customize resume
                customized_resume = run(uploaded_file, job_description)

                # Display customized resume
                st.subheader("Customized Resume")
                st.write(customized_resume)

                # Create download button
                # doc_buffer = create_docx(customized_resume)
                # st.download_button(
                #     label="Download Customized Resume",
                #     data=doc_buffer,
                #     file_name="customized_resume.docx",
                #     mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                # )

            except Exception as e:
                st.error(f"An error occurred: {e!s}")

    # Add instructions and tips
    with st.expander("How to use"):
        st.write("""
        1. Upload your current resume in PDF format
        2. Paste the job description you're targeting
        3. Click 'Customize Resume' to generate a tailored version
        4. Review the customized resume
        5. Download the result as a Word document
        """)

    # Footer
    st.markdown("---")
    st.markdown("Built with Streamlit and Crew AI")


if __name__ == "__main__":
    main()
