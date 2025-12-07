import asyncio
import os
from dotenv import load_dotenv
from agents.researcher import LegalResearcher

load_dotenv()

async def test_legal_knowledge():
    print("--- Testing Perplexity Legal Knowledge (PZP) ---")
    
    researcher = LegalResearcher()
    
    test_cases = [
        {
            "query": "O co chodzi w Art. 108 ustawy PZP? Wymień główne przesłanki.",
            "expected_keywords": ["wykluczenie", "przestępstwo", "karalność", "podatki"]
        },
        {
            "query": "Jakie są warianty trybu podstawowego wg Art. 275 PZP?",
            "expected_keywords": ["negocjacje", "fakultatywne", "obligatoryjne", "wariant"]
        },
        {
            "query": "Ile wynosi minimalny termin składania ofert w trybie podstawowym dla dostaw?",
            "expected_keywords": ["7 dni", "14 dni", "termin"]
        }
    ]
    
    for case in test_cases:
        print(f"\nQuery: {case['query']}")
        result = await researcher.perform_research(case['query'])
        print(f"Result snippet: {result[:200]}...") # Print first 200 chars
        
        missing_keywords = [kw for kw in case['expected_keywords'] if kw.lower() not in result.lower()]
        
        if not missing_keywords:
            print("✅ PASSED: All keywords found.")
        else:
            print(f"⚠️ WARNING: Missing keywords: {missing_keywords}")
            # We don't fail hard because LLM output varies, but it's a good indicator.

if __name__ == "__main__":
    asyncio.run(test_legal_knowledge())
