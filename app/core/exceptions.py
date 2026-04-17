class TravelIntelError(Exception):
    """Base exception for our system"""
    pass

class AgentExecutionError(TravelIntelError):
    """Jab koi specific agent (Researcher/Planner) fail ho jaye"""
    def __init__(self, agent_name: str, message: str):
        self.agent_name = agent_name
        self.message = message
        super().__init__(f"Agent [{agent_name}] failed: {message}")

class InsufficientDataError(TravelIntelError):
    """Jab Trust Score ke liye enough real reviews na milein"""
    pass

class SafetyTriggerError(TravelIntelError):
    """Jab AI content policies ya safety guardrails hit hon"""
    pass