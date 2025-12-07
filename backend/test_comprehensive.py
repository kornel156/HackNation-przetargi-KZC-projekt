import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from workflow.manager import WorkflowManager
from workflow.state import AgentRole

async def test_comprehensive_flow():
    print("--- STARTING COMPREHENSIVE SYSTEM TEST ---")
    manager = WorkflowManager()
    
    # Scenario: User wants to create SWZ for computer delivery
    
    # 1. Basic Data
    print("\n[STEP 1] Basic Data")
    user_input = """
    Chcę przygotować SWZ.
    Dane zamawiającego:
    Nazwa: Szkoła Podstawowa nr 1
    Adres: ul. Szkolna 5, 00-001 Warszawa
    NIP: 525-000-00-00
    REGON: 140000000
    Email: sekretariat@sp1.waw.pl
    Telefon: 22 123 45 67
    Strona: www.sp1.waw.pl
    Osoba: Anna Nowak
    """
    response = await manager.process_user_input(user_input)
    print(f"DEBUG: Active Section: {response.get('active_section')}")
    print(f"DEBUG: To Render: {response.get('to_render')}")
    print(f"Agent: {response['response'][:200]}...")
    
    if response['to_render'] and "Szkoła Podstawowa nr 1" in response['response']:
        print("[OK] Basic Data: Rendered correctly.")
        print(f"   Extracted NIP: {manager.state.swz_data.nip}")
    else:
        print("[FAIL] Basic Data: Failed.")
        exit(1)

    # 2. Subject (Przedmiot)
    print("\n[STEP 2] Subject")
    user_input = """
    Przejdźmy do przedmiotu zamówienia.
    Nazwa: Dostawa laptopów dla nauczycieli.
    Rodzaj: dostawy.
    CPV: 30213100-6.
    Opis: Przedmiotem zamówienia jest dostawa 20 fabrycznie nowych laptopów o przekątnej 15 cali, procesor i5, 16GB RAM.
    """
    response = await manager.process_user_input(user_input)
    print(f"DEBUG: Active Section: {response.get('active_section')}")
    print(f"DEBUG: To Render: {response.get('to_render')}")
    print(f"Agent: {response['response'][:200]}...")
    
    if response['to_render'] and "Dostawa laptopów" in response['response']:
        print("[OK] Subject: Rendered correctly.")
        print(f"   Extracted Title: {manager.state.swz_data.procurement_title}")
    else:
        print("[FAIL] Subject: Failed.")
        exit(1)

    # 3. Criteria (Kryteria)
    print("\n[STEP 3] Criteria")
    user_input = """
    Kryteria oceny ofert:
    Cena - 60%
    Gwarancja - 40%
    """
    response = await manager.process_user_input(user_input)
    print(f"DEBUG: Active Section: {response.get('active_section')}")
    print(f"DEBUG: To Render: {response.get('to_render')}")
    print(f"Agent: {response['response'][:200]}...")
    
    if response['to_render'] and "Cena" in response['response']:
        print("[OK] Criteria: Rendered correctly.")
        print(f"   Extracted Criteria: {manager.state.swz_data.criteria}")
    else:
        print("[FAIL] Criteria: Failed.")
        exit(1)

    # 4. Deadlines (Termin)
    print("\n[STEP 4] Deadlines")
    user_input = """
    Termin wykonania: 30 dni od podpisania umowy.
    """
    response = await manager.process_user_input(user_input)
    print(f"DEBUG: Active Section: {response.get('active_section')}")
    print(f"DEBUG: To Render: {response.get('to_render')}")
    print(f"Agent: {response['response'][:200]}...")
    
    if response['to_render'] and "30 dni" in response['response']:
        print("[OK] Deadlines: Rendered correctly.")
        print(f"   Extracted Deadline: {manager.state.swz_data.execution_deadline}")
    else:
        print("[FAIL] Deadlines: Failed.")
        exit(1)

    print("\n--- ALL TESTS PASSED SUCCESSFULLY ---")
    exit(0)

if __name__ == "__main__":
    asyncio.run(test_comprehensive_flow())
