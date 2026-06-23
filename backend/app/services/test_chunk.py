from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_chunks

pdf_path = "uploads/project_1/Payment Service BRD.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = create_chunks(text)

print(f"Total Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print("-" * 50)
    print(chunk)