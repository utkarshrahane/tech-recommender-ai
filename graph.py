from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from state import AgentState

# Initializing the 'brain'
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def supervisor_node(state: AgentState):
    # logic for the supervisor to look at 'messages' and 'next_step'
    # and return the name of the next agent to call.
    pass

# Initialize the Graph
workflow = StateGraph(AgentState)
# Add nodes for each agent