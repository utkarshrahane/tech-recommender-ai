from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from state import AgentState

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")

def analyst_node(state: AgentState):
    # This remains similar, but the input data is now much higher quality
    user_query = state['messages'][0].content
    detailed_research = state['messages'][-1].content

    prompt = f"""
    You are the Senior Value Analyst.
    User Query: {user_query}
    Research Summary: {detailed_research}

    Based on the research, pick the final TOP 3 products. 
    Explain why these 3 provide the 'Best Value for Money' compared to others.
    Format it as a clean report.
    """
    
    response = llm.invoke(prompt)
    
    return {
        "messages": [HumanMessage(content=response.content)],
        "next_step": "end"
    }
