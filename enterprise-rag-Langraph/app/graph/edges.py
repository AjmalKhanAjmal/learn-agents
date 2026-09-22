def route_after_analysis(state):

    if not state.get("requires_retrieval", True):
        return "generate"

    return "retrieve"


def route_after_evidence(state):

    if state.get("evidence_sufficient", False):
        return "generate"

    if state.get("retrieval_attempt", 0) >= 2:
        return "generate"

    return "rewrite"
 

def route_after_validation(state):

    if state.get("grounded", False):
        return "answer"

    if state.get("retrieval_attempt", 0) >= 2:
        return "answer"

    return "retry"
