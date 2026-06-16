import os
from dotenv import load_dotenv
from groq import Groq #type:ignore
from prompts.classifier_prompt import CLASSIFIER_PROMPT, TOPIC_RELEVANCE_PROMPT
from config import CLASSIFIER_MODEL

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_query(query: str) -> bool:
    try:
        prompt = CLASSIFIER_PROMPT.format(user_query=query)
        
        # Native Groq API execution payload
        response = client.chat.completions.create(
            model=CLASSIFIER_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0  # Kept at 0.0 for deterministic YES/NO returns
        )
        
        result = response.choices[0].message.content.strip().upper()
        return "YES" in result  

    except Exception as e:
        print(f"Native Classifier error: {e}")
        return False
    
    
def check_topic_relevance(follow_up_query: str, original_query: str) -> bool:
    try:
        prompt = TOPIC_RELEVANCE_PROMPT.format(
            original_query=original_query,
            follow_up_query=follow_up_query
        )

        # Native Groq API execution payload
        response = client.chat.completions.create(
            model=CLASSIFIER_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        
        result = response.choices[0].message.content.strip().upper()
        return "YES" in result

    except Exception as e:
        print(f"Native Topic relevance check error: {e}")
        return True