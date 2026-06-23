from app.services.embedding_service import model

from app.vectorstore.qdrant_service import (
    create_collection,
    store_embeddings,
    search_chunks
)

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_chunks
from app.services.embedding_service import generate_embeddings


pdf_path = "uploads/project_1/Payment Service BRD.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = create_chunks(text)

embeddings = generate_embeddings(chunks)

create_collection()

store_embeddings(
    chunks,
    embeddings
)

query = "What are payment processing requirements?"

query_embedding = model.encode(query)

results = search_chunks(query_embedding)

for result in results:

    print("\nScore:", result.score)

    print(result.payload["text"])