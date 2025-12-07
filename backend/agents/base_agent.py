import os
import google.generativeai as genai
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from workflow.state import WorkflowState, Message, AgentRole

class BaseAgent(ABC):
    def __init__(self, role: AgentRole, model_name: str = None):
        self.role = role
        self.model_name = model_name or os.getenv("GOOGLE_MODEL_NAME", "gemini-1.5-flash")
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
             # Fallback or error handling, for now assuming it will be there
             pass
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    @abstractmethod
    def get_system_instruction(self) -> str:
        """Returns the system instruction for the specific agent."""
        pass

    async def process(self, state: WorkflowState, user_input: str = None) -> Dict[str, Any]:
        """
        Processes the current state and user input to generate a response or action.
        Returns a dictionary with 'content' and optional 'metadata'.
        """
        system_instruction = self.get_system_instruction()
        
        # Construct prompt from history and current state
        prompt = f"{system_instruction}\n\n"
        prompt += "Current Workflow Phase: " + state.phase.value + "\n"
        prompt += "Current SWZ Data: " + str(state.swz_data.model_dump(exclude_none=True)) + "\n\n"
        
        prompt += "Conversation History:\n"
        for msg in state.history[-10:]: # Context window management
            prompt += f"{msg.role.value}: {msg.content}\n"
            
        if user_input:
            prompt += f"User: {user_input}\n"
            
        prompt += f"\n{self.role.value}:"

        try:
            response = self.model.generate_content(prompt)
            return {"content": response.text}
        except Exception as e:
            return {"content": f"Error generating response: {str(e)}"}
