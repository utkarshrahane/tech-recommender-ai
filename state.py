from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    # 'messages' will store the conversation history
    # Annotated with operator.add so new messages are appended, not overwritten
    messages: Annotated[List[str], operator.add]

    # Custom fields for tech recommendation logic
    user_requirements: dict
    shortlisted_products: List[dict]
    benchmarks: List[dict]
    final_recommendation: str
    next_step: str      # Helps the supervisor decide who goes next
    