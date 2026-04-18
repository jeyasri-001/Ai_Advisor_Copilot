import sys
import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from rag.hybrid_search import search


def main():
    print("\n" + "="*60)
    print("💼 FundsIndia AI Advisor Copilot")
    print("="*60)
    print("\nAsk me about mutual funds and investment strategies!")
    print("Type 'exit' to quit.\n")
    
    conversation_history = []
    
    while True:
        try:
            query = input("\n💬 You: ").strip()
            
            if query.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Thank you for using FundsIndia Copilot! Happy investing!")
                break
            
            if not query:
                continue
            
            # Add user message to history
            conversation_history.append({
                "role": "user",
                "content": query
            })
            
            # Get response
            response = search(query, conversation_history)
            
            # Add bot response to history
            if response:
                conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'exit' to quit.")


if __name__ == "__main__":
    main()
