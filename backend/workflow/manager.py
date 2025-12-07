from typing import Dict, Any
import json
import logging
from workflow.state import WorkflowState, Message, AgentRole, SWZSection
from agents.orchestrator import Orchestrator
from agents.researcher import LegalResearcher
from agents.specialized import *
from agents.supporting import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowManager:
    def __init__(self):
        self.state = WorkflowState()
        self.agents = {}
        self._initialize_agents()

    def _initialize_agents(self):
        # Core Agents
        self.agents[AgentRole.ORCHESTRATOR] = Orchestrator()
        self.agents[AgentRole.LEGAL_RESEARCHER] = LegalResearcher()
        
        # Specialized Agents
        self.agents[AgentRole.AGENT_DANE_ZAMAWIAJACEGO] = AgentDaneZamawiajacego()
        self.agents[AgentRole.AGENT_TRYB_PODSTAWA] = AgentTrybPodstawa()
        self.agents[AgentRole.AGENT_NAZWA_REFERENCJA] = AgentNazwaReferencja()
        self.agents[AgentRole.AGENT_TYP_PRZEDMIOT] = AgentTypPrzedmiot()
        self.agents[AgentRole.AGENT_TERMIN_WYKONANIA] = AgentTerminWykonania()
        self.agents[AgentRole.AGENT_WARIANTY] = AgentWarianty()
        self.agents[AgentRole.AGENT_TERMINY_SKLADANIA] = AgentTerminySkladania()
        self.agents[AgentRole.AGENT_OTWARCIE_OFERT] = AgentOtwarcieOfert()
        self.agents[AgentRole.AGENT_TERMIN_ZWIAZANIA] = AgentTerminZwiazania()
        self.agents[AgentRole.AGENT_KRYTERIA_OCENY] = AgentKryteriaOceny()
        self.agents[AgentRole.AGENT_CENA_KRYTERIUM] = AgentCenaKryterium()
        self.agents[AgentRole.AGENT_CECHY_JAKOSCIOWE] = AgentCechyJakosciowe()
        self.agents[AgentRole.AGENT_WYKLUCZENIA_OBOWIAZKOWE] = AgentWykluczeniaObowiazkowe()
        self.agents[AgentRole.AGENT_WYKLUCZENIA_FAKULTATYWNE] = AgentWykluczeniaFakultatywne()
        self.agents[AgentRole.AGENT_WARUNKI_UDZIALU] = AgentWarunkiUdzialu()
        self.agents[AgentRole.AGENT_DOKUMENTY_SRODKI] = AgentDokumentySrodki()
        self.agents[AgentRole.AGENT_UMOWA_PROJEKTOWANA] = AgentUmowaProjektowana()
        self.agents[AgentRole.AGENT_SRODKI_OCHRONY] = AgentSrodkiOchrony()
        self.agents[AgentRole.AGENT_KOMUNIKACJA_ELEKTRONICZNA] = AgentKomunikacjaElektroniczna()
        self.agents[AgentRole.AGENT_PROCEDURA_OCENY] = AgentProceduraOceny()
        self.agents[AgentRole.AGENT_KONSORCJA_PODWYKONAWCY] = AgentKonsorcjaPodwykonawcy()
        self.agents[AgentRole.AGENT_CZESCI_ZAMOWIENIA] = AgentCzesciZamowienia()
        self.agents[AgentRole.AGENT_WYMOGI_ZATRUDNIENIA] = AgentWymogiZatrudnienia()
        self.agents[AgentRole.AGENT_KLAUZULE_SPOLECZNE] = AgentKlauzuleSpoleczne()
        self.agents[AgentRole.AGENT_GWARANCJA_SERWIS] = AgentGwarancjaSerwis()
        self.agents[AgentRole.AGENT_WYMAGANIA_SPECJALNE] = AgentWymaganiaSpecjalne()
        
        # Supporting Agents
        self.agents[AgentRole.AGENT_WALIDACJA_GLOWNA] = AgentWalidacjaGlowna()
        self.agents[AgentRole.AGENT_FORMATOWANIE] = AgentFormatowanie()
        self.agents[AgentRole.AGENT_ZGODNOSC_PZP] = AgentZgodnoscPzp()
        self.agents[AgentRole.AGENT_ZALACZNIKI] = AgentZalaczniki()
        self.agents[AgentRole.AGENT_ANALIZA_KOMUNIKACJI] = AgentAnalizaKomunikacji()

        # Legacy/Fallback mappings
        self.agents[AgentRole.BASIC_DATA_AGENT] = self.agents[AgentRole.AGENT_DANE_ZAMAWIAJACEGO]
        self.agents[AgentRole.SUBJECT_AGENT] = self.agents[AgentRole.AGENT_TYP_PRZEDMIOT]
        self.agents[AgentRole.CRITERIA_AGENT] = self.agents[AgentRole.AGENT_KRYTERIA_OCENY]

    async def process_user_input(self, user_input: str) -> Dict[str, Any]:
        # 1. Add user message to history
        self.state.add_message(role=AgentRole.USER, content=user_input)
        
        # 2. Orchestrator decides next step
        orchestrator = self.agents[AgentRole.ORCHESTRATOR]
        decision_json = await orchestrator.process(self.state, user_input)
        
        try:
            decision = json.loads(decision_json)
        except json.JSONDecodeError:
            # Fallback if JSON is malformed
            decision = {
                "next_agent": "Orchestrator",
                "active_section": "none",
                "response_to_user": "I encountered an error processing your request. Could you please repeat?"
            }

        next_agent_role_str = decision.get("next_agent", "Orchestrator")
        active_section_str = decision.get("active_section", "none")
        response_to_user = decision.get("response_to_user", "")

        # Update active section
        try:
            self.state.active_section = SWZSection(active_section_str)
        except ValueError:
            pass # Keep previous or default

        # 3. Route to Agent
        to_render = False
        final_response = response_to_user

        if next_agent_role_str == "Orchestrator":
            # Orchestrator handles it directly
            pass
        else:
            # specialized agent
            try:
                # Map string to enum if needed, or use string directly if keys match
                # Our keys are AgentRole enums, so we need to match the string value
                target_role = None
                for role in AgentRole:
                    if role.value == next_agent_role_str or role.name == next_agent_role_str:
                        target_role = role
                        break
                
                if target_role and target_role in self.agents:
                    agent = self.agents[target_role]
                    agent_response = await agent.process(self.state, user_input)
                    
                    # Check for completion
                    if "SECTION_COMPLETE:" in agent_response:
                        to_render = True
                        template_content = agent_response.replace("SECTION_COMPLETE:", "").strip()
                        
                        # Render the template with current data
                        try:
                            from jinja2 import Template
                            template = Template(template_content)
                            rendered_content = template.render(**self.state.swz_data.model_dump())
                            final_response = rendered_content
                            
                            # Store the template in the state (optional, for future editing)
                            # self.state.swz_data.sections[self.state.active_section] = template_content
                            
                        except Exception as e:
                            logger.error(f"Template rendering failed: {e}")
                            final_response = template_content # Fallback to raw template
                    else:
                        final_response = agent_response
                else:
                    final_response = f"Error: Agent {next_agent_role_str} not found."
            except Exception as e:
                final_response = f"Error executing agent {next_agent_role_str}: {str(e)}"

        # 4. Update State with Agent Response
        # We assume the last active agent is the one responding
        responder_role = AgentRole.ORCHESTRATOR
        if next_agent_role_str != "Orchestrator":
             for role in AgentRole:
                    if role.value == next_agent_role_str or role.name == next_agent_role_str:
                        responder_role = role
                        break

        self.state.add_message(role=responder_role, content=final_response, to_render=to_render)
        
        return {
            "response": final_response,
            "to_render": to_render,
            "active_section": self.state.active_section,
            "swz_data": self.state.swz_data.model_dump()
        }

    def get_state(self) -> Dict[str, Any]:
        return self.state.model_dump()
