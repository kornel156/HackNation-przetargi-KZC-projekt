from typing import Dict, Any
from workflow.state import WorkflowState, Message, AgentRole, WorkflowPhase
from agents.orchestrator import Orchestrator
from agents.interviewer import Interviewer
from agents.legal import LegalOfficer
from agents.researcher import LegalResearcher
from agents.drafter import Drafter
from agents.validator import Validator

class WorkflowManager:
    def __init__(self):
        self.state = WorkflowState()
        self.agents = {
            AgentRole.ORCHESTRATOR: Orchestrator(),
            AgentRole.INTERVIEWER: Interviewer(),
            AgentRole.LEGAL_OFFICER: LegalOfficer(),
            AgentRole.LEGAL_RESEARCHER: LegalResearcher(),
            AgentRole.DRAFTER: Drafter(),
            AgentRole.VALIDATOR: Validator(),
        }

    async def process_user_input(self, user_input: str) -> str:
        # 1. Add user message to history
        self.state.history.append(Message(role=AgentRole.USER, content=user_input))
        
        # 2. Orchestrator decides next step
        orchestrator = self.agents[AgentRole.ORCHESTRATOR]
        decision = await orchestrator.decide_next_step(self.state)
        
        next_agent_role_str = decision.get("next_agent", "Interviewer")
        try:
            next_agent_role = AgentRole(next_agent_role_str)
        except ValueError:
            next_agent_role = AgentRole.INTERVIEWER
            
        # Update phase if orchestrator says so
        if "phase_update" in decision:
            try:
                self.state.phase = WorkflowPhase(decision["phase_update"])
            except ValueError:
                pass

        # 3. Execute Agent
        active_agent = self.agents.get(next_agent_role, self.agents[AgentRole.INTERVIEWER])
        self.state.current_agent = next_agent_role
        
        response = await active_agent.process(self.state, user_input)
        response_content = response["content"]
        
        # 4. Update State with Agent Response
        self.state.history.append(Message(role=next_agent_role, content=response_content))
        
        # 5. Check if we need to auto-transition or if we are waiting for user
        # For simplicity, we assume every agent response goes back to user unless it's an internal step
        # But to make it "agentic", we could loop here if the agent didn't ask a question.
        # For this implementation, we'll keep it simple: User -> Orchestrator -> Agent -> User.
        
        return response_content

    def get_state(self) -> Dict[str, Any]:
        return self.state.model_dump()
