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

    def generate_markdown(self) -> str:
        """Generuje markdown SWZ na podstawie aktualnych danych"""
        md_parts = []
        
        # Nagłówek dokumentu
        md_parts.append("# SPECYFIKACJA WARUNKÓW ZAMÓWIENIA (SWZ)")
        md_parts.append("")
        
        # Sekcja I: Dane Zamawiającego
        has_basic_data = any([
            self.organization_name, self.address, self.nip, 
            self.regon, self.contact_email, self.phone, 
            self.website, self.person_responsible
        ])
        
        if has_basic_data:
            md_parts.append("## I. DANE ZAMAWIAJĄCEGO")
            md_parts.append("")
            if self.organization_name:
                md_parts.append(f"**Nazwa zamawiającego:** {self.organization_name}")
            if self.address:
                md_parts.append(f"**Adres:** {self.address}")
            if self.nip:
                md_parts.append(f"**NIP:** {self.nip}")
            if self.regon:
                md_parts.append(f"**REGON:** {self.regon}")
            if self.contact_email:
                md_parts.append(f"**Email:** {self.contact_email}")
            if self.phone:
                md_parts.append(f"**Telefon:** {self.phone}")
            if self.website:
                md_parts.append(f"**Strona internetowa:** {self.website}")
            if self.person_responsible:
                md_parts.append(f"**Osoba odpowiedzialna:** {self.person_responsible}")
            md_parts.append("")
        
        # Sekcja II: Tryb i Przedmiot Zamówienia
        has_subject_data = any([
            self.procurement_mode, self.legal_basis, self.procurement_title,
            self.procurement_id, self.cpv_codes, self.procurement_type, self.description
        ])
        
        if has_subject_data:
            md_parts.append("## II. TRYB UDZIELENIA ZAMÓWIENIA I PRZEDMIOT")
            md_parts.append("")
            if self.procurement_mode:
                md_parts.append(f"**Tryb postępowania:** {self.procurement_mode}")
            if self.legal_basis:
                md_parts.append(f"**Podstawa prawna:** {self.legal_basis}")
            if self.procurement_title:
                md_parts.append(f"**Nazwa zamówienia:** {self.procurement_title}")
            if self.procurement_id:
                md_parts.append(f"**Numer referencyjny:** {self.procurement_id}")
            if self.cpv_codes:
                md_parts.append(f"**Kody CPV:** {', '.join(self.cpv_codes)}")
            if self.procurement_type:
                md_parts.append(f"**Rodzaj zamówienia:** {self.procurement_type}")
            if self.description:
                md_parts.append(f"\n**Opis przedmiotu zamówienia:**\n\n{self.description}")
            md_parts.append("")
        
        # Sekcja III: Terminy
        has_dates = any([
            self.execution_deadline, self.variants_allowed, 
            self.submission_deadline, self.opening_date, self.binding_period
        ])
        
        if has_dates:
            md_parts.append("## III. TERMINY")
            md_parts.append("")
            if self.execution_deadline:
                md_parts.append(f"**Termin wykonania zamówienia:** {self.execution_deadline}")
            md_parts.append(f"**Oferty wariantowe:** {'Dopuszczone' if self.variants_allowed else 'Niedopuszczone'}")
            if self.submission_deadline:
                md_parts.append(f"**Termin składania ofert:** {self.submission_deadline}")
            if self.opening_date:
                md_parts.append(f"**Termin otwarcia ofert:** {self.opening_date}")
            if self.binding_period:
                md_parts.append(f"**Termin związania ofertą:** {self.binding_period}")
            md_parts.append("")
        
        # Sekcja IV: Kryteria Oceny
        has_criteria = any([self.criteria, self.budget, self.quality_features])
        
        if has_criteria:
            md_parts.append("## IV. KRYTERIA OCENY OFERT")
            md_parts.append("")
            if self.criteria:
                md_parts.append("**Kryteria:**")
                for criterion in self.criteria:
                    name = criterion.get("name", "")
                    weight = criterion.get("weight", "")
                    md_parts.append(f"- {name}: {weight}%")
            if self.budget:
                md_parts.append(f"\n**Budżet:** {self.budget} PLN")
            if self.quality_features:
                md_parts.append("\n**Cechy jakościowe:**")
                for feature in self.quality_features:
                    md_parts.append(f"- {feature}")
            md_parts.append("")
        
        # Sekcja V: Wykluczenia i Warunki
        has_exclusions = any([
            self.exclusion_grounds_mandatory, self.exclusion_grounds_optional,
            self.participation_conditions, self.required_documents
        ])
        
        if has_exclusions:
            md_parts.append("## V. WARUNKI UDZIAŁU I WYKLUCZENIA")
            md_parts.append("")
            if self.exclusion_grounds_mandatory:
                md_parts.append("**Obligatoryjne podstawy wykluczenia:**")
                for ground in self.exclusion_grounds_mandatory:
                    md_parts.append(f"- {ground}")
            if self.exclusion_grounds_optional:
                md_parts.append("\n**Fakultatywne podstawy wykluczenia:**")
                for ground in self.exclusion_grounds_optional:
                    md_parts.append(f"- {ground}")
            if self.participation_conditions:
                md_parts.append("\n**Warunki udziału w postępowaniu:**")
                for condition in self.participation_conditions:
                    md_parts.append(f"- {condition}")
            if self.required_documents:
                md_parts.append("\n**Wymagane dokumenty:**")
                for doc in self.required_documents:
                    md_parts.append(f"- {doc}")
            md_parts.append("")
        
        # Sekcja VI: Umowa i Ochrona Prawna
        has_contract = any([self.contract_terms, self.legal_protection_info])
        
        if has_contract:
            md_parts.append("## VI. WARUNKI UMOWY I ŚRODKI OCHRONY PRAWNEJ")
            md_parts.append("")
            if self.contract_terms:
                md_parts.append("**Warunki umowy:**")
                for term in self.contract_terms:
                    md_parts.append(f"- {term}")
            if self.legal_protection_info:
                md_parts.append(f"\n**Środki ochrony prawnej:**\n\n{self.legal_protection_info}")
            md_parts.append("")
        
        # Sekcja VII: Komunikacja
        has_communication = any([self.communication_rules, self.evaluation_procedure])
        
        if has_communication:
            md_parts.append("## VII. KOMUNIKACJA I PROCEDURA")
            md_parts.append("")
            if self.communication_rules:
                md_parts.append(f"**Zasady komunikacji:**\n\n{self.communication_rules}")
            if self.evaluation_procedure:
                md_parts.append(f"\n**Procedura oceny:**\n\n{self.evaluation_procedure}")
            md_parts.append("")
        
        # Sekcja VIII: Dodatkowe Wymagania
        has_additional = any([
            self.consortium_rules, self.subcontracting_rules, self.lots,
            self.employment_requirements, self.social_clauses, 
            self.warranty_terms, self.special_requirements
        ])
        
        if has_additional:
            md_parts.append("## VIII. DODATKOWE WYMAGANIA")
            md_parts.append("")
            if self.consortium_rules:
                md_parts.append(f"**Zasady dla konsorcjów:**\n\n{self.consortium_rules}")
            if self.subcontracting_rules:
                md_parts.append(f"\n**Zasady podwykonawstwa:**\n\n{self.subcontracting_rules}")
            if self.lots:
                md_parts.append("\n**Części zamówienia:**")
                for lot in self.lots:
                    md_parts.append(f"- {lot.get('name', lot)}")
            if self.employment_requirements:
                md_parts.append(f"\n**Wymagania zatrudnienia:**\n\n{self.employment_requirements}")
            if self.social_clauses:
                md_parts.append(f"\n**Klauzule społeczne:**\n\n{self.social_clauses}")
            if self.warranty_terms:
                md_parts.append(f"\n**Warunki gwarancji:**\n\n{self.warranty_terms}")
            if self.special_requirements:
                md_parts.append(f"\n**Wymagania specjalne:**\n\n{self.special_requirements}")
            md_parts.append("")
        
        # Jeśli nie ma żadnych danych, dodaj placeholder
        if not any([has_basic_data, has_subject_data, has_dates, has_criteria, 
                    has_exclusions, has_contract, has_communication, has_additional]):
            md_parts.append("*Rozpocznij rozmowę z asystentem, aby uzupełnić dane dokumentu SWZ.*")
        
        return "\n".join(md_parts)

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
