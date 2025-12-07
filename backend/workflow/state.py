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

    def _val(self, value, placeholder="...............") -> str:
        """Zwraca wartość lub placeholder jeśli brak danych"""
        if value is None or value == "" or value == []:
            return placeholder
        return str(value)

    def generate_markdown(self) -> str:
        """Generuje markdown SWZ - zawsze pokazuje pełny szablon z placeholderami dla brakujących danych"""
        md_parts = []
        placeholder = "..............."
        
        # Nagłówek dokumentu
        md_parts.append("# SPECYFIKACJA WARUNKÓW ZAMÓWIENIA (SWZ)")
        md_parts.append("")
        
        # ============================================
        # Sekcja I: DANE ZAMAWIAJĄCEGO
        # ============================================
        md_parts.append("## I. DANE ZAMAWIAJĄCEGO")
        md_parts.append("")
        md_parts.append(f"**Nazwa zamawiającego:** {self._val(self.organization_name)}")
        md_parts.append(f"**Adres:** {self._val(self.address)}")
        md_parts.append(f"**NIP:** {self._val(self.nip)}")
        md_parts.append(f"**REGON:** {self._val(self.regon)}")
        md_parts.append(f"**Email:** {self._val(self.contact_email)}")
        md_parts.append(f"**Telefon:** {self._val(self.phone)}")
        md_parts.append(f"**Strona internetowa:** {self._val(self.website, '(opcjonalnie)')}")
        md_parts.append(f"**Osoba odpowiedzialna:** {self._val(self.person_responsible)}")
        md_parts.append("")
        
        # ============================================
        # Sekcja II: TRYB UDZIELENIA ZAMÓWIENIA I PRZEDMIOT
        # ============================================
        md_parts.append("## II. TRYB UDZIELENIA ZAMÓWIENIA I PRZEDMIOT")
        md_parts.append("")
        md_parts.append(f"**Tryb postępowania:** {self._val(self.procurement_mode)}")
        md_parts.append(f"**Podstawa prawna:** {self._val(self.legal_basis)}")
        md_parts.append(f"**Nazwa zamówienia:** {self._val(self.procurement_title)}")
        md_parts.append(f"**Numer referencyjny:** {self._val(self.procurement_id)}")
        cpv_display = ', '.join(self.cpv_codes) if self.cpv_codes else placeholder
        md_parts.append(f"**Kody CPV:** {cpv_display}")
        md_parts.append(f"**Rodzaj zamówienia:** {self._val(self.procurement_type, '(dostawy/usługi/roboty budowlane)')}")
        md_parts.append("")
        md_parts.append(f"**Opis przedmiotu zamówienia:**")
        md_parts.append("")
        md_parts.append(self._val(self.description, "_Opis przedmiotu zamówienia zostanie uzupełniony..._"))
        md_parts.append("")
        
        # ============================================
        # Sekcja III: TERMINY
        # ============================================
        md_parts.append("## III. TERMINY")
        md_parts.append("")
        md_parts.append(f"**Termin wykonania zamówienia:** {self._val(self.execution_deadline)}")
        variants_text = "Dopuszczone" if self.variants_allowed else "Niedopuszczone"
        md_parts.append(f"**Oferty wariantowe:** {variants_text}")
        md_parts.append(f"**Termin składania ofert:** {self._val(self.submission_deadline)}")
        md_parts.append(f"**Termin otwarcia ofert:** {self._val(self.opening_date)}")
        md_parts.append(f"**Termin związania ofertą:** {self._val(self.binding_period)}")
        md_parts.append("")
        
        # ============================================
        # Sekcja IV: KRYTERIA OCENY OFERT
        # ============================================
        md_parts.append("## IV. KRYTERIA OCENY OFERT")
        md_parts.append("")
        md_parts.append("**Kryteria:**")
        if self.criteria:
            for criterion in self.criteria:
                name = criterion.get("name", "")
                weight = criterion.get("weight", "")
                md_parts.append(f"- {name}: {weight}%")
        else:
            md_parts.append(f"- Cena: {placeholder}%")
            md_parts.append(f"- {placeholder}: {placeholder}%")
        md_parts.append("")
        md_parts.append(f"**Budżet:** {self._val(self.budget, placeholder)} PLN")
        md_parts.append("")
        md_parts.append("**Cechy jakościowe:**")
        if self.quality_features:
            for feature in self.quality_features:
                md_parts.append(f"- {feature}")
        else:
            md_parts.append(f"- {placeholder}")
        md_parts.append("")
        
        # ============================================
        # Sekcja V: WARUNKI UDZIAŁU I WYKLUCZENIA
        # ============================================
        md_parts.append("## V. WARUNKI UDZIAŁU I WYKLUCZENIA")
        md_parts.append("")
        md_parts.append("**Obligatoryjne podstawy wykluczenia (art. 108 PZP):**")
        if self.exclusion_grounds_mandatory:
            for ground in self.exclusion_grounds_mandatory:
                md_parts.append(f"- {ground}")
        else:
            md_parts.append("- _Zgodnie z art. 108 ust. 1 ustawy PZP_")
        md_parts.append("")
        md_parts.append("**Fakultatywne podstawy wykluczenia (art. 109 PZP):**")
        if self.exclusion_grounds_optional:
            for ground in self.exclusion_grounds_optional:
                md_parts.append(f"- {ground}")
        else:
            md_parts.append(f"- {placeholder}")
        md_parts.append("")
        md_parts.append("**Warunki udziału w postępowaniu:**")
        if self.participation_conditions:
            for condition in self.participation_conditions:
                md_parts.append(f"- {condition}")
        else:
            md_parts.append(f"- Zdolność do występowania w obrocie gospodarczym: {placeholder}")
            md_parts.append(f"- Uprawnienia do prowadzenia działalności: {placeholder}")
            md_parts.append(f"- Sytuacja ekonomiczna lub finansowa: {placeholder}")
            md_parts.append(f"- Zdolność techniczna lub zawodowa: {placeholder}")
        md_parts.append("")
        md_parts.append("**Wymagane dokumenty:**")
        if self.required_documents:
            for doc in self.required_documents:
                md_parts.append(f"- {doc}")
        else:
            md_parts.append(f"- {placeholder}")
        md_parts.append("")
        
        # ============================================
        # Sekcja VI: WARUNKI UMOWY I ŚRODKI OCHRONY PRAWNEJ
        # ============================================
        md_parts.append("## VI. WARUNKI UMOWY I ŚRODKI OCHRONY PRAWNEJ")
        md_parts.append("")
        md_parts.append("**Istotne postanowienia umowy:**")
        if self.contract_terms:
            for term in self.contract_terms:
                md_parts.append(f"- {term}")
        else:
            md_parts.append(f"- {placeholder}")
        md_parts.append("")
        md_parts.append("**Środki ochrony prawnej:**")
        md_parts.append("")
        if self.legal_protection_info:
            md_parts.append(self.legal_protection_info)
        else:
            md_parts.append("_Wykonawcom przysługują środki ochrony prawnej określone w Dziale IX ustawy PZP._")
        md_parts.append("")
        
        # ============================================
        # Sekcja VII: KOMUNIKACJA I PROCEDURA
        # ============================================
        md_parts.append("## VII. KOMUNIKACJA I PROCEDURA")
        md_parts.append("")
        md_parts.append("**Zasady komunikacji:**")
        md_parts.append("")
        if self.communication_rules:
            md_parts.append(self.communication_rules)
        else:
            md_parts.append(f"_Komunikacja między zamawiającym a wykonawcami odbywa się: {placeholder}_")
        md_parts.append("")
        md_parts.append("**Procedura oceny ofert:**")
        md_parts.append("")
        if self.evaluation_procedure:
            md_parts.append(self.evaluation_procedure)
        else:
            md_parts.append("_Procedura oceny ofert zostanie określona..._")
        md_parts.append("")
        
        # ============================================
        # Sekcja VIII: DODATKOWE WYMAGANIA
        # ============================================
        md_parts.append("## VIII. DODATKOWE WYMAGANIA")
        md_parts.append("")
        md_parts.append("**Zasady dla konsorcjów:**")
        md_parts.append("")
        if self.consortium_rules:
            md_parts.append(self.consortium_rules)
        else:
            md_parts.append(f"_{placeholder}_")
        md_parts.append("")
        md_parts.append("**Zasady podwykonawstwa:**")
        md_parts.append("")
        if self.subcontracting_rules:
            md_parts.append(self.subcontracting_rules)
        else:
            md_parts.append(f"_{placeholder}_")
        md_parts.append("")
        md_parts.append("**Części zamówienia:**")
        if self.lots:
            for lot in self.lots:
                md_parts.append(f"- {lot.get('name', lot)}")
        else:
            md_parts.append(f"- {placeholder}")
        md_parts.append("")
        md_parts.append(f"**Wymagania dot. zatrudnienia:** {self._val(self.employment_requirements, placeholder)}")
        md_parts.append("")
        md_parts.append(f"**Klauzule społeczne:** {self._val(self.social_clauses, placeholder)}")
        md_parts.append("")
        md_parts.append(f"**Warunki gwarancji:** {self._val(self.warranty_terms, placeholder)}")
        md_parts.append("")
        md_parts.append(f"**Wymagania specjalne:** {self._val(self.special_requirements, placeholder)}")
        md_parts.append("")
        
        # ============================================
        # Sekcja IX: ZAŁĄCZNIKI
        # ============================================
        md_parts.append("## IX. ZAŁĄCZNIKI")
        md_parts.append("")
        md_parts.append("1. Formularz ofertowy")
        md_parts.append("2. Oświadczenie o braku podstaw wykluczenia")
        md_parts.append("3. Oświadczenie o spełnianiu warunków udziału")
        md_parts.append("4. Projekt umowy")
        md_parts.append(f"5. {placeholder}")
        md_parts.append("")
        
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
