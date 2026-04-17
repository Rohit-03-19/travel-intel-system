from app.agents.state import AgentState
from app.core.logging import logger
from app.tools.search_tool import search_real_reviews
from langchain_openai import ChatOpenAI
from app.core.config import settings

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY)

def researcher_node(state: AgentState):
    destination = state.get("destination", "the destination")
    logger.info(f"--- RESEARCHING REALITY FOR: {destination} ---")
    
    # 1. Real-time Search (Looking for dirt/reality)
    search_query = f"current situation and honest traveler reviews for {destination} construction crowd scams safety April 2026"
    raw_results = search_real_reviews(search_query)
    
    # 2. Senior Critic Analysis
    prompt = f"""
    You are a highly experienced, cynical travel journalist known for exposing the 'Influencer vs Reality' gap.
    Analyze the following search data for {destination}:
    
    SEARCH DATA:
    {raw_results}
    
    YOUR TASKS:
    1. Identify 'Red Flags': Is there construction? Extreme crowds? Recent scams? Bad weather?
    2. Influencer vs Reality: What are influencers hiding that real people are complaining about?
    3. Calculate a 'Trust Score' (1.0 to 10.0) based on how reliable the destination is right now.
    
    Provide a concise, blunt report for the traveler.
    """
    
    response = llm.invoke(prompt)
    
    # Return updated state
    return {
        "research_reports": [response.content],
        "trust_scores": {destination: "Analyzed via Web Search"},
        "next_step": "planner"
    }