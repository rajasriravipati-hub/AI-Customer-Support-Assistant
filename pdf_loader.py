import pdfplumber
import logging


def extract_pdf_text(pdf_file):
    """
    Extract text from uploaded PDF
    """

    try:

        text = ""

        with pdfplumber.open(pdf_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    except Exception as e:

        logging.error(f"PDF Extraction Error: {e}")

        return ""