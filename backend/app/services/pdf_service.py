from pypdf import PdfReader


def extract_text_from_pdf(file_path: str):

    reader = PdfReader(file_path)

    extracted_text = ""

    for page in reader.pages:
        extracted_text += page.extract_text()
        extracted_text += "\n"

    return extracted_text