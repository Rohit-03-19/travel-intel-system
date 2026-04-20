import os
import json
from app.agents.state import AgentState
from app.core.logging import logger
from langchain_groq import ChatGroq
from app.core.config import settings

# Groq Setup - JSON Mode locked
llm = ChatGroq(
    temperature=0.1, # Temperature aur kam kiya taaki logic ekdum sharp rahe
    model="llama-3.3-70b-versatile", 
    groq_api_key=settings.GROQ_API_KEY
).bind(response_format={"type": "json_object"})

def planner_node(state: AgentState):
    logger.info("--- 🧠 GENERATING LOGISTICS-HEAVY EXECUTION PLAN ---")
    
    destination = state.get("destination")
    user_query = state.get("user_query")
    # Research context se 'Ground Reality' uthayi
    research_context = state["research_reports"][-1] if state["research_reports"] else "No research available."
    
    # Inside planner_node function
    prompt = f"""
    You are a Professional Travel Guide & Budget Strategist. Create a detailed 'Day 1' execution plan for {destination}.

    STRICT NOMENCLATURE:
    - The plan title should be "DAY 1: [Destination Name] Execution".
    - Divide the day into 3-4 logical blocks based on TIME and AREA (e.g., '08:00 AM - 11:00 AM: Arrival & Local Transit').

    STRICT BULLET POINT RULES:
    1. Every point MUST include a duration and approximate cost in brackets.
    2. Format: "Emoji [Duration] [Cost] Activity/Food/Tip Detail"
    3. Cost should be in INR (e.g., ₹500). If it's free, write ₹0.

    RESEARCH DATA: {research_context}
    USER BUDGET & VIBE: {user_query}

    STRICT JSON FORMAT:
    {{
    "itinerary": {{
        "08:00 AM - 11:00 AM: [Area/Theme Name]": [
        "📍 [1 hour] [₹200] Activity description with specific location names.",
        "🍴 [45 mins] [₹300] Food recommendation with approximate cost.",
        "💡 [0 mins] [₹0] Practical hack regarding this time/area block."
        ],
        "[Next Time Block]": [],
        "[Next Time Block]": []
    }},
    "verdict": "Detailed safety and budget reassurance."
    }}
    """
    
    try:
        response = llm.invoke(prompt)
        # Parse logic to handle JSON string
        structured_data = json.loads(response.content)
        
        # Itinerary extract karna
        itinerary = structured_data.get("itinerary", {})
        verdict = structured_data.get("verdict", "Logistics verified for safety.")

        return {
            "itinerary": itinerary,
            "reality_report": verdict,
            "next_step": "concierge"
        }
    except Exception as e:
        logger.error(f"PLANNER_NODE ERROR: {e}")
        # Robust Fallback
        return {
            "itinerary": {
                "System Alert": [
                    "📍 Transit logic failed to parse.",
                    "🍴 Check your backend connection.",
                    "💡 Tip: Try a more specific query like 'Kedarnath trek from Gaurikund'."
                ]
            },
            "reality_report": "Error in generating logistics. Check terminal logs.",
            "next_step": "concierge"
        }