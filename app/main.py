from app.agents.graph import travel_agent_app
from app.core.logging import setup_logging, logger

setup_logging()

def run_test_query():
    inputs = {
        "user_query": "I want to visit Vrindavan in a low budget",
        "destination": "Vrindavan",
        "research_reports": [],
        "trust_scores": {},
        "is_approved": False
    }
    
    logger.info("Starting Agentic Workflow...")
    
    # Run the graph
    for output in travel_agent_app.stream(inputs):
        for key, value in output.items():
            logger.info(f"Finished Node: {key}")
            # print(value) # Debugging ke liye value check kar sakte ho

if __name__ == "__main__":
    run_test_query()