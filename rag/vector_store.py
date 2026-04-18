from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Qdrant client
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = "funds_collection"


def search_funds(query):
    print(f"\n🔍 Searching for: {query}")

    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=5
    ).points

    print("\n🎯 Top Matching Funds:\n")

    fund_results = []
    for i, result in enumerate(results):
        payload = result.payload
        fund_results.append(payload)

        print(f"{i+1}. {payload['fund_name']}")
        print(f"   Category: {payload['category']}")
        print(f"   AMC: {payload['amc']}")
        print(f"   NAV: {payload['nav']}")
        print("-" * 40)
    
    return fund_results


if __name__ == "__main__":
    while True:
        query = input("\n💬 Ask something (or type 'exit'): ")

        if query.lower() == "exit":
            break

        search_funds(query)