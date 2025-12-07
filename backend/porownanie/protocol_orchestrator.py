import os
import logging
import json
from datetime import datetime
from porownanie.models import FinalEvaluationReport, SWZData
from porownanie.agents.protocol_data_agent import ProtocolDataAgent
from porownanie.agents.section_generators import SectionGeneratorAgent
from porownanie.agents.document_builder_agent import DocumentBuilderAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProtocolOrchestrator:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.data_agent = ProtocolDataAgent()
        self.section_agent = SectionGeneratorAgent()
        
        template_path = os.path.join(input_dir, "protokol_wzor_TP.docx")
        self.doc_builder = DocumentBuilderAgent(template_path)

    def generate_protocol(self):
        logger.info("Starting Protocol Generation...")
        
        # 1. Load Evaluation Results
        report_path = os.path.join(self.output_dir, "final_report.json")
        if not os.path.exists(report_path):
            logger.error(f"Report not found at {report_path}")
            return
            
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Hack to load into Pydantic model from dict, ignoring extra fields if any
            report = FinalEvaluationReport(**data)

        # 2. Load SWZ (Mocked/Hardcoded for now as we don't have separate SWZ parser yet)
        # Ideally we would parse `61cOU.pdf` again or use cached data.
        # We will use SWZData defaults which we updated in models.py
        swz = SWZData() 

        # 3. Collect Data
        protocol_data = self.data_agent.collect_data(swz, report)
        
        # 4. Generate Sections
        s_proc = self.section_agent.generate_procedural_sections(swz)
        s_part = self.section_agent.generate_parties_sections()
        s_res = self.section_agent.generate_results_sections(report, swz)
        s_form = self.section_agent.generate_formal_sections()
        
        all_sections = s_proc + s_part + s_res + s_form
        protocol_data.sections = all_sections
        
        # 5. Build Document
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        docx_filename = f"Protokol_{swz.case_id.replace('/', '-')}_{timestamp}.docx"
        output_path = os.path.join(self.output_dir, docx_filename)
        
        self.doc_builder.build_document(protocol_data, output_path)
        logger.info(f"Protocol generated at {output_path}")
        return output_path
