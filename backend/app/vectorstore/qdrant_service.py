from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams
from qdrant_client.models import PointStruct

client = QdrantClient(":memory:")


def create_collection():

    collections = client.get_collections().collections

    existing = [c.name for c in collections]

    if "brd_chunks" not in existing:

        client.create_collection(
            collection_name="brd_chunks",
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )

        print("Collection Created")


def store_embeddings(chunks, embeddings):

    points = []

    for idx, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):

        points.append(
            PointStruct(
                id=idx,
                vector=embedding.tolist(),
                payload={
                    "text": chunk
                }
            )
        )

    client.upsert(
        collection_name="brd_chunks",
        points=points
    )

    print(f"{len(points)} vectors stored")

def search_chunks(query_embedding):

    results = client.query_points(
        collection_name="brd_chunks",
        query=query_embedding.tolist(),
        limit=3
    )

    return results.points