# pipeline/orchestrator.py
import time
from pipeline.classifier import classify_query
from pipeline.reformulator import reformulate_query
from pipeline.retriever import retrieve
from pipeline.assembler import assemble_context
from pipeline.critic import evaluate_context
from config import REDIRECT_MESSAGE

def run_agentic_rag(prompt: str, max_loops: int = 2):
    """
    Orchestrates the agentic RAG loop using a state-driven while loop.
    Yields status dictionary updates so the Streamlit UI can render live progress trees.
    """
    
    state = {
        "original_query": prompt,
        "search_queries": [],
        "context_block": "",
        "source_map": {},
        "loop_count": 0,
        "sufficient": False,
        "missing_info": "",
        "status": "processing",
        "redirect": False
    }

    yield {"step": "classifying", "message": "Analyzing medical query intent...", "state": state}
    is_medical = classify_query(prompt)
    
    if not is_medical:
        state["redirect"] = True
        state["status"] = "redirected"
        yield {"step": "redirect", "message": REDIRECT_MESSAGE, "state": state}
        return

    yield {"step": "decomposing", "message": "Deconstructing multi-context clinical topics...", "state": state}
    state["search_queries"] = reformulate_query(prompt) # missing_info defaults to None

    while state["loop_count"] < max_loops:
        current_loop = state["loop_count"] + 1
        
        yield {
            "step": f"retrieving_loop_{current_loop}", 
            "message": f"Searching medical sources (Attempt {current_loop}/{max_loops})...", 
            "state": state
        }
        raw_docs = retrieve(state["search_queries"])
        
        new_context, new_sources = assemble_context(raw_docs)
        if new_context:
            state["context_block"] += "\n\n" + new_context
            state["source_map"].update(new_sources)

        yield {
            "step": f"evaluating_loop_{current_loop}", 
            "message": f"Auditing context block for factual coverage (Attempt {current_loop}/{max_loops})...", 
            "state": state
        }
        evaluation = evaluate_context(state["original_query"], state["context_block"])
        
        state["sufficient"] = evaluation["sufficient"]
        state["missing_info"] = evaluation["missing_info"]

        if state["sufficient"]:
            yield {
                "step": "loop_complete", 
                "message": "Factual context verified successfully. Synthesizing answer...", 
                "state": state
            }
            break

        state["loop_count"] += 1
        if state["loop_count"] < max_loops:
            yield {
                "step": f"correcting_loop_{current_loop}", 
                "message": f"Information gap detected regarding: '{state['missing_info']}'. Refining search criteria...", 
                "state": state
            }
            state["search_queries"] = reformulate_query(prompt, missing_info=state["missing_info"])
            
    state["status"] = "complete"
    yield {"step": "finished", "message": "Context gathering complete.", "state": state}