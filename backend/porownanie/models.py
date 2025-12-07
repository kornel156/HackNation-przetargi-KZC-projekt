from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from enum import Enum

class ValidationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"

class SWZData(BaseModel):
    # Evaluation Params
    min_guarantee_months: int = 24
    max_delivery_days: int = 30
    weight_price: float = 60.0
    weight_guarantee: float = 20.0
    weight_delivery: float = 20.0
    required_packages: List[str] = []
    
    # Protocol Metadata (New)
    case_id: str = "ZP/2024/123"
    buyer_name: str = "SZPITAL WOJEWÓDZKI IM. KARDYNAŁA STEFANA WYSZYŃSKIEGO W ŁOMŻY"
    buyer_address: str = "Al. Piłsudskiego 11, 18-404 Łomża"
    project_name: str = "Zakup sprzętu do rehabilitacji onkologicznej"
    cpv_codes: List[str] = ["33 10 00 00-1"]
    budget: float = 250000.00
    procedure_mode: str = "przetarg nieograniczony"
    publication_date: str = "2021-10-20"
    submission_deadline: str = "2021-10-25 12:00"
    opening_date: str = "2021-10-25 14:00"

class ProtocolSection(BaseModel):
    section_id: int
    title: str
    content: Any # Dict or String

class ProtocolData(BaseModel):
    case_id: str
    creation_date: datetime
    sections: List[ProtocolSection]

class SupplierData(BaseModel):
    name: str = Field(..., description="Full name of the supplier")
    address: Optional[str] = None
    nip: Optional[str] = None
    regon: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    bank_account: Optional[str] = None

class FinancialData(BaseModel):
    netto: float
    vat_rate: float
    brutto_calculated: float
    brutto_stated: float
    currency: str = "PLN"
    is_math_correct: bool = True

class TechnicalParams(BaseModel):
    guarantee_months: int
    delivery_days: int
    payment_terms: str
    packages: List[str] = []

class Declaration(BaseModel):
    read_and_understood: bool = False
    accepts_without_reservations: bool = False
    subcontracting_plan: str = "none"

class Offer(BaseModel):
    offer_id: str
    file_name: str
    supplier: SupplierData
    financial: FinancialData
    technical: TechnicalParams
    declarations: Declaration
    raw_text_snippet: Optional[str] = None
    extraction_confidence: float = 1.0

class ValidationCheck(BaseModel):
    check_name: str
    status: ValidationStatus
    message: str
    severity: str = "MEDIUM"

class ValidationResult(BaseModel):
    offer_id: str
    overall_status: ValidationStatus
    checks: List[ValidationCheck]

class CriterionScore(BaseModel):
    criterion_name: str
    score: float
    max_points: float
    weight: float
    formula_explanation: str

class ScoringResult(BaseModel):
    offer_id: str
    total_score: float
    rank: int = 0
    criteria_scores: List[CriterionScore]

class ComplianceFinding(BaseModel):
    issue: str
    risk_level: str
    recommendation: str

class ComplianceReport(BaseModel):
    offer_id: str
    findings: List[ComplianceFinding]
    krs_verified: bool = False
    tax_verified: bool = False

class FinalEvaluationReport(BaseModel):
    evaluation_id: str
    created_at: datetime
    offers_processed: int
    winner_offer_id: Optional[str]
    rankings: List[ScoringResult]
    details: Dict[str, Dict[str, Any]]  # Map offer_id -> detailed data
