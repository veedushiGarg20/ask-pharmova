import os
from dotenv import load_dotenv
from tavily import TavilyClient #type:ignore
from config import TRUSTED_SOURCES, TAVILY_MAX_RESULTS

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
if api_key is None:
    raise EnvironmentError("TAVILY_API_KEY is not set")

tavily_client = TavilyClient(api_key=api_key)

def retrieve(queries: list[str]) -> list[dict]:
    try:
        unique_results = {}
        
        for query in queries:
            query = query.strip()
            if not query:
                continue
        
            response = tavily_client.search(
                query=query,
                max_results=TAVILY_MAX_RESULTS,
                include_domains=TRUSTED_SOURCES,
                search_depth="basic" # Standard low-latency setup matching Phase 1 spec
            )
            
            results = response.get("results", [])
            
            for doc in results:
                url = doc.get("url")
                if url and url not in unique_results:
                    unique_results[url] = doc
            
        return list(unique_results.values()) if unique_results else []
        
    except Exception as e:
        print(f"Native Tavily retrieval error: {e}")
        return []