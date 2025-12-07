import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from workflow.manager import WorkflowManager
from workflow.state import AgentRole

# Mocking the API key if not present for testing purposes
if "GOOGLE_API_KEY" not in os.environ:
    print("WARNING: GOOGLE_API_KEY not found. Agents might fail if not mocked.")

async def run_test():
    manager = WorkflowManager()
    
    print("--- Starting Test Conversation ---")
    
    # 1. User starts
    user_input = "Dzień dobry, chciałbym przygotować SWZ na zakup komputerów."
    print(f"User: {user_input}")
    response = await manager.process_user_input(user_input)
    print(f"System: {response}")
    
    # 2. User provides info
    user_input = "Urząd Gminy w Wąchocku, ul. Wielka 1."
    print(f"User: {user_input}")
    response = await manager.process_user_input(user_input)
    print(f"System: {response}")
    
    # 3. User asks for legal check
    user_input = "Sprawdź jakie są wymogi dla komputerów w PZP."
    print(f"User: {user_input}")
    response = await manager.process_user_input(user_input)
    print(f"System: {response}")
    
    print("--- Test Finished ---")

if __name__ == "__main__":
    asyncio.run(run_test())
