from rag.vector_store import search_funds
from graph.graph_retriever import get_fund_details
from agents.generator_agent import generate_response


def search(query: str, conversation_history: list = None):

    print(f"\n🔍 Query: {query}")

    # Vector Search
    fund_results = search_funds(query)

    if not fund_results:
        print("❌ No funds found")
        return

    # LLM Response
    print("\n🤖 Generating AI Response...\n")
    
    # Convert fund_name to name for compatibility
    for f in fund_results:
        if "fund_name" in f and "name" not in f:
            f["name"] = f["fund_name"]
    
    answer = generate_response(
        query=query,
        fund_results=fund_results,
        conversation_history=conversation_history
    )

    print("\n🤖 AI Advisor Copilot:\n")
    print(answer)
    
    return answer