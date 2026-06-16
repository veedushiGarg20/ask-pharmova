from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from prompts.classifier_prompt import CLASSIFIER_PROMPT, TOPIC_RELEVANCE_PROMPT
from config import CLASSIFIER_MODEL
from dotenv import load_dotenv
import os

load_dotenv()

def classify_query(query: str) -> bool:
    try:
        llm = ChatGroq(
            model=CLASSIFIER_MODEL,
            api_key=os.getenv("GROQ_API_KEY")
        )

        prompt = CLASSIFIER_PROMPT.format(user_query=query)
        response = llm.invoke([HumanMessage(content=prompt)])
        
        content = response.content
        if isinstance(content, list):
            content = " ".join(str(item) for item in content)
        result = content.strip().upper()

        return result == "YES"

    except Exception as e:
        print(f"Classifier error: {e}")
        return False
    
    
def check_topic_relevance(follow_up_query: str, original_query: str) -> bool:
    try:
        llm = ChatGroq(
            model=CLASSIFIER_MODEL,
            api_key=os.getenv("GROQ_API_KEY")
        )

        prompt = TOPIC_RELEVANCE_PROMPT.format(
            original_query=original_query,
            follow_up_query=follow_up_query
        )

        response = llm.invoke([HumanMessage(content=prompt)])
        result = response.content.strip().upper()

        return result == "YES"

    except Exception as e:
        print(f"Topic relevance check error: {e}")
        return True