from typing import Tuple, List, Optional
from agents import jira_agent, gherkin_agent, script_agent, coverage_agent
from memory import save_memory, retrieve_memory, init_db


def _build_historical_context(past_data: Optional[List[tuple]]) -> str:
    """Formats past memory arrays into a string context."""
    if not past_data:
        return ""
    
    # Efficient string concatenation using list comprehension
    return "".join(f"\nPrevious Feature: {row[1]}\n" for row in past_data)


def _generate_and_validate_gherkin(base_feature: str, enhanced_feature: str, max_retries: int = 1) -> Tuple[str, str]:
    """
    ReAct Loop: Generates Gherkin script, analyzes coverage, and conditionally improves.
    """
    current_feature = enhanced_feature
    
    for attempt in range(max_retries + 1):
        # ACT
        gherkin = gherkin_agent(current_feature)
        # OBSERVE
        coverage = coverage_agent(base_feature, gherkin)
        
        # Check for coverage gaps
        coverage_text = coverage.lower()
        needs_improvement = "missing" in coverage_text or "not covered" in coverage_text
        
        # Stop early if the coverage is perfectly fine
        if not needs_improvement:
            break
            
        # THINK / IMPROVE: Refine feature input for the next iteration
        if attempt < max_retries:
            current_feature += "\nInclude edge cases and missing scenarios."

    return gherkin, coverage


def run_pipeline(ticket_id: str) -> Tuple[str, str, str, str]:
    """
    Orchestrates the feature extraction, Gherkin generation, and script writing pipeline.
    """
    # Step 0: Initialize DB
    init_db()

    # Step 1 & 2: Fetch and build context
    feature = jira_agent(ticket_id)
    past_data = retrieve_memory(ticket_id)
    enhanced_feature = feature + _build_historical_context(past_data)

    # Step 3, 4, & 5: Execute ReAct loop for Gherkin and Coverage
    gherkin, coverage = _generate_and_validate_gherkin(
        base_feature=feature, 
        enhanced_feature=enhanced_feature
    )

    # Step 6: Generate final script
    script = script_agent(gherkin)

    # Step 7: Update Memory
    save_memory({
        "ticket": ticket_id,
        "feature": feature,
        "gherkin": gherkin,
        "script": script
    })

    return feature, gherkin, script, coverage
