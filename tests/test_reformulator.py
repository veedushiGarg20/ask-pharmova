# tests/test_reformulator.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.reformulator import reformulate_query

def run_reformulator_test():
    print("Starting Native SDK Reformulator Test...")
    print("-" * 60)

    # Test Input
    sample_query = "what are the symptoms of diabetes?"
    print(f"[Original Input User Prompt]: '{sample_query}'")
    
    
    refined_search_query = reformulate_query(sample_query)
    
    print("-" * 60)
    print(f"[Groq Reformulated Query]: '{refined_search_query}'")
    print("-" * 60)
    
    if refined_search_query != sample_query and len(refined_search_query) > 0:
        print("Pass Status: SUCCESS (Query successfully optimized!)")
    else:
        print("Pass Status: WARNING (Returned original query or blank string)")

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        from dotenv import load_dotenv
        load_dotenv()
        
    run_reformulator_test()