from typing import TypedDict, Annotated, List, Optional
import operator

class AgentState(TypedDict):
    #user inputs
    user_query: str
    destination: str
    
    #Brain data 
    research_reports: Annotated[List, operator.add]
    trust_scores: dict
    
    #Output data
    itinerary: Optional[dict]
    budget_estimation: Optional[dict]
    
    #Flow control
    next_step: str
    is_approved: bool
    
    