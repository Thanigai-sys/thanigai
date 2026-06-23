from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-base-en-v1.5"
)


def generate_embeddings(chunks):

    embeddings = model.encode(
        chunks
    )

    return embeddings