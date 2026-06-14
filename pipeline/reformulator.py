from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from prompts.reformulator_prompt import REFORMULATOR_PROMPT
from config import REFORMULATOR_MODEL
from dotenv import load_dotenv
import os

load_dotenv()

def reformulate_query(query: str) -> str:
    try:
        llm = ChatGroq(
            model=REFORMULATOR_MODEL,
            api_key=os.getenv("GROQ_API_KEY")
        )

        prompt = REFORMULATOR_PROMPT.format(user_query=query)
        response = llm.invoke([HumanMessage(content=prompt)])
        
        content = response.content
        if isinstance(content, list):
            content = " ".join(str(item) for item in content)
        reformulated = content.strip()

        return reformulated if reformulated else query

    except Exception as e:
        print(f"Reformulator error: {e}")
        return query