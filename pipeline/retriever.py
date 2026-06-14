from langchain_community.tools.tavily_search import TavilySearchResults 
from config import TRUSTED_SOURCES, TAVILY_MAX_RESULTS
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
if api_key is None:
    raise EnvironmentError("TAVILY_API_KEY is not set")
os.environ["TAVILY_API_KEY"] = api_key

def retrieve(query: str) -> list[dict]:
    try:
        tavily = TavilySearchResults(
            max_results=TAVILY_MAX_RESULTS,
            include_domains=TRUSTED_SOURCES,
            tavily_api_key=api_key
        )
        results = tavily.invoke(query)
        return results if results else []
    except Exception as e:
        print(f"Tavily retrieval error: {e}")
        return []