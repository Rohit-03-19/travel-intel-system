import os
import datetime
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from app.core.config import settings
from app.agents.state import AgentState
from app.core.logging import logger

# 1. Environment Variables load karo (.env file se)
load_dotenv()

# 2. Modern Search Tool Setup
# Isse wo 'deprecated' wali warning khatam ho jayegi
search_tool = TavilySearchResults(max_results=5)

def researcher_node(state: AgentState):
    logger.info("--- Executing Balanced & Spiritual Researcher Node ---")
    
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    destination = state["destination"]
    
    # 3. Smart Search Query
    # Hum queries mein 'aura' aur 'significance' jaise words add kar rahe hain 
    # taaki LLM ko positive context bhi mile.
    search_query = f"current travel situation in {destination} April 2026 spiritual significance aura crowd construction safety"
    
    try:
        search_results = search_tool.invoke({"query": search_query})
    except Exception as e:
        logger.error(f"Search failed: {e}")
        search_results = "Search unavailable. Proceeding with general knowledge."

    # 4. The Balanced Advisor Prompt (The Sandwich Method)
    system_prompt = f"""
    You are a Senior Travel Intelligence Advisor with deep cultural empathy. 
    Your mission is to provide a BALANCED briefing for {destination} as of {current_date}.
    
    Follow this EXACT structure to ensure the traveler feels inspired but remains safe:
    
    1. 🌸 THE SOUL & VIBE: 
       Start with the destination's spiritual or historical aura. Mention local legends, 
       sacred elements (e.g., sacred trees of Nidhivan, ancient rituals), or the 
       general positive energy a traveler feels. Make it inviting.

    2. 📊 SEASONAL & CROWD INTELLIGENCE: 
       Discuss logistics. Weekends vs Weekdays crowds? Seasonal weather 
       (e.g., heat in April/May). Be practical.

    3. ⚠️ PRACTICAL CONSTRAINTS (GROUND REALITY): 
       Gently but clearly mention active construction, safety issues, or recent incidents. 
       Use a factual, non-alarmist tone. ALWAYS mention how a smart traveler can AVOID 
       these issues (e.g., use authorized guides, avoid boating in monsoon).

    4. 🚩 SMART SCORE & VERDICT: 
       Provide an 'Ease of Visit' score out of 10. 
       Conclude with one 'Pro-Tip' for a smooth experience.

    Keep the tone helpful, professional, and culturally respectful.
    """

    user_message = f"Analyze search data and provide a briefing for {destination}: \n\n {search_results}"

    # 5. LLM Call (Higher temperature for better descriptive writing)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4, groq_api_key = settings.GROQ_API_KEY) 
    response = llm.invoke([
        ("system", system_prompt),
        ("user", user_message)
    ])

    return {
        "research_reports": [response.content],
        "trust_scores": {"ease_of_visit": "Calculated in report"}
    }