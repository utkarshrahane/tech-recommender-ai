from langchain_google_genai import ChatGoogleGenerativeAI
from tools.search_tool import search_tool
from langchain_core.messages import HumanMessage
from state import AgentState

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")

def researcher_node(state: AgentState):
    query = state['messages'][0].content 
    
    # Rationale: We ask the tool to get the content of the top articles
    search_data = search_tool.invoke({"query": query})
    
    # We create a prompt to help the Researcher 'read' the text
    # instead of just passing raw JSON.
    reading_prompt = f"""
    You are an expert researcher. I have provided raw search results from tech blogs.
    User Request: {query}
    Raw Data: {search_data}

    Task:
    1. Read through the provided search results and content.
    2. Identify the top 4 smartphones that are consistently rated highly in these articles.
    3. For each phone, extract specific details: Price, Key Camera Specs, and why the reviewer liked it.
    
    Return this as a structured summary for the Analyst.
    """
    
    response = llm.invoke(reading_prompt)
    
    return {
        "messages": [HumanMessage(content=response.content)],
        "next_step": "analyst" 
    }
