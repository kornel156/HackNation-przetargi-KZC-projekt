from agents.base_agent import BaseAgent
from workflow.state import AgentRole
from duckduckgo_search import DDGS
from openai import OpenAI
import os

class LegalResearcher(BaseAgent):
    def __init__(self):
        super().__init__(role=AgentRole.LEGAL_RESEARCHER)
        self.ddgs = DDGS()
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        self.perplexity_client = None
        if self.perplexity_api_key and "YOUR_PERPLEXITY_API_KEY" not in self.perplexity_api_key:
            self.perplexity_client = OpenAI(
                api_key=self.perplexity_api_key, 
                base_url="https://api.perplexity.ai"
            )

    def get_system_instruction(self) -> str:
        return """
        You are the Legal Researcher (Badacz Prawny).
        Your goal is to find FACTUAL information about Polish Public Procurement Law (PZP) and related regulations.
        You must verify the user's requests against current laws.
        
        When asked to research, use the provided tools (simulated here by your internal knowledge + search results injected into context).
        Since you are an AI, you will receive search results in your prompt if available.
        
        Output your findings clearly, citing the specific article of the PZP act if possible.
        """

    async def perform_research(self, query: str) -> str:
        """
        Performs a web search using Perplexity API (preferred) or DuckDuckGo (fallback).
        """
        # Try Perplexity first
        if self.perplexity_client:
            try:
                messages = [
                    {"role": "system", "content": "You are a helpful legal research assistant. Search for current Polish Public Procurement Law (PZP). Be precise and cite sources."},
                    {"role": "user", "content": query}
                ]
                response = self.perplexity_client.chat.completions.create(
                    model="llama-3.1-sonar-large-128k-online",
                    messages=messages,
                )
                return f"Perplexity Search Results:\n{response.choices[0].message.content}"
            except Exception as e:
                print(f"Perplexity API failed: {e}. Falling back to DuckDuckGo.")
        
        # Fallback to DuckDuckGo
        try:
            results = self.ddgs.text(query, region='pl-pl', max_results=3)
            summary = "DuckDuckGo Search Results:\n"
            for r in results:
                summary += f"- {r['title']}: {r['body']} ({r['href']})\n"
            return summary
        except Exception as e:
            return f"Error performing search: {str(e)}"

    async def process(self, state, user_input=None):
        # Override process to inject search results if needed
        # For simplicity, we assume the Orchestrator or Manager calls perform_research explicitly
        # or we detect a research need here.
        
        # Simple heuristic: if the last message asks for verification or law, do a search.
        last_msg = state.history[-1].content if state.history else ""
        search_results = ""
        
        if "sprawdź" in last_msg.lower() or "ustawa" in last_msg.lower() or "pzp" in last_msg.lower():
            query = f"PZP {last_msg}"
            search_results = await self.perform_research(query)
            
        # Call base process but inject search results into the prompt (via user_input or a custom way)
        # Here we append it to the user input for the model to see
        augmented_input = user_input or ""
        if search_results:
            augmented_input += f"\n\n[SYSTEM INJECTED RESEARCH DATA]:\n{search_results}"
            
        return await super().process(state, augmented_input)
