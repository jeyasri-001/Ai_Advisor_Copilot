from rag.vector_store import search_funds
from graph.graph_retriever import get_fund_details
from agents.generator_agent import generate_response


def search(query: str, conversation_history: list = None):
    try:
        print(f"\n🔍 Query: {query}")

        # Vector Search
        print("📊 Searching vector database...")
        fund_results = search_funds(query)
        print(f"✅ Found {len(fund_results) if fund_results else 0} funds")

        if not fund_results:
            print("❌ No funds found")
            return "I couldn't find any relevant funds for your query. Please try rephrasing your question."

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
    except Exception as e:
        print(f"❌ Error in search: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"An error occurred: {str(e)}"