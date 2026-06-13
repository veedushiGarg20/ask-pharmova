from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from prompts.classifier_prompt import CLASSIFIER_PROMPT
from config import GEMINI_MODEL
from dotenv import load_dotenv
import os

load_dotenv()

def classify_query(query: str) -> bool:
    try:
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        prompt = CLASSIFIER_PROMPT.format(user_query=query)
        response = llm.invoke([HumanMessage(content=prompt)])
        result = response.content.strip().upper()

        return result == "YES"

    except Exception as e:
        print(f"Classifier error: {e}")
        return False