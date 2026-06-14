import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.classifier import classify_query
from pipeline.reformulator import reformulate_query
from pipeline.retriever import retrieve
from pipeline.assembler import assemble_context
from pipeline.generator import generate
from config import REDIRECT_MESSAGE

query = "What are the symptoms of diabetes?"

print(f"Query: {query}")

is_medical = classify_query(query)
print(f"Medical: {is_medical}")

if not is_medical:
    print(REDIRECT_MESSAGE)
else:
    reformulated = reformulate_query(query)
    print(f"Reformulated: {reformulated}")

    results = retrieve(reformulated)
    context_block, source_map = assemble_context(results)

    print(f"Retrieved {len(results)} results")
    for n, meta in source_map.items():
        print(f"  [{n}] {meta['url']}")

    print("\nGenerating response...\n")
    response, source_map = generate(query, context_block, source_map)
    # content = response if isinstance(response, str) else str(response)
    print(response)