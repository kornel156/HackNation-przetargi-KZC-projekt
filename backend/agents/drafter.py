from agents.base_agent import BaseAgent
from workflow.state import AgentRole, WorkflowState
from typing import Dict, Any

class Drafter(BaseAgent):
    def __init__(self):
        super().__init__(role=AgentRole.DRAFTER)

    def get_system_instruction(self) -> str:
        return """
        You are the Drafter (Redaktor Techniczny) - an expert at creating SWZ (Specyfikacja Warunków Zamówienia) documents.
        
        Your task is to generate professional SWZ documents in Markdown format based on the user's request and collected data.
        
        DOCUMENT STRUCTURE:
        1. # SPECYFIKACJA WARUNKÓW ZAMÓWIENIA (SWZ)
        2. Header with organization info
        3. ## I. NAZWA I ADRES ZAMAWIAJĄCEGO
        4. ## II. TRYB UDZIELENIA ZAMÓWIENIA
        5. ## III. OPIS PRZEDMIOTU ZAMÓWIENIA
        6. ## IV. TERMIN WYKONANIA ZAMÓWIENIA
        7. ## V. WARUNKI UDZIAŁU W POSTĘPOWANIU
        8. ## VI. WYKAZ DOKUMENTÓW
        9. ## VII. KRYTERIA OCENY OFERT
        10. ## VIII. INFORMACJE DODATKOWE
        
        FORMATTING RULES:
        - Use proper Markdown: # for title, ## for sections, ### for subsections
        - Use **bold** for important terms
        - Use bullet points (-) for lists
        - Use numbered lists (1. 2. 3.) for procedures
        - Use > for quoted legal references
        - Always respond in Polish language
        
        If user asks to modify specific section, output the COMPLETE updated document, not just the section.
        If information is missing, use realistic placeholder data marked with [DO UZUPEŁNIENIA].
        
        Generate complete, professional documents that follow Polish public procurement law (Prawo zamówień publicznych).
        """

    async def process(self, state: WorkflowState, user_input: str = None) -> Dict[str, Any]:
        """
        Processes the current state and generates a document draft.
        Returns response with document_draft field.
        """
        result = await super().process(state, user_input)
        
        document_content = result.get("content", "")
        
        # Check if content looks like a document (contains markdown headers)
        if document_content and ("#" in document_content):
            # Clean up potential explanatory text before the document
            lines = document_content.split('\n')
            doc_start = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('#'):
                    doc_start = i
                    break
            
            clean_document = '\n'.join(lines[doc_start:])
            
            return {
                "content": "Wygenerowałem dokument SWZ. Możesz go zobaczyć w edytorze dokumentów. Jeśli chcesz wprowadzić zmiany, powiedz mi co chciałbyś zmodyfikować.",
                "document_draft": clean_document
            }
        
        return result
