import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts.generator_prompt import GENERATOR_PROMPT, SYSTEM_PROMPT, FOLLOWUP_PROMPT
from config import GENERATION_MODEL

load_dotenv()

FALLBACK_MESSAGE = (
    "I was unable to find sufficient information from trusted medical sources "
    "to answer your question. Please consult a qualified healthcare provider."
)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate(query: str, context_block: str, source_map: dict, conversation_history: list = None) -> tuple[str, dict]:
    if not context_block.strip():
        return FALLBACK_MESSAGE, {}

    try:
        messages = []

        if conversation_history is not None:
            for message in conversation_history:
                role = "user" if message["role"] == "user" else "model"
                messages.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=message["content"])]
                    )
                )
            
            query_prompt = FOLLOWUP_PROMPT.format(
                context_block=context_block,
                user_query=query
            )
        else:
            query_prompt = GENERATOR_PROMPT.format(
                context_block=context_block,
                user_query=query
            )

        messages.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=query_prompt)]
            )
        )

        
        response = client.models.generate_content(
            model=GENERATION_MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2  # Keep deterministic and strictly grounded to provided context
            )
        )

        return response.text, source_map

    except Exception as e:
        print(f"Native Gemini Generation error: {e}")
        return "An error occurred while generating the clinical response.", {}