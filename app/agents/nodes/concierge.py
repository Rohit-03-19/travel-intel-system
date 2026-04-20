import os
from app.agents.state import AgentState
from app.core.logging import logger
from app.tools.search_tool import search_real_reviews
from app.tools.budget_utils import calculate_estimated_budget
from langchain_groq import ChatGroq
from app.core.config import settings

# Groq Setup
llm = ChatGroq(
    temperature=0.2, 
    model="llama-3.3-70b-versatile", 
    groq_api_key=settings.GROQ_API_KEY
)

def concierge_node(state: AgentState):
    logger.info("--- 🏨 CONCIERGE: FINDING SAFE & VIBEY STAYS ---")
    
    destination = state.get("destination")
    user_query = state.get("user_query", "").lower()
    # Research reports se safety context lo
    research_report = state["research_reports"][-1] if state["research_reports"] else ""
    
    # 1. Determine Tier
    tier = "budget" if any(word in user_query for word in ["low budget", "cheap", "affordable"]) else "mid"
    
    # 2. Search for real stays
    search_query = f"best rated clean {tier} stays in {destination} near main temples 2026 safe areas"
    stay_data = search_real_reviews(search_query)
    
    # 3. Smart Selection (Using context to avoid bad areas)
    prompt = f"""
    You are a Strategic Concierge. Suggest 2-3 best stays in {destination} for a {tier} traveler.
    
    SAFETY CONTEXT FROM RESEARCH:
    {research_report}
    
    STAY DATA FOUND:
    {stay_data}
    
    REQUIREMENTS:
    - Ensure stays are in areas NOT affected by heavy construction or safety issues mentioned.
    - Focus on 'Value for Money' and 'Authentic Experience'.
    - Be brief and helpful.
    """
    
    stay_suggestions = llm.invoke(prompt)
    
    # 4. Math Budget (1 Day default)
    math_budget = calculate_estimated_budget(days=1, tier=tier)
    
    return {
        "budget_estimation": {
            "stay_options": stay_suggestions.content,
            "financial_breakdown": math_budget
        },
        "next_step": "END"
    }