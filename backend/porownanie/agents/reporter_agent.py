import json
import os
from datetime import datetime
from typing import List, Dict
from ..models import FinalEvaluationReport, ScoringResult, ValidationResult, ComplianceReport, Offer

class ReporterAgent:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_report(self, 
                       offers: List[Offer], 
                       validations: List[ValidationResult], 
                       scorings: List[ScoringResult], 
                       compliance_reports: List[ComplianceReport]) -> str:
        
        # Aggregate details
        details = {}
        winner_id = scorings[0].offer_id if scorings else None

        for offer in offers:
            oid = offer.offer_id
            v = next((x for x in validations if x.offer_id == oid), None)
            s = next((x for x in scorings if x.offer_id == oid), None)
            c = next((x for x in compliance_reports if x.offer_id == oid), None)
            
            details[oid] = {
                "supplier": offer.supplier.model_dump(),
                "financial": offer.financial.model_dump(),
                "validation": v.model_dump() if v else None,
                "score": s.model_dump() if s else None,
                "compliance": c.model_dump() if c else None
            }

        final_report = FinalEvaluationReport(
            evaluation_id=f"EVAL-{datetime.now().strftime('%Y%m%d%H%M')}",
            created_at=datetime.now(),
            offers_processed=len(offers),
            winner_offer_id=winner_id,
            rankings=scorings,
            details=details
        )

        # Save JSON
        json_path = os.path.join(self.output_dir, "final_report.json")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(final_report.model_dump_json(indent=2))

        # Generate HTML Summary
        html_content = self._generate_html(final_report)
        html_path = os.path.join(self.output_dir, "report.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return json_path

    def _generate_html(self, report: FinalEvaluationReport) -> str:
        rows = ""
        for rank in report.rankings:
            oid = rank.offer_id
            detail = report.details.get(oid)
            supplier = detail['supplier']['name'] if detail else "Unknown"
            price = detail['financial']['brutto_stated'] if detail else 0
            
            rows += f"""
            <tr>
                <td>{rank.rank}</td>
                <td>{supplier}</td>
                <td>{price} PLN</td>
                <td>{rank.total_score}</td>
            </tr>
            """
            
        return f"""
        <html>
        <head><title>Evaluation Report {report.evaluation_id}</title></head>
        <body>
            <h1>Evaluation Report</h1>
            <p>ID: {report.evaluation_id}</p>
            <p>Date: {report.created_at}</p>
            <h2>Rankings</h2>
            <table border="1">
                <tr><th>Rank</th><th>Supplier</th><th>Price (Brutto)</th><th>Score</th></tr>
                {rows}
            </table>
        </body>
        </html>
        """
