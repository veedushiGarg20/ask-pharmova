# tests/test_generator.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.classifier import classify_query
from pipeline.reformulator import reformulate_query
from pipeline.retriever import retrieve
from pipeline.assembler import assemble_context
from pipeline.generator import generate
from config import REDIRECT_MESSAGE

# A standard medical query to test the end-to-end native SDK implementation
query = "What are the symptoms of diabetes and what lifestyle changes should I make?"

print("Running Native Pipeline Integration Test (End-to-End Generation)...")
print("=" * 80)
print(f"Query: {query}\n")

# 1. Evaluate Query Intent via Groq Native Client
is_medical = classify_query(query)
print(f"Query is medical: {is_medical}")

if not is_medical:
    print(f"Redirect Message: {REDIRECT_MESSAGE}")
else:
    # 2. Optimize Search Keywords via Groq Native Client
    reformulated = reformulate_query(query)
    print(f"Reformulated query: '{reformulated}'")

    # 3. Pull Documents via Tavily Client
    print("Querying trusted domains...")
    results = retrieve(reformulated)

    # 4. Parse Context (Vanilla Python)
    context_block, source_map = assemble_context(results)

    print(f"Retrieval Output: Extracted {len(results)} source document records.")
    for n, meta in source_map.items():
        print(f"  [{n}] Reference URL: {meta['url']}")

    # 5. Synthesize Grounded Medical Response via Gemini Native Client
    print("\nConnecting to Gemini to generate response...\n")
    response, final_source_map = generate(query, context_block, source_map)
    
    print("=" * 80)
    print("[GEMINI RESPONSE]:")
    print(response)
    print("=" * 80)