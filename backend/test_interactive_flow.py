import asyncio
import json
from dotenv import load_dotenv
from workflow.manager import WorkflowManager
from workflow.state import SWZSection

load_dotenv()

async def test_interactive_flow():
    print("--- Testing Interactive Flow ---")
    manager = WorkflowManager()
    
    # 1. User starts conversation
    print("\nUser: Chcę przygotować SWZ.")
    response = await manager.process_user_input("Chcę przygotować SWZ.")
    print(f"Agent: {response['response']}")
    print(f"Active Section: {response['active_section']}")
    
    # 2. User provides basic data (simulated)
    print("\nUser: Nazwa to 'Urząd Gminy', ulica Polna 1, Warszawa.")
    response = await manager.process_user_input("Nazwa to 'Urząd Gminy', ulica Polna 1, Warszawa.")
    print(f"Agent: {response['response']}")
    
    # 3. User provides missing data to complete section
    print("\nUser: NIP 1234567890, www.ug.pl, email kontakt@ug.pl")
    response = await manager.process_user_input("NIP 1234567890, www.ug.pl, email kontakt@ug.pl")
    print(f"Agent: {response['response']}")
    print(f"To Render: {response['to_render']}")
    
    if response['to_render']:
        print("✅ SUCCESS: Section I completed and marked for rendering.")
    else:
        print("⚠️ WARNING: Section I not completed yet (might need more info).")

if __name__ == "__main__":
    asyncio.run(test_interactive_flow())
