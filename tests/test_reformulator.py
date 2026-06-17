# tests/test_reformulator.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.reformulator import reformulate_query

def run_reformulator_test():
    print("Starting Native SDK Reformulator Test...")
    print("-" * 60)

    # Test Input
    sample_query = "What are the common side effects of Metformin and can I take it with Jardiance?"
    print(f"[Original Input User Prompt]: '{sample_query}'")
    refined_search_query = reformulate_query(sample_query)
    print("-" * 60)
    print(f"Reformulated Queries]: '{refined_search_query}'")
    print("-" * 60)
    
    mock_critic_gap = "missing information regarding drug-drug interactions between Metformin and Jardiance"
    corrective_queries = reformulate_query(sample_query, missing_info=mock_critic_gap)
    print("-" * 60)
    print(f"Corrective Queries]: '{corrective_queries}'")

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        from dotenv import load_dotenv
        load_dotenv()
        
    run_reformulator_test()