from agents.base_agent import BaseAgent
from workflow.state import WorkflowState, AgentRole, WorkflowPhase
import json
import re

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
        
        IMPORTANT ROUTING RULES:
        - If user asks to "generate", "create", "write", "draft" a document/SWZ -> route to "Drafter"
        - If user asks to "check", "validate", "verify" -> route to "Validator"
        - If user asks legal questions or about law/regulations -> route to "Legal Officer" or "Legal Researcher"
        - If user provides information or answers questions -> route to "Interviewer"
        - If user asks to edit, modify, update the document -> route to "Drafter"
        
        Analyze the current state and history.
        Output a JSON object with:
        - "next_agent": The role of the next agent to act. Must be one of: "Interviewer", "Legal Officer", "Legal Researcher", "Drafter", "Validator"
        - "phase_update": (Optional) New phase to transition to.
        - "thought": Your reasoning.
        
        Example:
        {
            "next_agent": "Drafter",
            "phase_update": "ASSEMBLY",
            "thought": "User requested document generation."
        }
        """

    async def decide_next_step(self, state: WorkflowState) -> dict:
        # Check for explicit document generation requests first
        if state.history:
            last_user_msg = None
            for msg in reversed(state.history):
                if msg.role == AgentRole.USER:
                    last_user_msg = msg.content.lower()
                    break
            
            if last_user_msg:
                # Direct routing for common requests
                draft_keywords = ["wygeneruj", "stwórz", "napisz", "utwórz", "generuj", "draft", "dokument", "swz", "generate", "create"]
                edit_keywords = ["edytuj", "zmień", "popraw", "dodaj", "usuń", "edit", "modify", "change", "add"]
                validate_keywords = ["sprawdź", "zweryfikuj", "waliduj", "check", "validate", "verify"]
                
                if any(kw in last_user_msg for kw in draft_keywords):
                    return {
                        "next_agent": "Drafter",
                        "phase_update": "ASSEMBLY",
                        "thought": "User requested document generation or editing."
                    }
                
                if any(kw in last_user_msg for kw in validate_keywords):
                    return {
                        "next_agent": "Validator",
                        "phase_update": "AUDIT",
                        "thought": "User requested document validation."
                    }
        
        # Use LLM for more complex decisions
        response = await self.process(state)
        content = response["content"]
        
        # Clean up code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        # Try to extract JSON from the response
        json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group()
            
        try:
            return json.loads(content.strip())
        except:
            # Fallback if JSON parsing fails
            return {"next_agent": "Interviewer", "thought": "Failed to parse decision, defaulting to Interviewer."}
