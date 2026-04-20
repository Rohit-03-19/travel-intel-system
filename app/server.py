from fastapi import FastAPI, HTTPException
from app.api.schemas import ModifyTripRequest, TripRequest, TripResponse
from app.agents.graph import travel_agent_app
from app.db.database import save_trip, init_db, get_all_trips, get_trip_by_id
from typing import List, Dict
import uvicorn
import uuid
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# .env se variables load karo
load_dotenv()

app = FastAPI(title="Travel Intel AI Agent")

# --- 1. Global Memory Store ---
# Ye threads ko save rakhega taaki frontend naye page par data fetch kar sake
threads: Dict[str, dict] = {}

# --- 2. CORS Setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB initialize on startup
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Travel Intel API is Live!"}

# --- 3. Plan a New Trip (Initiates Research & Pauses) ---
@app.post("/plan-trip")
async def plan_trip(request: TripRequest):
    try:
        # Unique Thread ID generate karo
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        inputs = {
            "user_query": request.user_query,
            "destination": request.destination,
            "research_reports": [],
            "trust_scores": {},
            "itinerary": {},
            "is_approved": False
        }
        
        # Graph invoke karo - Ye 'planner' node se pehle ruk jayega
        final_state = travel_agent_app.invoke(inputs, config=config)
        
        # Researcher ki report nikalo
        report = final_state.get("research_reports", [""])[-1]
        
        # SAVE TO MEMORY: Iske bina frontend ko naye page par data nahi milega
        threads[thread_id] = {
            "thread_id": thread_id,
            "status": "AWAITING_APPROVAL",
            "reality_report": report,
            "destination": request.destination,
            "user_query": request.user_query,
            "itinerary": {}
        }
        
        return {
            "thread_id": thread_id,
            "status": "AWAITING_APPROVAL",
            "message": "Reality check complete. Please review the report.",
            "reality_report": report,
            "destination": request.destination
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Planning failed: {str(e)}")

# --- 4. Get Trip Status (Frontend Data Fetching) ---
@app.get("/trip-status/{thread_id}")
async def get_trip_status(thread_id: str):
    if thread_id in threads:
        return threads[thread_id]
    raise HTTPException(status_code=404, detail="Thread not found. Server might have restarted.")

# --- 5. Approve Trip (Resumes Graph to Generate Itinerary) ---
@app.post("/approve-trip/{thread_id}")
async def approve_trip(thread_id: str):
    try:
        if thread_id not in threads:
            raise HTTPException(status_code=404, detail="Thread not found")

        config = {"configurable": {"thread_id": thread_id}}
        
        # Resume Execution: None pass karne se LangGraph wahan se shuru karega jahan interrupt hua tha
        final_state = travel_agent_app.invoke(None, config=config)
        
        dest = final_state.get("destination")
        plan = final_state.get("itinerary", {})
        report = final_state.get("research_reports", [""])[-1]
        
        # Update thread in memory
        threads[thread_id]["status"] = "COMPLETED"
        threads[thread_id]["itinerary"] = plan
        
        # Final result DB mein save karo history ke liye
        trip_id = save_trip("Approved Trip", dest, plan, report)
        
        return {
            "trip_id": trip_id,
            "thread_id": thread_id,
            "destination": dest,
            "itinerary": plan,
            "reality_report": report,
            "status": "COMPLETED"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Approval failed: {str(e)}")

# --- 6. Modify an Existing Trip ---
@app.post("/modify-trip", response_model=TripResponse)
async def modify_trip(request: ModifyTripRequest):
    old_trip = get_trip_by_id(request.trip_id)
    if not old_trip:
        raise HTTPException(status_code=404, detail="Original trip not found")

    try:
        inputs = {
            "user_query": f"MODIFICATION: {request.modification_query} | PREVIOUS: {old_trip.final_plan}",
            "destination": old_trip.destination,
            "research_reports": [old_trip.reality_report],
            "trust_scores": {},
            "itinerary": old_trip.final_plan,
            "is_approved": True 
        }
        
        # Naya thread for modification
        new_thread_id = str(uuid.uuid4())
        final_state = travel_agent_app.invoke(inputs, config={"configurable": {"thread_id": new_thread_id}})
        
        new_plan = final_state.get("itinerary", {})
        new_report = final_state.get("research_reports", [""])[-1]
        
        new_trip_id = save_trip(f"MODIFIED: {request.modification_query}", old_trip.destination, new_plan, new_report)
        
        return {
            "trip_id": new_trip_id,
            "destination": old_trip.destination,
            "itinerary": new_plan,
            "reality_report": new_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 7. History Endpoints ---
@app.get("/trips", response_model=List[TripResponse])
async def list_trips():
    history = get_all_trips()
    return [
        {
            "trip_id": t.id,
            "destination": t.destination,
            "itinerary": t.final_plan if isinstance(t.final_plan, dict) else {"plan": t.final_plan},
            "reality_report": t.reality_report
        } for t in history
    ]

@app.get("/trips/{trip_id}", response_model=TripResponse)
async def get_single_trip(trip_id: int):
    trip = get_trip_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found.")
    return {
        "trip_id": trip.id,
        "destination": trip.destination,
        "itinerary": trip.final_plan if isinstance(trip.final_plan, dict) else {"plan": trip.final_plan},
        "reality_report": trip.reality_report
    }

if __name__ == "__main__":
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=True)