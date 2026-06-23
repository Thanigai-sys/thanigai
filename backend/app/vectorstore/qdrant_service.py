from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams

client = QdrantClient(":memory:")


def create_collection():

    client.recreate_collection(
        collection_name="brd_chunks",

        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE
        )
    )

    print("Collection Created")