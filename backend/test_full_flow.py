import asyncio
import os
from dotenv import load_dotenv
from workflow.manager import WorkflowManager
from workflow.state import AgentRole

# Load environment variables
from pathlib import Path
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

async def test_full_section_completion():
    print("--- Testing Full Section Completion (Basic Data) ---")
    manager = WorkflowManager()
    
    # 1. User initiates
    user_input_1 = "Chcę przygotować SWZ. Zacznijmy od danych zamawiającego."
    print(f"\nUser: {user_input_1}")
    response_1 = await manager.process_user_input(user_input_1)
    print(f"Agent ({response_1['active_section']}): {response_1['response']}")
    
    # 2. User provides ALL required data for Section I
    user_input_2 = """
    Oto dane:
    Nazwa: Urząd Gminy w Przykładowie
    Adres: ul. Słoneczna 1, 00-001 Przykładowo
    NIP: 123-456-78-90
    REGON: 123456789
    Email: przetargi@przykladowo.pl
    Telefon: +48 123 456 789
    Strona www: www.przykladowo.pl
    Osoba odpowiedzialna: Jan Kowalski, Kierownik Referatu
    """
    print(f"\nUser: {user_input_2}")
    response_2 = await manager.process_user_input(user_input_2)
    print(f"Agent ({response_2['active_section']}): {response_2['response']}")
    print(f"To Render: {response_2['to_render']}")
    
    if response_2['to_render']:
        print("\nSUCCESS: Section marked as complete and ready to render!")
        print("Rendered Content Preview:")
        print(response_2['response'][:200] + "...")
        
        # Verify extracted data
        if manager.state.swz_data.organization_name == "Urząd Gminy w Przykładowie":
             print("SUCCESS: Data extracted correctly into SWZData.")
        else:
             print(f"FAILURE: Data extraction failed. Got: {manager.state.swz_data.organization_name}")
             exit(1)
             
        # Verify rendering (check if placeholders are replaced)
        if "Urząd Gminy w Przykładowie" in response_2['response']:
             print("SUCCESS: Template rendered correctly.")
        else:
             print("FAILURE: Template NOT rendered (placeholders might be present).")
             exit(1)
             
        exit(0)
    else:
        print("\nFAILURE: Section NOT marked as complete.")
        exit(1)

if __name__ == "__main__":
    asyncio.run(test_full_section_completion())
