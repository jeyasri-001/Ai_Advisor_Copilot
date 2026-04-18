from groq import Groq
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def critique_response(query: str, response: str, fund_names: list) -> dict:
    """Validate response for quality and compliance"""
    
    issues = []
    
    # Check 1: Response length (should be substantial)
    if len(response.split()) < 50:
        issues.append("Response too brief - needs more detail")
    
    # Check 2: Compliance checks
    if re.search(r'\bguaranteed\b|\b100%\s*return|\bdefinitely\b', response, re.I):
        issues.append("Contains risky guarantee claims")
    
    if re.search(r'\d+%\s*(return|profit|gain)', response) and \
       not re.search(r'(past|historical|may|could)', response, re.I):
        issues.append("Return claims lack proper context")
    
    # Check 3: Fund recommendations exist
    fund_mentioned = any(fund.lower() in response.lower() for fund in fund_names)
    if not fund_mentioned and len(fund_names) > 0:
        issues.append("No specific funds mentioned in response")
    
    # Check 4: Conversational tone
    if response.count('\n') > 8 or response.count('•') > 5:
        issues.append("Response too structured - needs natural tone")
    
    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "confidence": 1.0 - (len(issues) * 0.2)
    }


def improve_response(query: str, response: str, issues: list) -> str:
    """Enhance response based on critique"""
    
    if not issues:
        return response
    
    system_prompt = f"""You are a financial advisor. The user asked: "{query}"
    
Your previous response had these issues: {', '.join(issues)}

Rewrite the response to:
1. Be more detailed and conversational (2-3 paragraphs minimum)
2. Explain WHY you recommend specific funds
3. Use natural language, not bullet points
4. Include relevant fund details (category, risk, why it suits them)
5. Avoid guarantees and unrealistic claims

Keep the same recommendations but make it more human and detailed."""
    
    response_obj = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": response}],
        system=system_prompt,
        temperature=0.7,
        max_tokens=1500
    )
    
    return response_obj.choices[0].message.content
