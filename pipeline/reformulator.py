from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from prompts.reformulator_prompt import REFORMULATOR_PROMPT
from config import GEMINI_MODEL
from dotenv import load_dotenv
import os

load_dotenv()

def reformulate_query(query: str) -> str:
    try:
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        prompt = REFORMULATOR_PROMPT.format(user_query=query)
        response = llm.invoke([HumanMessage(content=prompt)])
        reformulated = response.content.strip()

        return reformulated if reformulated else query

    except Exception as e:
        print(f"Reformulator error: {e}")
        return query