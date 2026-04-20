from pydantic import BaseModel
from typing import Optional, Dict, Any

class TripRequest(BaseModel):
    user_query: str
    destination: str

class TripResponse(BaseModel):
    trip_id: int
    destination: str
    itinerary: Dict[str, Any]
    reality_report: str
    status: str = "success"
    
class ModifyTripRequest(BaseModel):
    trip_id: int
    modification_query: str  # Example: "Make it luxury" or "Add more temples"