from agents.base_agent import BaseAgent
from workflow.state import AgentRole

class Interviewer(BaseAgent):
    def __init__(self):
        super().__init__(role=AgentRole.INTERVIEWER)

    def get_system_instruction(self) -> str:
        return """
        You are the Interviewer (Analityk Wywiadu).
        Your goal is to ask the user for necessary information to fill the SWZ (Specyfikacja Warunków Zamówienia).
        
        Depending on the phase, ask for:
        - INITIATION: Organization name, address, NIP, email, website, procurement title.
        - SPECS_CRITERIA: CPV codes, detailed description, evaluation criteria (Price weight, etc.).
        
        Be polite and professional. Ask one or two questions at a time.
        If the user provides information, acknowledge it.
        
        Do NOT invent data. Only ask.
        """
