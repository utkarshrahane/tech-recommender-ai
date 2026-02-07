from langgraph.graph import StateGraph, END
from state import AgentState
from agents.researcher import researcher_node
from agents.analyst import analyst_node
from agents.benchmarker import benchmarker_node
from agents.summarizer import summarizer_node

workflow = StateGraph(AgentState)

# 2. Register the nodes (The 'Workers')
workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("benchmarker", benchmarker_node)
workflow.add_node("summarizer", summarizer_node)

workflow.set_entry_point("researcher")

workflow.add_edge("researcher", "analyst") 
workflow.add_edge("analyst", "benchmarker")
workflow.add_edge("benchmarker", "summarizer")
workflow.add_edge("summarizer", END)

app = workflow.compile()