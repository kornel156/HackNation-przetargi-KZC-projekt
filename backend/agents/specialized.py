from agents.base_agent import BaseAgent
from workflow.state import AgentRole, WorkflowState, SWZSection
import json

class SpecializedAgent(BaseAgent):
    def __init__(self, role: AgentRole, section: SWZSection):
        super().__init__(role=role)
        self.section = section

    async def process(self, state: WorkflowState, user_input: str) -> str:
        # This is a simplified process loop for specialized agents
        # They should check if they have enough info to generate the section
        # If not, they ask the user.
        # If yes, they generate the section and set to_render=True (handled by manager/orchestrator)
        
        system_instruction = self.get_system_instruction()
        
        # We inject the current SWZ data into the prompt
        swz_context = f"Current SWZ Data: {state.swz_data.model_dump_json()}"
        
        prompt = f"""
        {system_instruction}
        
        {swz_context}
        
        User Input: {user_input}
        
        If you have gathered all necessary information for your section, output the final section content in Markdown format.
        Start the final content with "SECTION_COMPLETE:" followed by the markdown.
        If you need more information, ask the user a specific question.
        """
        
        response = self.model.generate_content(prompt).text
        return response

class BasicDataAgent(SpecializedAgent):
    def __init__(self):
        super().__init__(role=AgentRole.BASIC_DATA_AGENT, section=SWZSection.I_BASIC_DATA)

    def get_system_instruction(self) -> str:
        return """
        You are the Basic Data Agent. Your goal is to draft "Rozdział I. Nazwa i adres Zamawiającego" of the SWZ.
        You need to gather:
        - Organization Name (Nazwa zamawiającego)
        - Address (Ulica, kod, miasto)
        - NIP
        - Website (Adres strony internetowej)
        - E-mail
        
        Ask the user for these details if they are missing.
        Once you have them, generate the section in Markdown.
        """

class SubjectAgent(SpecializedAgent):
    def __init__(self):
        super().__init__(role=AgentRole.SUBJECT_AGENT, section=SWZSection.II_SUBJECT)

    def get_system_instruction(self) -> str:
        return """
        You are the Subject Agent. Your goal is to draft "Rozdział II. Tryb udzielenia zamówienia" and "Rozdział III. Opis przedmiotu zamówienia".
        You need to gather:
        - Procurement Title (Nazwa zamówienia)
        - Short Description (Krótki opis)
        - CPV Codes (Kody CPV)
        - Procurement Mode (Tryb, e.g., Tryb Podstawowy)
        
        Ask the user for these details if they are missing.
        Once you have them, generate the section in Markdown.
        """

class CriteriaAgent(SpecializedAgent):
    def __init__(self):
        super().__init__(role=AgentRole.CRITERIA_AGENT, section=SWZSection.VII_CRITERIA)

    def get_system_instruction(self) -> str:
        return """
        You are the Criteria Agent. Your goal is to draft "Rozdział VII. Kryteria oceny ofert".
        You need to gather:
        - List of criteria (e.g., Price, Warranty, Experience)
        - Weights for each criterion (must sum to 100%)
        
        Ask the user for these details if they are missing.
        Once you have them, generate the section in Markdown.
        """
