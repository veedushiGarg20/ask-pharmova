import os
import json
from dotenv import load_dotenv
from groq import Groq #type:ignore
from prompts.reformulator_prompt import REFORMULATOR_PROMPT
from config import REFORMULATOR_MODEL

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def reformulate_query(query: str) -> list[str]:
    try:
        prompt = REFORMULATOR_PROMPT.format(user_query=query)
        
        response = client.chat.completions.create(
            model=REFORMULATOR_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Kept low for deterministic and accurate structural returns
            response_format={"type": "json_object"}
        )
        
        raw_content = response.choices[0].message.content
        parsed_json = json.loads(raw_content)
        
        queries = parsed_json.get("queries", [query])
        
        return queries if queries else [query]

    except Exception as e:
        print(f"Multi-Context Reformulator error: {e}")
        return [query]