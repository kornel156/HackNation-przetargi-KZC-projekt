from typing import List
from ..models import Offer, ComplianceReport, ComplianceFinding

class ComplianceAgent:
    def check_compliance(self, offer: Offer) -> ComplianceReport:
        findings = []

        # Mock KRS Check
        # In real world: call API with offer.supplier.nip
        findings.append(ComplianceFinding(
            issue="KRS Status",
            risk_level="LOW",
            recommendation="Verified (Mock): Active entity."
        ))

        # Mock Tax Check
        findings.append(ComplianceFinding(
            issue="Tax Arrears",
            risk_level="LOW",
            recommendation="Verified (Mock): No arrears found."
        ))

        # Check for specific suspicious values
        if offer.technical.guarantee_months < 12:
            findings.append(ComplianceFinding(
                issue="Low Guarantee",
                risk_level="MEDIUM",
                recommendation="Guarantee below standard 12 months."
            ))

        return ComplianceReport(
            offer_id=offer.offer_id,
            findings=findings,
            krs_verified=True,
            tax_verified=True
        )
