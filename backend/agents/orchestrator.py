from agents.base_agent import BaseAgent
from workflow.state import WorkflowState, AgentRole, WorkflowPhase
import json

class Orchestrator(BaseAgent):
    def __init__(self):
        super().__init__(role=AgentRole.ORCHESTRATOR)

    def get_system_instruction(self) -> str:
        return """
        You are the Orchestrator (Koordynator Procesu) of the SWZ-Architect system.
        Your role is to manage the workflow and decide which agent should act next.
        You do not generate the SWZ content yourself, but you direct the flow.
        
        The phases are:
        1. INITIATION: Gather basic info (Interviewer).
        2. LEGAL_RESEARCH: Research applicable laws (Legal Researcher).
        3. LEGAL_CORE: Define mode and conditions (Legal Officer).
        4. SPECS_CRITERIA: Define subject and criteria (Interviewer & Validator).
        5. ASSEMBLY: Generate the document (Drafter).
        6. AUDIT: Verify the document (Validator).
        
        Analyze the current state and history.
        Output a JSON object with:
        - "next_agent": The role of the next agent to act.
        - "phase_update": (Optional) New phase to transition to.
        - "thought": Your reasoning.
        
        Example:
        {
            "next_agent": "Interviewer",
            "thought": "We need to get the organization name."
        }
        """

    async def decide_next_step(self, state: WorkflowState) -> dict:
        # Specialized method for orchestrator to return structured decision
        response = await self.process(state)
        content = response["content"]
        # Clean up code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        try:
            return json.loads(content.strip())
        except:
            # Fallback if JSON parsing fails
            return {"next_agent": "Interviewer", "thought": "Failed to parse decision, defaulting to Interviewer."}
