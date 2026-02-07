from langchain_core.messages import HumanMessage
from tools.file_tool import save_report_to_file
from state import AgentState

def summarizer_node(state: AgentState):
    # 1. Combine all the work done so far
    final_content = f"""
# Tech Recommendation Report (2026)
    
## Analyst Recommendations
{state['messages'][-2].content}

## Technical Benchmarks
{state['messages'][-1].content}
    """
    
    # 2. Use our new tool to save it
    save_report_to_file(final_content)
    
    return {
        "messages": [HumanMessage(content="Final report has been generated and saved to recommendation_report.md")],
        "next_step": "end"
    }
