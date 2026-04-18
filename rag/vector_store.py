from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Try Streamlit secrets first, fallback to environment variable
try:
    import streamlit as st
    qdrant_url = st.secrets.get("QDRANT_URL", os.getenv("QDRANT_URL"))
    qdrant_api_key = st.secrets.get("QDRANT_API_KEY", os.getenv("QDRANT_API_KEY"))
except:
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

# Qdrant client
client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
)

COLLECTION_NAME = "funds_collection"


def search_funds(query):
    print(f"\n🔍 Searching for: {query}")

    query_vector = model.encode(query).tolist()

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=5
    )

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