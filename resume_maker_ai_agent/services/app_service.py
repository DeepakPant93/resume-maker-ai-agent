import pypdf
from streamlit.runtime.uploaded_file_manager import UploadedFile

# from docx import Document
from resume_maker_ai_agent.crew import ResumeMakerAIAgent


def read_pdf(uploaded_file: UploadedFile) -> str:
    text = ""
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return text


def run(pdf_file_path: UploadedFile, job_description: str) -> str:
    """
    Processes a PDF resume file, customizes it based on the job description,
    and returns the updated resume text.

    :param pdf_file_path: Path to the PDF file containing the resume.
    :param job_description: Description of the job for which the resume needs to be customized.
    :return: A string representing the updated resume content.
    """

    print("Extracting text from PDF")
    resume_text = read_pdf(pdf_file_path)

    # Run the crew
    print("Running the crew")
    inputs = {"resume_text": resume_text, "job_description": job_description}
    result = ResumeMakerAIAgent().crew().kickoff(inputs=inputs)
    print("Done")

    print(result.raw)

    return str(result.raw)


# def create_docx(content) -> bytes | None:
#     """Create a Word document with the content."""
#     # doc = Document()
#     # doc.add_paragraph(content)

#     # # Save to bytes buffer
#     # buffer = io.BytesIO()
#     # doc.save(buffer)
#     # buffer.seek(0)
#     # return buffer
#     return None
