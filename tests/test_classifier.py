# tests/test_classifier.py
import os
import sys

# 1. Fix the import path resolution footprint
# This appends the root directory to the Python path so it can locate 'classifier' cleanly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.classifier import classify_query, check_topic_relevance

def run_diagnostic_tests():
    print("Starting Native SDK Classifier Diagnostic Tests...")
    print("-" * 60)

    # Test Case 1: Pure Medical Inquiry
    medical_prompt = "What are the primary symptoms of Type 2 Diabetes and what diet is recommended?"
    print(f"[Test 1 Input]: '{medical_prompt}'")
    
    is_medical = classify_query(medical_prompt)
    print(f"[Classifier Result]: {is_medical}")
    print(f"Pass Status: {'SUCCESS' if is_medical is True else 'FAILED'}")
    print("-" * 60)

    # Test Case 2: Non-Medical Irrelevant Query
    non_medical_prompt = "How do I write a fast matrix multiplication algorithm in C++?"
    print(f"[Test 2 Input]: '{non_medical_prompt}'")
    
    is_medical_2 = classify_query(non_medical_prompt)
    print(f"[Classifier Result]: {is_medical_2}")
    print(f"Pass Status: {'SUCCESS' if is_medical_2 is False else 'FAILED'}")
    print("-" * 60)

    # Test Case 3: Topic Relevance Follow-up Check
    orig = "My knee hurts when I climb stairs"
    follow_up = "Should I use an ice pack or a heat patch on it?"
    print(f"[Test 3 Input] Orig: '{orig}' | Follow-up: '{follow_up}'")
    
    is_relevant = check_topic_relevance(follow_up_query=follow_up, original_query=orig)
    print(f"[Topic Relevance Result]: {is_relevant}")
    print(f"Pass Status: {'SUCCESS' if is_relevant is True else 'FAILED'}")
    print("-" * 60)

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        from dotenv import load_dotenv
        load_dotenv()
        
    run_diagnostic_tests()