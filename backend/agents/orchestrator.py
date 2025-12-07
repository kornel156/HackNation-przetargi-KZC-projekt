from agents.base_agent import BaseAgent
from workflow.state import AgentRole, WorkflowState, SWZSection
import json

class Orchestrator(BaseAgent):
    def __init__(self):
        super().__init__(role=AgentRole.ORCHESTRATOR)

    def get_system_instruction(self) -> str:
        return """
        You are the Orchestrator of the SWZ Architect system.
        Your job is to understand the user's intent and route them to the correct specialized agent.
        
        Available Agents/Sections:
        - BASIC_DATA_AGENT: For organization details, address, contact info (Section I).
        - SUBJECT_AGENT: For procurement title, description, CPV codes, mode (Section II & III).
        - CRITERIA_AGENT: For evaluation criteria and weights (Section VII).
        - LEGAL_RESEARCHER: For specific legal questions about PZP (Public Procurement Law).
        
        Output a JSON object with the following structure:
        {
            "thought": "Reasoning for your decision",
            "next_agent": "AgentRole (e.g., 'Basic Data Agent', 'Subject Agent', 'Criteria Agent', 'Legal Researcher', or 'Orchestrator' if unclear)",
            "active_section": "SWZSection (e.g., 'I_BASIC_DATA', 'II_SUBJECT', 'VII_CRITERIA', or 'none')",
            "response_to_user": "Optional message to user if you are handling it directly or transitioning"
        }
        
        If the user wants to start from the beginning, route to BASIC_DATA_AGENT.
        If the user asks a legal question, route to LEGAL_RESEARCHER.
        If the user provides data for a specific section, route to that section's agent.
        """

    async def process(self, state: WorkflowState, user_input: str) -> str:
        # The orchestrator analyzes the input and decides the next step
        # It doesn't generate the final response usually, but directs the flow.
        
        prompt = f"""
        {self.get_system_instruction()}
        
        Current Active Section: {state.active_section}
        User Input: {user_input}
        """
        
        response = self.model.generate_content(prompt).text
        
        # Clean up json block if present
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
            
        return response.strip()
