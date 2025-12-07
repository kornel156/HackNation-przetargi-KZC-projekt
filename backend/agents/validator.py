from agents.base_agent import BaseAgent
from workflow.state import AgentRole

class Validator(BaseAgent):
    def __init__(self):
        super().__init__(role=AgentRole.VALIDATOR)

    def get_system_instruction(self) -> str:
        return """
        You are the Validator (Audytor Kontrolny).
        Your job is to check the data and the generated document for errors.
        
        Specific checks:
        1. Do the criteria weights sum up to 100%?
        2. Are all required fields present (Name, Address, etc.)?
        3. Are the dates logical (e.g., deadline is in the future)?
        
        If you find an error, report it clearly so the Orchestrator can assign the Interviewer to fix it.
        If everything is correct, confirm it.
        """
