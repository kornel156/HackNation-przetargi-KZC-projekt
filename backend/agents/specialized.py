from agents.base_agent import BaseAgent
from workflow.state import AgentRole, WorkflowState, SWZSection
from agents.prompts import *
import json

class SpecializedAgent(BaseAgent):
    def __init__(self, role: AgentRole, section: SWZSection, system_prompt: str):
        super().__init__(role=role)
        self.section = section
        self.system_prompt = system_prompt

    def get_system_instruction(self) -> str:
        return self.system_prompt

    async def process(self, state: WorkflowState, user_input: str) -> str:
        # We inject the current SWZ data into the prompt
        swz_context = f"Current SWZ Data: {state.swz_data.model_dump_json()}"
        
        # Add history
        history_str = "Conversation History:\n"
        for msg in state.history[-5:]:
             history_str += f"{msg.role.value}: {msg.content}\n"
        
        prompt = f"""
        {self.get_system_instruction()}
        
        {swz_context}
        
        {history_str}
        
        User Input: {user_input}
        
        Follow the instructions in the system prompt above.
        """
        
        print(f"DEBUG: Prompt for {self.role}:\n{prompt[:500]}...\n[...]\n{prompt[-500:]}")
        response = self.model.generate_content(prompt).text
        
        # Try to parse as JSON
        try:
            # Clean up json block if present
            clean_response = response
            if "```json" in response:
                clean_response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                clean_response = response.split("```")[1].split("```")[0]
            
            data = json.loads(clean_response.strip())
            
            # Extract message to user
            user_message = data.get("message", "")
            
            if "section_complete" in data and data["section_complete"]:
                # Update SWZ Data with extracted values
                if "extracted_data" in data:
                    for key, value in data["extracted_data"].items():
                        if hasattr(state.swz_data, key):
                            setattr(state.swz_data, key, value)
                
                # Return template content prefixed with SECTION_COMPLETE
                if "template_content" in data:
                    return f"SECTION_COMPLETE:{data['template_content']}"
            
            # If not complete, return the message to user
            if user_message:
                return user_message
            
            # Fallback if no message but valid JSON (shouldn't happen with good prompts)
            return str(data)
                    
        except json.JSONDecodeError:
            print(f"DEBUG: JSON Parse Error. Raw response: {response}")
            # If parsing fails, treat the whole response as a message to the user
            return response

# --- PHASE 1: BASIC DATA ---
class AgentDaneZamawiajacego(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_DANE_ZAMAWIAJACEGO, SWZSection.I_BASIC_DATA, AGENT_DANE_ZAMAWIAJACEGO_PROMPT)

# --- PHASE 2: MODE & SUBJECT ---
class AgentTrybPodstawa(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_TRYB_PODSTAWA, SWZSection.IV_PROCEDURE, AGENT_TRYB_PODSTAWA_PROMPT)

class AgentNazwaReferencja(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_NAZWA_REFERENCJA, SWZSection.II_SUBJECT, AGENT_NAZWA_REFERENCJA_PROMPT)

class AgentTypPrzedmiot(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_TYP_PRZEDMIOT, SWZSection.II_SUBJECT, AGENT_TYP_PRZEDMIOT_PROMPT)

# --- PHASE 3: DATES & VARIANTS ---
class AgentTerminWykonania(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_TERMIN_WYKONANIA, SWZSection.IV_PROCEDURE, AGENT_TERMIN_WYKONANIA_PROMPT)

class AgentWarianty(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_WARIANTY, SWZSection.II_SUBJECT, AGENT_WARIANTY_PROMPT)

class AgentTerminySkladania(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_TERMINY_SKLADANIA, SWZSection.IV_PROCEDURE, AGENT_TERMINY_SKLADANIA_PROMPT)

class AgentOtwarcieOfert(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_OTWARCIE_OFERT, SWZSection.IV_PROCEDURE, AGENT_OTWARCIE_OFERT_PROMPT)

class AgentTerminZwiazania(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_TERMIN_ZWIAZANIA, SWZSection.IV_PROCEDURE, AGENT_TERMIN_ZWIAZANIA_PROMPT)

