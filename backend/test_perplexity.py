import asyncio
import os
from dotenv import load_dotenv
from agents.researcher import LegalResearcher
from workflow.state import WorkflowState, Message, AgentRole

load_dotenv()

async def test_perplexity():
    print("--- Testing Perplexity Integration ---")
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key or "YOUR_PERPLEXITY_API_KEY" in api_key:
        print("WARNING: PERPLEXITY_API_KEY is not set or is default. Test might fail or fallback to DuckDuckGo.")
    else:
        print("PERPLEXITY_API_KEY found.")

    researcher = LegalResearcher()
    
    # Simulate a state where a search is needed
    state = WorkflowState()
    state.history.append(Message(role=AgentRole.USER, content="Sprawdź w PZP jakie są terminy składania ofert w trybie podstawowym."))
    
    # Force a search query directly to test the method
    query = "PZP terminy składania ofert tryb podstawowy"
    print(f"Performing research for: {query}")
    
    result = await researcher.perform_research(query)
    print("\nResult:")
    print(result)
    
    if "Perplexity Search Results" in result:
        print("\nSUCCESS: Perplexity API was used.")
    elif "DuckDuckGo Search Results" in result:
        print("\nSUCCESS: Fallback to DuckDuckGo worked (Perplexity might be unconfigured).")
    else:
        print("\nFAILURE: No search results returned.")

if __name__ == "__main__":
    asyncio.run(test_perplexity())
