import re
from typing import Optional
from pypdf import PdfReader
from ..models import Offer, SupplierData, FinancialData, TechnicalParams, Declaration

class ParserAgent:
    def __init__(self):
        pass

    def parse_pdf(self, file_path: str) -> Offer:
        """
        Extracts data from a PDF file and returns a structured Offer object.
        """
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        # Basic ID generation from filename
        import os
        filename = os.path.basename(file_path)
        offer_id = filename.split('.')[0]

        # Extract Fields using Regex
        supplier = self._extract_supplier(text)
        financial = self._extract_financial(text)
        technical = self._extract_technical(text)
        declarations = self._extract_declarations(text)

        return Offer(
            offer_id=offer_id,
            file_name=filename,
            supplier=supplier,
            financial=financial,
            technical=technical,
            declarations=declarations,
            raw_text_snippet=text[:500]
        )

    def _extract_supplier(self, text: str) -> SupplierData:
        # Improved NIP regex
        # Look for NIP followed immediately by digits or separated
        nip_match = re.search(r'NIP[:\s]*(\d{3}-\d{2}-\d{2}-\d{3})', text)
        if not nip_match:
             # Try without separator or with different dashes
             nip_match = re.search(r'NIP[:\s]*(\d{3}-\d{3}-\d{2}-\d{2})', text)
        if not nip_match:
             nip_match = re.search(r'NIP(\d{10}|\d{3}-\d{3}-\d{2}-\d{2})', text)
        
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        
        name = "Unknown Company"
        if "Wykonawca:" in text:
            parts = text.split("Wykonawca:", 1)
            if len(parts) > 1:
                name_line = parts[1].splitlines()[0].strip()
                if name_line:
                    name = name_line

        return SupplierData(
            name=name,
            nip=nip_match.group(1) if nip_match else None,
            email=email_match.group(0) if email_match else None
        )

    def _extract_financial(self, text: str) -> FinancialData:
        netto = 0.0
        vat = 0.0
        brutto = 0.0
        
        def parse_price(val):
            if not val: return 0.0
            val = val.replace(' ', '').replace(',', '.')
            try:
                return float(val)
            except:
                return 0.0

        # Regex for price with 'zł' or 'PLN' and optional colon
        # "brutto 150 000,00 zł"
        brutto_match = re.search(r'brutto[:\s]*([\d\s]+,\d{2})\s*(?:zł|PLN)', text, re.IGNORECASE)
        if brutto_match:
            brutto = parse_price(brutto_match.group(1))

        # "netto 121 951,22 zł"
        netto_match = re.search(r'netto[:\s]*([\d\s]+,\d{2})\s*(?:zł|PLN)', text, re.IGNORECASE)
        if netto_match:
            netto = parse_price(netto_match.group(1))

        # VAT "23%"
        vat_match = re.search(r'(\d{1,2})%', text)
        if vat_match:
            vat = float(vat_match.group(1))
        elif netto > 0 and brutto > 0:
            vat_calc = (brutto - netto) / netto * 100
            vat = round(vat_calc)
            
        return FinancialData(
            netto=netto,
            vat_rate=vat,
            brutto_stated=brutto,
            brutto_calculated=netto * (1 + vat/100) if netto else 0
        )

    def _extract_technical(self, text: str) -> TechnicalParams:
        # Guarantee
        guarantee = 0
        # "na okres 36\nmiesięcy"
        g_match = re.search(r'okres\s*(\d+)\s*mie', text, re.IGNORECASE)
        if not g_match:
             g_match = re.search(r'(\d+)\s*miesiące', text)
        if g_match:
            guarantee = int(g_match.group(1))
            
        # Delivery "do 3 miesięcy" -> need to handle "miesięcy" -> 30 days
        delivery = 0
        d_match = re.search(r'termin realizacji[:\s]*do\s*(\d+)\s*mies', text, re.IGNORECASE)
        if d_match:
            delivery = int(d_match.group(1)) * 30
        else:
             d_match = re.search(r'termin realizacji[:\s]*(\d+)\s*dni', text, re.IGNORECASE)
             if d_match:
                delivery = int(d_match.group(1))

        return TechnicalParams(
            guarantee_months=guarantee,
            delivery_days=delivery,
            payment_terms="30 days" 
        )

    def _extract_declarations(self, text: str) -> Declaration:
        read = "zapozna" in text.lower() and "zrozum" in text.lower()
        return Declaration(
            read_and_understood=read,
            accepts_without_reservations=True # Assumption for now
        )
