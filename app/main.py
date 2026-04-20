from app.agents.graph import travel_agent_app
from app.core.logging import setup_logging, logger
from app.db.database import init_db, save_trip

setup_logging()
init_db()
def run_test_query():
    inputs = {
        "user_query": "I want to visit Vrindavan in a low budget. Suggest a realistic 1-day plan.",
        "destination": "Vrindavan",
        "research_reports": [],
        "trust_scores": {},
        "itinerary": {},
        "is_approved": False
    }
    
    logger.info("🚀 System Active: Optimizing your travel experience...")
    
    try:
        final_state = travel_agent_app.invoke(inputs)
        query = final_state.get("user_query")
        dest = final_state.get("destination")
        plan = final_state.get("itinerary", {}) # Dictionary form
        report = final_state.get("research_reports", [""])[-1]

        # 3. SAVE TO LOCAL DATABASE
        trip_id = save_trip(query, dest, plan, report)
        logger.info(f"💾 Trip saved successfully with ID: {trip_id}")
        print("\n" + "✨" + " ="*29)
        print(f"   VIBE CHECK & PLAN FOR: {final_state.get('destination').upper()}")
        print(" " + " ="*29 + "\n")

        # --- 1. THE ITINERARY (The Main Value) ---
        print("🗓️  YOUR SMART 1-DAY ITINERARY")
        print("-" * 40)
        itinerary = final_state.get("itinerary", {})
        if isinstance(itinerary, dict) and "plan" in itinerary:
            print(itinerary["plan"])
        else:
            print("Plan is being finalized...")

        # --- 2. STAYS & BUDGET (The Logistics) ---
        print("\n🏨 STAYS & BUDGET ESTIMATION")
        print("-" * 40)
        budget_data = final_state.get("budget_estimation", {})
        if budget_data:
            print(f"{budget_data.get('stay_options')}")
            breakdown = budget_data.get('financial_breakdown', {})
            print(f"\n💰 Estimated Cost: {breakdown.get('total_estimated')} {breakdown.get('currency')} (Daily)")
        else:
            print("Calculating best deals for you...")

        # --- 3. THE REALITY CHECK (The Fine Print / Warnings) ---
        print("\n" + "!" * 5 + " REALITY CHECK & SAFETY BRIEFING " + "!" * 5)
        print("-" * 40)
        reports = final_state.get("research_reports", [])
        if reports:
            print(reports[-1])
        else:
            print("Safety data unavailable at the moment.")

        print("\n" + "✨" + " ="*29 + "\n")

    except Exception as e:
        logger.error(f"❌ System Failure: {e}")

if __name__ == "__main__":
    # 1. Nayi Trip Generate Karo
    run_test_query()

    # 2. Check Karo ki DB mein kya hai
    from app.db.database import get_all_trips
    print("\n" + "📜" + " ="*29)
    print("   YOUR SAVED TRAVEL HISTORY")
    print(" ="*29)
    
    history = get_all_trips()
    for trip in history:
        print(f"ID: {trip.id} | Destination: {trip.destination} | Date: {trip.created_at.strftime('%Y-%m-%d')}")