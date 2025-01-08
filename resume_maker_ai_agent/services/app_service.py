import warnings
import PyPDF2
# from docx import Document
import io

from resume_maker_ai_agent.crew import ResumeMakerAIAgent
from streamlit.runtime.uploaded_file_manager import UploadedFile


def _extract_text_from_pdf(pdf_file_path):
    """Extract text content from uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
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
    resume_text = _extract_text_from_pdf(pdf_file_path)

    # Run the crew
    print("Running the crew")
    inputs = {"resume_text": resume_text, "job_description": job_description}
    result = ResumeMakerAIAgent().crew().kickoff(inputs=inputs)

    return result.raw


def create_docx(content):
    """Create a Word document with the content."""
    # doc = Document()
    # doc.add_paragraph(content)

    # # Save to bytes buffer
    # buffer = io.BytesIO()
    # doc.save(buffer)
    # buffer.seek(0)
    # return buffer
    return none