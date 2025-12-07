from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from workflow.manager import WorkflowManager
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SWZ Architect API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = WorkflowManager()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    to_render: bool
    active_section: str
    state: dict
    markdown_content: str

class SWZUpdateRequest(BaseModel):
    # Dane zamawiającego
    organization_name: Optional[str] = None
    address: Optional[str] = None
    nip: Optional[str] = None
    regon: Optional[str] = None
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    person_responsible: Optional[str] = None
    
    # Tryb i przedmiot
    procurement_mode: Optional[str] = None
    legal_basis: Optional[str] = None
    procurement_title: Optional[str] = None
    procurement_id: Optional[str] = None
    cpv_codes: Optional[str] = None
    procurement_type: Optional[str] = None
    description: Optional[str] = None
    
    # Terminy
    execution_deadline: Optional[str] = None
    variants_allowed: Optional[bool] = False
    submission_deadline: Optional[str] = None
    opening_date: Optional[str] = None
    binding_period: Optional[str] = None
    
    # Kryteria
    criteria_price_weight: Optional[str] = None
    criteria_other_name: Optional[str] = None
    criteria_other_weight: Optional[str] = None
    budget: Optional[str] = None
    quality_features: Optional[str] = None
    
    # Warunki i wykluczenia
    exclusion_grounds_optional: Optional[str] = None
    participation_conditions: Optional[str] = None
    required_documents: Optional[str] = None
    
    # Umowa
    contract_terms: Optional[str] = None
    legal_protection_info: Optional[str] = None
    
    # Komunikacja
    communication_rules: Optional[str] = None
    evaluation_procedure: Optional[str] = None
    
    # Dodatkowe
    consortium_rules: Optional[str] = None
    subcontracting_rules: Optional[str] = None
    lots: Optional[str] = None
    employment_requirements: Optional[str] = None
    social_clauses: Optional[str] = None
    warranty_terms: Optional[str] = None
    special_requirements: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await manager.process_user_input(request.message)
        return ChatResponse(
            response=result["response"], 
            to_render=result["to_render"],
            active_section=str(result["active_section"]),
            state=manager.get_state(),
            markdown_content=result["markdown_content"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/state")
async def get_state():
    return manager.get_state()

@app.get("/initial-template")
async def get_initial_template():
    """Zwraca początkowy szablon SWZ z placeholderami"""
    markdown_content = manager.state.swz_data.generate_markdown()
    return {
        "markdown_content": markdown_content,
        "swz_data": manager.state.swz_data.model_dump()
    }

@app.post("/update-swz")
async def update_swz(request: SWZUpdateRequest):
    """Aktualizuje dane SWZ na podstawie formularza i zwraca nowy markdown"""
    try:
        swz_data = manager.state.swz_data
        
        # Aktualizuj dane zamawiającego
        if request.organization_name:
            swz_data.organization_name = request.organization_name
        if request.address:
            swz_data.address = request.address
        if request.nip:
            swz_data.nip = request.nip
        if request.regon:
            swz_data.regon = request.regon
        if request.contact_email:
            swz_data.contact_email = request.contact_email
        if request.phone:
            swz_data.phone = request.phone
        if request.website:
            swz_data.website = request.website
        if request.person_responsible:
            swz_data.person_responsible = request.person_responsible
        
        # Aktualizuj tryb i przedmiot
        if request.procurement_mode:
            swz_data.procurement_mode = request.procurement_mode
        if request.legal_basis:
            swz_data.legal_basis = request.legal_basis
        if request.procurement_title:
            swz_data.procurement_title = request.procurement_title
        if request.procurement_id:
            swz_data.procurement_id = request.procurement_id
        if request.cpv_codes:
            swz_data.cpv_codes = [code.strip() for code in request.cpv_codes.split(",") if code.strip()]
        if request.procurement_type:
            swz_data.procurement_type = request.procurement_type
        if request.description:
            swz_data.description = request.description
        
        # Aktualizuj terminy
        if request.execution_deadline:
            swz_data.execution_deadline = request.execution_deadline
        swz_data.variants_allowed = request.variants_allowed or False
        if request.submission_deadline:
            swz_data.submission_deadline = request.submission_deadline
        if request.opening_date:
            swz_data.opening_date = request.opening_date
        if request.binding_period:
            swz_data.binding_period = request.binding_period
        
        # Aktualizuj kryteria
        criteria = []
        if request.criteria_price_weight:
            criteria.append({"name": "Cena", "weight": int(request.criteria_price_weight)})
        if request.criteria_other_name and request.criteria_other_weight:
            criteria.append({"name": request.criteria_other_name, "weight": int(request.criteria_other_weight)})
        if criteria:
            swz_data.criteria = criteria
        
        if request.budget:
            try:
                swz_data.budget = float(request.budget)
            except ValueError:
                pass
        
        if request.quality_features:
            swz_data.quality_features = [f.strip() for f in request.quality_features.split("\n") if f.strip()]
        
        # Aktualizuj warunki i wykluczenia
        if request.exclusion_grounds_optional:
            swz_data.exclusion_grounds_optional = [g.strip() for g in request.exclusion_grounds_optional.split("\n") if g.strip()]
        if request.participation_conditions:
            swz_data.participation_conditions = [c.strip() for c in request.participation_conditions.split("\n") if c.strip()]
        if request.required_documents:
            swz_data.required_documents = [d.strip() for d in request.required_documents.split("\n") if d.strip()]
        
        # Aktualizuj umowę
        if request.contract_terms:
            swz_data.contract_terms = [t.strip() for t in request.contract_terms.split("\n") if t.strip()]
        if request.legal_protection_info:
            swz_data.legal_protection_info = request.legal_protection_info
        
        # Aktualizuj komunikację
        if request.communication_rules:
            swz_data.communication_rules = request.communication_rules
        if request.evaluation_procedure:
            swz_data.evaluation_procedure = request.evaluation_procedure
        
        # Aktualizuj dodatkowe wymagania
        if request.consortium_rules:
            swz_data.consortium_rules = request.consortium_rules
        if request.subcontracting_rules:
            swz_data.subcontracting_rules = request.subcontracting_rules
        if request.lots:
            swz_data.lots = [{"name": l.strip()} for l in request.lots.split("\n") if l.strip()]
        if request.employment_requirements:
            swz_data.employment_requirements = request.employment_requirements
        if request.social_clauses:
            swz_data.social_clauses = request.social_clauses
        if request.warranty_terms:
            swz_data.warranty_terms = request.warranty_terms
        if request.special_requirements:
            swz_data.special_requirements = request.special_requirements
        
        # Generuj nowy markdown
        markdown_content = swz_data.generate_markdown()
        
        return {
            "markdown_content": markdown_content,
            "swz_data": swz_data.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
