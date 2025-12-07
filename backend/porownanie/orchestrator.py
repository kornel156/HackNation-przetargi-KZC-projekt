import os
import logging
from typing import List
from .agents.parser_agent import ParserAgent
from .agents.validator_agent import ValidatorAgent
from .agents.scorer_agent import ScorerAgent
from .agents.compliance_agent import ComplianceAgent
from .agents.reporter_agent import ReporterAgent
from .models import SWZData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.parser = ParserAgent()
        self.validator = ValidatorAgent()
        self.scorer = ScorerAgent()
        self.compliance = ComplianceAgent()
        self.reporter = ReporterAgent(output_dir)

    def run(self):
        logger.info("Starting Orchestrator...")
        
        # 1. Load Files
        pdf_files = [f for f in os.listdir(self.input_dir) if f.lower().endswith('.pdf')]
        # Filter out SWZ itself if possible (assuming SWZ is '61cOU.pdf' and offers are others)
        # But wait, the prompt says "analyze SWZ and offers". 
        # For now, let's treat 'formularz...' as the offer.
        
        offer_files = [f for f in pdf_files if "formularz" in f.lower() or "oferta" in f.lower()]
        
        offers = []
        for f in offer_files:
            path = os.path.join(self.input_dir, f)
            try:
                logger.info(f"Parsing {f}...")
                offer = self.parser.parse_pdf(path)
                offers.append(offer)
            except Exception as e:
                logger.error(f"Failed to parse {f}: {e}")

        if not offers:
            logger.warning("No offers found to process.")
            return

        # 2. Validation
        validations = []
        # Define SWZ Parameters (Hardcoded for now or parsed from SWZ file in future)
        swz_params = SWZData() 
        
        valid_offers = []
        for offer in offers:
            logger.info(f"Validating {offer.offer_id}...")
            res = self.validator.validate_offer(offer, swz=swz_params)
            validations.append(res)
            # We keep all offers for reporting, even failed ones?
            # Let's say we only score passed/warning ones.
            if res.overall_status != "FAILED":
                valid_offers.append(offer)
            else:
                 # Depending on strictness. Let's include them in scoring list but they might get 0.
                 valid_offers.append(offer) 

        # 3. Scoring
        logger.info("Scoring offers...")
        scoring_results = self.scorer.score_offers(valid_offers, swz=swz_params)

        # 4. Compliance
        compliance_reports = []
        for offer in valid_offers:
            logger.info(f"Checking compliance for {offer.offer_id}...")
            comp = self.compliance.check_compliance(offer)
            compliance_reports.append(comp)

        # 5. Reporting
        logger.info("Generating report...")
        report_path = self.reporter.generate_report(offers, validations, scoring_results, compliance_reports)
        logger.info(f"Report generated at {report_path}")

        return report_path
