def route_after_analys(state):
    if not state.get("requires_retrieval",True):
        return "generate"
    
    return "retrieve"


# s evidence sufficient?
# Yes
# Return "generate" and produce an answer.

# No
# Check the retrieval attempt count.


# Have we reached the retry limit?
# Yes
# Return "generate" to stop retrying.

# No
# Return "rewrite" to try a better query.

def route_after_evidence(state):

    if state.get("evidence_sufficient", False):
        return "generate"

    if state.get("retrieval_attempt", 0) >= 2:
        return "generate"

    return "rewrite"
 
 
 
#  Validation completed
# The graph calls route_after_validation(state).


# Is grounded true?
# Yes → answer
# The answer passed the grounding check.

# If no

# Have retrieval attempts reached 2?
# Yes → answer
# Stop retrying and proceed to the answer node.

# If no

# Return retry
# Try another retrieval or query-rewriting cycle.





def route_after_validation(state):

    if state.get("grounded", False):
        return "answer"

    if state.get("retrieval_attempt", 0) >= 2:
        return "answer"

    return "retry"
