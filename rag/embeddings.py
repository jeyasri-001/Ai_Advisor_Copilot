from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Qdrant connection
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = "funds_collection"


def create_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    print("✅ Collection created")


def insert_embeddings():
    with open("data/sample_funds.json") as f:
        funds = json.load(f)

    points = []

    for i, fund in enumerate(funds):
        text = fund["description"]
        vector = model.encode(text).tolist()

        points.append({
            "id": i,
            "vector": vector,
            "payload": fund
        })

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("✅ Embeddings stored in Qdrant")


if __name__ == "__main__":
    create_collection()
    insert_embeddings()