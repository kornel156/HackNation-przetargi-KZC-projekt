from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import time

class AgentRole(str, Enum):
    USER = "User"
    ORCHESTRATOR = "Orchestrator"
    INTERVIEWER = "Interviewer"
    LEGAL_OFFICER = "Legal Officer"
    LEGAL_RESEARCHER = "Legal Researcher"
    DRAFTER = "Drafter"
    VALIDATOR = "Validator"
    # Specialized Agents
    BASIC_DATA_AGENT = "Basic Data Agent"
    SUBJECT_AGENT = "Subject Agent"
    CRITERIA_AGENT = "Criteria Agent"

class SWZSection(str, Enum):
    NONE = "none"
    I_BASIC_DATA = "I_BASIC_DATA"
    II_SUBJECT = "II_SUBJECT"
    III_EXCLUSION = "III_EXCLUSION"
    IV_PROCEDURE = "IV_PROCEDURE"
    V_DOCUMENTS = "V_DOCUMENTS"
    VI_COMMUNICATION = "VI_COMMUNICATION"
    VII_CRITERIA = "VII_CRITERIA"
    # Add more as needed

class Message(BaseModel):
    role: AgentRole
    content: str
    timestamp: float = Field(default_factory=lambda: time.time())
    metadata: Dict[str, Any] = Field(default_factory=dict)
    to_render: bool = False # Flag to indicate if this message contains a finished section to render

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
    
    # Generated Content (Stored as strings for now, or dicts)
    sections: Dict[str, str] = Field(default_factory=dict)

class WorkflowState(BaseModel):
    history: List[Message] = Field(default_factory=list)
    swz_data: SWZData = Field(default_factory=SWZData)
    active_section: SWZSection = SWZSection.NONE
    current_agent: AgentRole = AgentRole.ORCHESTRATOR
    waiting_for_user: bool = False

    def add_message(self, role: AgentRole, content: str, metadata: Dict[str, Any] = None, to_render: bool = False):
        self.history.append(Message(
            role=role, 
            content=content, 
            metadata=metadata or {},
            to_render=to_render
        ))
