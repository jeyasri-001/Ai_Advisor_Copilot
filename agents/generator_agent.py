from groq import Groq
import os
from dotenv import load_dotenv
from config.system_prompt import get_advisor_prompt
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_response(
    query: str,
    fund_results: list,
    conversation_history: list = None,
    retrieved_context: str = "",
    graph_insights: str = ""
) -> str:

    # Convert fund results → names and details
    fund_names = []
    fund_details_text = ""
    for f in fund_results:
        if isinstance(f, dict):
            name = f.get("name", "Unknown Fund")
            fund_names.append(name)
            category = f.get("category", "N/A")
            risk = f.get("risk", "N/A")
            nav = f.get("nav", "N/A")
            amc = f.get("amc", "N/A")
            fund_details_text += f"\n- {name} (Category: {category}, Risk: {risk}, NAV: {nav}, AMC: {amc})"
        else:
            fund_names.append(str(f))

    system_prompt = get_advisor_prompt(
        query=query,
        funds=fund_names,
        retrieved_context=retrieved_context,
        graph_insights=graph_insights
    )

    messages = [{
        "role": "system",
        "content": system_prompt
    }]

    if conversation_history and len(conversation_history) > 0:
        messages.extend(conversation_history[-4:])

    messages.append({
        "role": "user",
        "content": query
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.9
    )

    final = response.choices[0].message.content

    safety = safety_check(final, query)

    if not safety["is_safe"]:
        final += "\n\n⚠️ " + ", ".join(safety["warnings"])

    return final


def safety_check(response: str, query: str):

    warnings = []

    if re.search(r'\bguaranteed\b|\b100%|\bdefinitely\b', response, re.I):
        warnings.append("Avoid guarantee claims")

    if re.search(r'\d+%\s*(return|profit)', response) and \
       not re.search(r'(past|historical)', response, re.I):
        warnings.append("Return % without context")

    if "zero risk" in response.lower() and "zero risk" not in query.lower():
        warnings.append("Unrealistic zero-risk implication")

    return {
        "is_safe": len(warnings) == 0,
        "warnings": warnings
    }