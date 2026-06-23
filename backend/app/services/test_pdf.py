from app.services.pdf_service import extract_text_from_pdf

pdf_path = "uploads/project_1/Payment Service BRD.pdf"

text = extract_text_from_pdf(pdf_path)

print(text)