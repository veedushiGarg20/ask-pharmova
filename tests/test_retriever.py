import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.classifier import classify_query
from pipeline.reformulator import reformulate_query
from pipeline.retriever import retrieve
from pipeline.assembler import assemble_context
from config import REDIRECT_MESSAGE

test_queries = [
    "I've been struggling to stay motivated at work and feel stuck in my career. What should I do?",
    "What are the current indications for PCSK9 inhibitors in statin-intolerant patients with familial hypercholesterolemia?",
    "How can I stop procrastinating while studying?",
    "I've lost interest in activities I used to enjoy and feel hopeless most days.",
    "I'm trying to decide whether I should switch careers from software engineering to product management."
    
]

for query in test_queries:
    print(f"\nQuery: {query}")
    
    is_medical = classify_query(query)
    print(f"Medical: {is_medical}")
    
    if not is_medical:
        print(REDIRECT_MESSAGE)
        print("-" * 50)
        continue
    
    reformulated = reformulate_query(query)
    print(f"Reformulated: {reformulated}")
    
    results = retrieve(reformulated)
    context_block, source_map = assemble_context(results)
    
    print(f"Retrieved {len(results)} results")
    for n, meta in source_map.items():
        print(f"  [{n}] {meta['url']}")
    
    print("-" * 50)