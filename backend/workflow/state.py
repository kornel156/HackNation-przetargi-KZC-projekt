from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import time

class AgentRole(str, Enum):
    USER = "User"
    ORCHESTRATOR = "Orchestrator"
    
    # Specialized Agents
    AGENT_DANE_ZAMAWIAJACEGO = "Agent_Dane_Zamawiajacego"
    AGENT_TRYB_PODSTAWA = "Agent_Tryb_Podstawa"
    AGENT_NAZWA_REFERENCJA = "Agent_Nazwa_Referencja"
    AGENT_TYP_PRZEDMIOT = "Agent_Typ_Przedmiot"
    AGENT_TERMIN_WYKONANIA = "Agent_Termin_Wykonania"
    AGENT_WARIANTY = "Agent_Warianty"
    AGENT_TERMINY_SKLADANIA = "Agent_Terminy_Skladania"
    AGENT_OTWARCIE_OFERT = "Agent_Otwarcie_Ofert"
    AGENT_TERMIN_ZWIAZANIA = "Agent_Termin_Zwiazania"
    AGENT_KRYTERIA_OCENY = "Agent_Kryteria_Oceny"
    AGENT_CENA_KRYTERIUM = "Agent_Cena_Kryterium"
    AGENT_CECHY_JAKOSCIOWE = "Agent_Cechy_Jakosciowe"
    AGENT_WYKLUCZENIA_OBOWIAZKOWE = "Agent_Wykluczenia_Obowiazkowe"
    AGENT_WYKLUCZENIA_FAKULTATYWNE = "Agent_Wykluczenia_Fakultatywne"
    AGENT_WARUNKI_UDZIALU = "Agent_Warunki_Udzialu"
    AGENT_DOKUMENTY_SRODKI = "Agent_Dokumenty_Srodki"
    AGENT_UMOWA_PROJEKTOWANA = "Agent_Umowa_Projektowana"
    AGENT_SRODKI_OCHRONY = "Agent_Srodki_Ochrony"
    AGENT_KOMUNIKACJA_ELEKTRONICZNA = "Agent_Komunikacja_Elektroniczna"
    AGENT_PROCEDURA_OCENY = "Agent_Procedura_Oceny"
    AGENT_KONSORCJA_PODWYKONAWCY = "Agent_Konsorcja_Podwykonawcy"
    AGENT_CZESCI_ZAMOWIENIA = "Agent_Czesci_Zamowienia"
    AGENT_WYMOGI_ZATRUDNIENIA = "Agent_Wymogi_Zatrudnienia"
    AGENT_KLAUZULE_SPOLECZNE = "Agent_Klauzule_Spoleczne"
    AGENT_GWARANCJA_SERWIS = "Agent_Gwarancja_Serwis"
    AGENT_WYMAGANIA_SPECJALNE = "Agent_Wymagania_Specjalne"
    
    # Supporting Agents
    AGENT_WALIDACJA_GLOWNA = "Agent_Walidacja_Glowna"
    AGENT_FORMATOWANIE = "Agent_Formatowanie"
    AGENT_ZGODNOSC_PZP = "Agent_Zgodnosc_Pzp"
    AGENT_ZALACZNIKI = "Agent_Zalaczniki"
    AGENT_ANALIZA_KOMUNIKACJI = "Agent_Analiza_Komunikacji"
    
    # Legacy/Fallback (optional, can keep for compatibility or remove)
    LEGAL_RESEARCHER = "Legal Researcher"
    BASIC_DATA_AGENT = "Basic Data Agent" # Mapping to AGENT_DANE_ZAMAWIAJACEGO
    SUBJECT_AGENT = "Subject Agent" # Mapping to AGENT_TYP_PRZEDMIOT
    CRITERIA_AGENT = "Criteria Agent" # Mapping to AGENT_KRYTERIA_OCENY

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
    # --- PHASE 1: BASIC DATA (Agent_Dane_Zamawiajacego) ---
    organization_name: Optional[str] = None
    address: Optional[str] = None
    nip: Optional[str] = None
    regon: Optional[str] = None
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    person_responsible: Optional[str] = None
    
    # --- PHASE 2: MODE & SUBJECT (Agent_Tryb_Podstawa, Agent_Nazwa_Referencja, Agent_Typ_Przedmiot) ---
    procurement_mode: Optional[str] = None
    legal_basis: Optional[str] = None
    procurement_title: Optional[str] = None
    procurement_id: Optional[str] = None
    cpv_codes: List[str] = Field(default_factory=list)
    procurement_type: Optional[str] = None # dostawy/usługi/roboty
    description: Optional[str] = None
    
    # --- PHASE 3: DATES & VARIANTS (Agent_Termin_Wykonania, Agent_Warianty, Agent_Terminy_Skladania, Agent_Otwarcie_Ofert, Agent_Termin_Zwiazania) ---
    execution_deadline: Optional[str] = None
    variants_allowed: bool = False
    submission_deadline: Optional[str] = None
    opening_date: Optional[str] = None
    binding_period: Optional[str] = None
    
    # --- PHASE 4: CRITERIA & QUALITY (Agent_Kryteria_Oceny, Agent_Cena_Kryterium, Agent_Cechy_Jakosciowe) ---
    criteria: List[Dict[str, Any]] = Field(default_factory=list) # e.g. {"name": "Price", "weight": 60}
    budget: Optional[float] = None
    quality_features: List[str] = Field(default_factory=list)
    
    # --- PHASE 5: EXCLUSIONS & CONDITIONS (Agent_Wykluczenia_Obowiazkowe, Agent_Wykluczenia_Fakultatywne, Agent_Warunki_Udzialu, Agent_Dokumenty_Srodki) ---
    exclusion_grounds_mandatory: List[str] = Field(default_factory=list)
    exclusion_grounds_optional: List[str] = Field(default_factory=list)
    participation_conditions: List[str] = Field(default_factory=list)
    required_documents: List[str] = Field(default_factory=list)
    
    # --- PHASE 6: CONTRACT & LEGAL (Agent_Umowa_Projektowana, Agent_Srodki_Ochrony) ---
    contract_terms: List[str] = Field(default_factory=list)
    legal_protection_info: Optional[str] = None
    
    # --- PHASE 7: COMMUNICATION & PROCEDURE (Agent_Komunikacja_Elektroniczna, Agent_Procedura_Oceny) ---
    communication_rules: Optional[str] = None
    evaluation_procedure: Optional[str] = None
    
    # --- PHASE 8: ADVANCED/OPTIONAL (Agent_Konsorcja_Podwykonawcy, Agent_Czesci_Zamowienia, Agent_Wymogi_Zatrudnienia, Agent_Klauzule_Spoleczne, Agent_Gwarancja_Serwis, Agent_Wymagania_Specjalne) ---
    consortium_rules: Optional[str] = None
    subcontracting_rules: Optional[str] = None
    lots: List[Dict[str, Any]] = Field(default_factory=list) # Parts of the order
    employment_requirements: Optional[str] = None
    social_clauses: Optional[str] = None
    warranty_terms: Optional[str] = None
    special_requirements: Optional[str] = None

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
