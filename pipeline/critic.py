import os
import json
from dotenv import load_dotenv
from groq import Groq
from prompts.critic_prompt import CRITIC_PROMPT
from config import CRITIC_MODEL

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def evaluate_context(query: str, context_block: str) -> dict:
    # If retriever returned nothing, immediately trigger a failure gap state
    if not context_block.strip():
        return {"sufficient": False, "missing_info": "The search returned absolutely no results."}

    try:
        prompt = CRITIC_PROMPT.format(user_query=query, context_block=context_block)
        
        response = client.chat.completions.create(
            model=CRITIC_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0, # Complete determinism for verification accuracy
            response_format={"type": "json_object"}
        )
        
        raw_content = response.choices[0].message.content
        parsed_json = json.loads(raw_content)
        
        return {
            "sufficient": bool(parsed_json.get("sufficient", False)),
            "missing_info": str(parsed_json.get("missing_info", ""))
        }

    except Exception as e:
        print(f"Native Critic Node error: {e}")
        return {"sufficient": True, "missing_info": ""}