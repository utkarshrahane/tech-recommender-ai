from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.search_tool import search_tool
from langchain_core.messages import HumanMessage
from state import AgentState, ResearchOutput

# Rationale: Using the 'preview' model for the best reasoning capabilities in 2026
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
structured_researcher = llm.with_structured_output(ResearchOutput)

def researcher_node(state: AgentState):
    # 1. Get current date to ground the search (Prevents Hallucinations)
    current_time = datetime.now().strftime("%B %Y")
    req = state["request"]
    
    # 2. Construct a search query focused on the 'now' of 2026
    query = f"Latest {req.category}s released in India near {current_time}. Budget: {req.budget} INR. Focus: {req.priority}."
    
    # 3. Perform the live search
    search_results = search_tool.invoke({"query": query})
    
    prompt = f"""
    You are an expert tech researcher in {current_time}. 
    Based on these LIVE search results, identify the best {req.category}s: {search_results}
    
    CRITICAL RULES:
    - Only pick phones that are current/released in late 2025 or early 2026.
    - IGNORE older 2024 models (like Nothing 2a or Nord 3).
    - Look for models like 'Nothing Phone (3a) Pro', 'Motorola Edge 60 Pro', and 'Vivo T4 Pro'.
    - Ensure the price is strictly under {req.budget} INR.
    """
    
    # --- FIX: We now explicitly assign the result to 'response' ---
    response = structured_researcher.invoke(prompt)
    
    return {
        "shortlist": response.products,
        "messages": [HumanMessage(content=f"Researcher found {len(response.products)} current models for {current_time}.")]
    }
