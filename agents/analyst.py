from langchain_google_genai import ChatGoogleGenerativeAI
from state import AgentState, ScoutedProduct
from typing import List
from pydantic import BaseModel

# We define a temporary container for the LLM output
class AnalystOutput(BaseModel):
    top_picks: List[ScoutedProduct]
    rationale: str

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
# Rationale: This 'binds' the model to the Pydantic schema
structured_llm = llm.with_structured_output(AnalystOutput)

def analyst_node(state: AgentState):
    # Rationale: Gemini now returns an ACTUAL object, not a string
    res = structured_llm.invoke(f"Analyze these for a {state['request'].budget} budget: {state['messages'][-1]}")
    
    return {
        "shortlist": res.top_picks,
        "messages": [f"Selected {len(res.top_picks)} products based on value."],
        "next_step": "benchmarker"
    }