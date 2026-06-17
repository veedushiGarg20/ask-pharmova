import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.critic import evaluate_context

def run_critic_test():
    print("Running Native Critic Node Standalone Audit Test...")
    print("=" * 70)
    
    query = "What are the side effects of Metformin and can I take it with Jardiance?"
    
    bad_context = "[1] Metformin is highly effective. Common side effects include gastrointestinal distress, bloating, and gas."
    
    print(f"Query: '{query}'")
    print(f"Mock Context: '{bad_context}'")
    print("Evaluating coverage sufficiency...")
    
    evaluation = evaluate_context(query, bad_context)
    print("\nCritic Output Object:")
    print(evaluation)
    
    if evaluation["sufficient"] is False and "Jardiance" in evaluation["missing_info"]:
        print("\nPass Status: SUCCESS! The critic correctly identified the missing clinical information gap.")
    else:
        print("\nPass Status: FAILED. The critic failed to accurately spot the text deficit.")

if __name__ == "__main__":
    run_critic_test()