from langchain_google_genai import ChatGoogleGenerativeAI
from tools.search_tool import search_tool
from langchain_core.messages import HumanMessage
from state import AgentState, BenchmarkOutput

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
structured_benchmarker = llm.with_structured_output(BenchmarkOutput)

def benchmarker_node(state: AgentState):
    # 1. Extract the names of the phones the Researcher/Analyst picked
    names = [p.name for p in state["shortlist"]]
    
    # 2. Specific technical query
    query = f"Technical camera sensor names (Sony/Samsung) and AnTuTu v10 scores for: {', '.join(names)}"
    search_data = search_tool.invoke({"query": query})
    
    prompt = f"""
    Find technical data for ONLY these models: {names}. 
    Data source: {search_data}
    
    Fill out the TechnicalSpecs for each phone. If an AnTuTu score is missing, estimate it based on the chipset (e.g., Snapdragon 7 Gen 4 is ~1M).
    """
    
    # --- FIX: Explicitly assign the structured output to 'response' ---
    response = structured_benchmarker.invoke(prompt)
    
    return {
        "benchmarks": response.specs,
        "messages": [HumanMessage(content="Hardware benchmarks successfully verified and structured.")]
    }
