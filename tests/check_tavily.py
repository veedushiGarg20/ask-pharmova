from langchain_community.tools.tavily_search import TavilySearchResults #type:ignore
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY") #type:ignore

tavily = TavilySearchResults(max_results=3)
results = tavily.invoke("symptoms of diabetes")

for r in results:
    print(r["url"])
    print(r["content"][:200])
    print("---")