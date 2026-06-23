from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_chunks
from app.services.embedding_service import generate_embeddings

pdf_path = "uploads/project_1/Payment Service BRD.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = create_chunks(text)

embeddings = generate_embeddings(chunks)

print(f"Total Chunks: {len(chunks)}")

print(f"Total Embeddings: {len(embeddings)}")

print("\nFirst Vector Sample:")

print(embeddings[0][:10])




