# tests/retriever_test.py
import sys
import os

# Append root folder structure path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.classifier import classify_query
from pipeline.reformulator import reformulate_query
from pipeline.retriever import retrieve
from config import REDIRECT_MESSAGE

# Using a classic multi-context query to run through the whole chain
query = "What are the common side effects of Diabetes and what are the lifestyle changes I should adopt?"

print("Running Step 2 Pipeline Integration Test (Multi-Context Split & Fetch)...")
print("=" * 80)
print(f"Original User Query: '{query}'\n")

# 1. Intent Check
is_medical = classify_query(query)
print(f"Medical Intent Verified: {is_medical}")

if not is_medical:
    print(f"Policy Action: {REDIRECT_MESSAGE}")
else:
    # 2. Multi-Query Reformulator
    sub_queries = reformulate_query(query)
    print(f"Groq Deconstructed Sub-Queries List:\n   {sub_queries}\n")

    # 3. Looped & Deduplicated Native Retrieval
    print("Executing multi-search retrieval process...")
    results = retrieve(sub_queries)
    
    print("=" * 80)
    print(f"Total Consolidated Unique Documents Extracted: {len(results)}")
    print("=" * 80)
    
    for idx, doc in enumerate(results, 1):
        print(f"   [{idx}] Source URL: {doc.get('url')}")