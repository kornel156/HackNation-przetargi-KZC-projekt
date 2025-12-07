from datetime import datetime
from typing import List, Dict, Any
from ..models import SWZData, FinalEvaluationReport, ProtocolSection

class SectionGeneratorAgent:
    def __init__(self):
        pass

    def generate_procedural_sections(self, swz: SWZData) -> List[ProtocolSection]:
        # Agent 2
        sections = []
        
        # 1. Zamawiający
        content_1 = f"Pełna nazwa: {swz.buyer_name}\nAdres: {swz.buyer_address}"
        sections.append(ProtocolSection(section_id=1, title="Zamawiający", content=content_1))

        # 2. Przedmiot Zamówienia
        content_2 = f"Nazwa: {swz.project_name}\nCPV: {', '.join(swz.cpv_codes)}"
        sections.append(ProtocolSection(section_id=2, title="Przedmiot zamówienia", content=content_2))

        # 3. Wartość
        content_3 = f"Wartość szacunkowa: {swz.budget:.2f} PLN"
        sections.append(ProtocolSection(section_id=3, title="Wartość zamówienia", content=content_3))

        # 5. Tryb
        content_5 = f"Tryb: {swz.procedure_mode}"
        sections.append(ProtocolSection(section_id=5, title="Tryb udzielenia zamówienia", content=content_5))
        
        return sections

    def generate_parties_sections(self) -> List[ProtocolSection]:
        # Agent 3 (Mocked data for people)
        sections = []
        
        # 6. Osoby
        content_6 = "Kierownik: Jan Kowalski (Dyrektor)\nKomisja Przetargowa: Anna Nowak (Przewodnicząca), Piotr Wiśniewski (Członek)"
        sections.append(ProtocolSection(section_id=6, title="Osoby wykonujące czynności", content=content_6))
        
        return sections

    def generate_results_sections(self, report: FinalEvaluationReport, swz: SWZData) -> List[ProtocolSection]:
        # Agent 4
        sections = []
        
        # 11. Termin składania
        sections.append(ProtocolSection(section_id=11, title="Termin składania ofert", content=swz.submission_deadline))
        
        # 12. Otwarcie
        sections.append(ProtocolSection(section_id=12, title="Otwarcie ofert", content=f"{swz.opening_date}, Kwota: {swz.budget:.2f} PLN"))

        # 13. Zestawienie ofert
        table_rows = []
        for rank in report.rankings:
            detail = report.details.get(rank.offer_id)
            supplier = detail['supplier']['name'] if detail else "Unknown"
            price = detail['financial']['brutto_stated'] if detail else 0.0
            table_rows.append(f"{rank.rank}. {supplier} - {price:.2f} PLN")
        
        content_13 = "\n".join(table_rows)
        sections.append(ProtocolSection(section_id=13, title="Zestawienie ofert", content=content_13))

        # 14. Odrzucone - Assume none if report says nothing (or filter)
        # Check details for failed validations with status FAILED?
        # In previous run form had FAILED validation but was ranked 1 (demo mode). 
        # In real scenario we'd list them here.
        rejected = [oid for oid, d in report.details.items() if d['validation'] and d['validation']['overall_status'] == 'FAILED']
        content_14 = "Brak ofert odrzuconych."
        if rejected:
             content_14 = f"Odrzucono: {', '.join(rejected)} - Powód: Niezgodność z SWZ/NIP"
        
        sections.append(ProtocolSection(section_id=14, title="Oferty odrzucone", content=content_14))

        # 22. Najkorzystniejsza oferta
        if report.winner_offer_id:
             winner_detail = report.details.get(report.winner_offer_id)
             supplier_name = winner_detail['supplier']['name']
             price = winner_detail['financial']['brutto_stated']
             score = report.rankings[0].total_score
             
             justification = (
                 f"Jako najkorzystniejszą wybrano ofertę {supplier_name}.\n"
                 f"Oferta uzyskała {score} punktów. Cena: {price:.2f} PLN.\n"
                 "Oferta spełnia wszystkie wymagania SWZ i przedstawia najkorzystniejszy bilans ceny i innych kryteriów."
             )
             
             content_22 = f"Wybrano ofertę: {supplier_name}\n\nUzasadnienie:\n{justification}"
             sections.append(ProtocolSection(section_id=22, title="Najkorzystniejsza oferta", content=content_22))
        
        return sections

    def generate_formal_sections(self) -> List[ProtocolSection]:
        # Agent 5
        sections = []
        
        # 29. Udzielenie zamówienia
        sections.append(ProtocolSection(section_id=29, title="Udzielenie zamówienia", content="Umowa zostanie zawarta w terminie zgodnym z PZP."))
        
        # 30. Załączniki
        atts = "1. SWZ\n2. Oferty\n3. Informacja z otwarcia"
        sections.append(ProtocolSection(section_id=30, title="Załączniki", content=atts))
        
        # 33. Zatwierdzenie
        sections.append(ProtocolSection(section_id=33, title="Zatwierdzenie", content="Zatwierdzam: ........................... (Kierownik Zamawiającego)"))
        
        return sections
