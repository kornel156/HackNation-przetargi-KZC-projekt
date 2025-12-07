from agents.base_agent import BaseAgent
from workflow.state import AgentRole, WorkflowState, SWZSection
from agents.prompts import *
import json

class SupportingAgent(BaseAgent):
    def __init__(self, role: AgentRole, system_prompt: str):
        super().__init__(role=role)
        self.system_prompt = system_prompt

    def get_system_instruction(self) -> str:
        return self.system_prompt

    async def process(self, state: WorkflowState, user_input: str) -> str:
        # Supporting agents might need access to the full generated sections or specific data
        swz_context = f"Current SWZ Data: {state.swz_data.model_dump_json()}"
        
        prompt = f"""
        {self.get_system_instruction()}
        
        {swz_context}
        
        User Input: {user_input}
        """
        
        response = self.model.generate_content(prompt).text
        return response

class AgentWalidacjaGlowna(SupportingAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_WALIDACJA_GLOWNA, AGENT_WALIDACJA_GLOWNA_PROMPT)

class AgentFormatowanie(SupportingAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_FORMATOWANIE, AGENT_FORMATOWANIE_PROMPT)

class AgentZgodnoscPzp(SupportingAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_ZGODNOSC_PZP, AGENT_ZGODNOSC_PZP_PROMPT)

class AgentZalaczniki(SupportingAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_ZALACZNIKI, AGENT_ZALACZNIKI_PROMPT)

class AgentAnalizaKomunikacji(SupportingAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_ANALIZA_KOMUNIKACJI, AGENT_ANALIZA_KOMUNIKACJI_PROMPT)
