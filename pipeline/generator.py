from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from prompts.generator_prompt import GENERATOR_PROMPT
from config import GENERATION_MODEL
from dotenv import load_dotenv
import os

load_dotenv()

FALLBACK_MESSAGE = (
    "I was unable to find sufficient information from trusted medical sources "
    "to answer your question. Please consult a qualified healthcare provider."
)

def generate(query: str, context_block: str, source_map: dict) -> tuple[str, dict]:
    if not context_block.strip():
        return FALLBACK_MESSAGE, {}

    llm = ChatGoogleGenerativeAI(
        model=GENERATION_MODEL,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = GENERATOR_PROMPT.format(
        context_block=context_block,
        user_query=query
    )

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)

    content = response.content
    if isinstance(content, list):
        content = content[0].get("text", "") if isinstance(content[0], dict) else content[0].text

    return content, source_map
