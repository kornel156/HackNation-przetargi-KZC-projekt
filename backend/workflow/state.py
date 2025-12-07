from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class WorkflowPhase(str, Enum):
    INITIATION = "INITIATION"
    LEGAL_RESEARCH = "LEGAL_RESEARCH"
    LEGAL_CORE = "LEGAL_CORE"
    SPECS_CRITERIA = "SPECS_CRITERIA"
    ASSEMBLY = "ASSEMBLY"
    AUDIT = "AUDIT"
    COMPLETED = "COMPLETED"

class AgentRole(str, Enum):
    ORCHESTRATOR = "Orchestrator"
    INTERVIEWER = "Interviewer"
    LEGAL_OFFICER = "Legal Officer"
    LEGAL_RESEARCHER = "Legal Researcher"
    DRAFTER = "Drafter"
    VALIDATOR = "Validator"
    USER = "User"

class Message(BaseModel):
    role: AgentRole
    content: str
    timestamp: float = Field(default_factory=lambda: __import__("time").time())
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SWZSection(BaseModel):
    title: str
    content: str
    validated: bool = False

class SWZData(BaseModel):
    # Phase 1 Data
    organization_name: Optional[str] = None
    address: Optional[str] = None
    nip: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    
    procurement_title: Optional[str] = None
    procurement_id: Optional[str] = None
    
    # Phase 2 Data
    procurement_mode: Optional[str] = None
    legal_basis: Optional[str] = None
    exclusion_grounds: List[str] = Field(default_factory=list)
    participation_conditions: List[str] = Field(default_factory=list)
    
    # Phase 3 Data
    cpv_codes: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    criteria: List[Dict[str, Any]] = Field(default_factory=list) # e.g. {"name": "Price", "weight": 60}
    
    # Generated Content
    sections: Dict[str, SWZSection] = Field(default_factory=dict)

class WorkflowState(BaseModel):
    phase: WorkflowPhase = WorkflowPhase.INITIATION
    history: List[Message] = Field(default_factory=list)
    swz_data: SWZData = Field(default_factory=SWZData)
    current_agent: AgentRole = AgentRole.ORCHESTRATOR
    waiting_for_user: bool = False