# --- PHASE 4: CRITERIA & QUALITY ---
class AgentKryteriaOceny(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_KRYTERIA_OCENY, SWZSection.VII_CRITERIA, AGENT_KRYTERIA_OCENY_PROMPT)

class AgentCenaKryterium(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_CENA_KRYTERIUM, SWZSection.VII_CRITERIA, AGENT_CENA_KRYTERIUM_PROMPT)

class AgentCechyJakosciowe(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_CECHY_JAKOSCIOWE, SWZSection.II_SUBJECT, AGENT_CECHY_JAKOSCIOWE_PROMPT)

# --- PHASE 5: EXCLUSIONS & CONDITIONS ---
class AgentWykluczeniaObowiazkowe(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_WYKLUCZENIA_OBOWIAZKOWE, SWZSection.III_EXCLUSION, AGENT_WYKLUCZENIA_OBOWIAZKOWE_PROMPT)

class AgentWykluczeniaFakultatywne(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_WYKLUCZENIA_FAKULTATYWNE, SWZSection.III_EXCLUSION, AGENT_WYKLUCZENIA_FAKULTATYWNE_PROMPT)

class AgentWarunkiUdzialu(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_WARUNKI_UDZIALU, SWZSection.III_EXCLUSION, AGENT_WARUNKI_UDZIALU_PROMPT)

class AgentDokumentySrodki(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_DOKUMENTY_SRODKI, SWZSection.V_DOCUMENTS, AGENT_DOKUMENTY_SRODKI_PROMPT)

# --- PHASE 6: CONTRACT & LEGAL ---
class AgentUmowaProjektowana(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_UMOWA_PROJEKTOWANA, SWZSection.NONE, AGENT_UMOWA_PROJEKTOWANA_PROMPT)

class AgentSrodkiOchrony(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_SRODKI_OCHRONY, SWZSection.NONE, AGENT_SRODKI_OCHRONY_PROMPT)

# --- PHASE 7: COMMUNICATION & PROCEDURE ---
class AgentKomunikacjaElektroniczna(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_KOMUNIKACJA_ELEKTRONICZNA, SWZSection.VI_COMMUNICATION, AGENT_KOMUNIKACJA_ELEKTRONICZNA_PROMPT)

class AgentProceduraOceny(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_PROCEDURA_OCENY, SWZSection.IV_PROCEDURE, AGENT_PROCEDURA_OCENY_PROMPT)

# --- PHASE 8: ADVANCED/OPTIONAL ---
class AgentKonsorcjaPodwykonawcy(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_KONSORCJA_PODWYKONAWCY, SWZSection.III_EXCLUSION, AGENT_KONSORCJA_PODWYKONAWCY_PROMPT)

class AgentCzesciZamowienia(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_CZESCI_ZAMOWIENIA, SWZSection.II_SUBJECT, AGENT_CZESCI_ZAMOWIENIA_PROMPT)

class AgentWymogiZatrudnienia(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_WYMOGI_ZATRUDNIENIA, SWZSection.NONE, AGENT_WYMOGI_ZATRUDNIENIA_PROMPT)

class AgentKlauzuleSpoleczne(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_KLAUZULE_SPOLECZNE, SWZSection.NONE, AGENT_KLAUZULE_SPOLECZNE_PROMPT)

class AgentGwarancjaSerwis(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_GWARANCJA_SERWIS, SWZSection.II_SUBJECT, AGENT_GWARANCJA_SERWIS_PROMPT)

class AgentWymaganiaSpecjalne(SpecializedAgent):
    def __init__(self):
        super().__init__(AgentRole.AGENT_WYMAGANIA_SPECJALNE, SWZSection.II_SUBJECT, AGENT_WYMAGANIA_SPECJALNE_PROMPT)

# Legacy Aliases
BasicDataAgent = AgentDaneZamawiajacego
SubjectAgent = AgentTypPrzedmiot
CriteriaAgent = AgentKryteriaOceny
