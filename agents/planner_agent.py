from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def plan_query(query: str) -> dict:
    """Analyze user intent and create search strategy"""
    
    system_prompt = """You are a financial advisor assistant. Analyze the user's query and extract:
1. investment_goal: (growth/income/safety/liquidity)
2. risk_level: (conservative/balanced/aggressive)
3. time_horizon: (short/medium/long)
4. search_keywords: (list of 2-3 keywords to search for)

Return ONLY valid JSON, no other text."""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": query}],
        system=system_prompt,
        temperature=0.3,
        max_tokens=300
    )
    
    try:
        result = json.loads(response.choices[0].message.content)
        return result
    except:
        return {
            "investment_goal": "growth",
            "risk_level": "balanced",
            "time_horizon": "medium",
            "search_keywords": [query]
        }
