from langchain_google_genai import ChatGoogleGenerativeAI
from tools.search_tool import search_tool
from langchain_core.messages import HumanMessage
from state import AgentState

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")

def benchmarker_node(state: AgentState):
    # 1. Get the specific names from the Analyst's message
    analyst_report = state['messages'][-1].content
    
    # Rationale: We explicitly tell the search tool to only look for 
    # benchmarks for the specific phones mentioned in the previous report.
    specific_query = f"Technical camera sensor specs, AnTuTu, and Geekbench scores for ONLY: {analyst_report}"
    raw_data = search_tool.invoke({"query": specific_query})
    
    prompt = f"""
    You are a Technical Hardware Specialist.
    Analyst's Picks: {analyst_report}
    Technical Data Found: {raw_data}
    
    Task:
    - Provide a Technical Score (1-100) for ONLY the phones picked by the Analyst.
    - Focus on: AnTuTu v10 scores, Camera Sensor names (e.g., Sony LYT-700C), and OIS availability.
    - If you can't find the phone's score, search for the score of the chipset inside it.
    
    Format as a clean technical table followed by a 2-sentence specialist verdict.
    """
    
    response = llm.invoke(prompt)
    
    return {
        "messages": [HumanMessage(content=response.content)],
        "next_step": "end"
    }