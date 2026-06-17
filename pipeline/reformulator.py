import os
import json
from dotenv import load_dotenv
from groq import Groq #type:ignore
from prompts.reformulator_prompt import REFORMULATOR_PROMPT, CORRECTIVE_REFORMULATOR_PROMPT
from config import REFORMULATOR_MODEL

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def reformulate_query(query: str, missing_info: str = "") -> list[str]:
    try:
        if missing_info and missing_info.strip():
            print("Generating corrective reformulation queries focused on the identified information gap...")
            prompt = CORRECTIVE_REFORMULATOR_PROMPT.format(
                user_query=query,
                missing_info=missing_info
            )
        else:
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
        
        if queries:
            return queries
        else:
            return[f"{query} {missing_info}"] if missing_info else [query]

    except Exception as e:
        print(f"Multi-Context Reformulator error: {e}")
        return [query]