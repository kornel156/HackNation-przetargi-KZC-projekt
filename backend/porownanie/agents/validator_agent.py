from typing import List
from ..models import Offer, ValidationResult, ValidationCheck, ValidationStatus, SWZData

class ValidatorAgent:
    def __init__(self):
        pass

    def validate_offer(self, offer: Offer, swz: SWZData = None) -> ValidationResult:
        checks = []

        # 1. Math Check
        if abs(offer.financial.brutto_calculated - offer.financial.brutto_stated) < 0.05:
            msg = "Netto + VAT equals Brutto"
            status = ValidationStatus.PASSED
        elif offer.financial.netto == 0:
             msg = "Could not extract price"
             status = ValidationStatus.WARNING
        else:
            msg = f"Math error: {offer.financial.brutto_calculated} != {offer.financial.brutto_stated}"
            status = ValidationStatus.FAILED
        
        checks.append(ValidationCheck(check_name="Price Math", status=status, message=msg))

        # 2. NIP Presence
        if offer.supplier.nip:
             checks.append(ValidationCheck(check_name="NIP Check", status=ValidationStatus.PASSED, message=f"Found: {offer.supplier.nip}"))
        else:
             checks.append(ValidationCheck(check_name="NIP Check", status=ValidationStatus.FAILED, message="NIP missing", severity="CRITICAL"))

        # 3. SWZ Compliance (if SWZ data provided)
        if swz:
            if offer.technical.guarantee_months < swz.min_guarantee_months:
                 checks.append(ValidationCheck(check_name="Min Guarantee", status=ValidationStatus.FAILED, message=f"Too low: {offer.technical.guarantee_months}"))
            else:
                 checks.append(ValidationCheck(check_name="Min Guarantee", status=ValidationStatus.PASSED, message="OK"))

        # 4. Signatures (Placeholder)
        checks.append(ValidationCheck(check_name="Signature", status=ValidationStatus.WARNING, message="Digital signature verification not implemented"))

        # Overall Status
        overall = ValidationStatus.PASSED
        for c in checks:
            if c.status == ValidationStatus.FAILED:
                overall = ValidationStatus.FAILED
                break
        
        return ValidationResult(
            offer_id=offer.offer_id,
            overall_status=overall,
            checks=checks
        )
