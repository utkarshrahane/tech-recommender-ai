from state import AgentState
from tools.file_tool import save_report_to_file
from langchain_core.messages import HumanMessage

def summarizer_node(state: AgentState):
    # Rationale: Building a report from Pydantic objects is much cleaner 
    # than parsing messy LLM strings.
    
    report = f"# 📱 Expert {state['request'].category} Report\n\n"
    report += f"**Budget:** {state['request'].budget} INR | **Focus:** {state['request'].priority}\n\n"
    
    report += "## 🏆 Top Recommendations\n"
    for p in state["shortlist"]:
        report += f"### {p.name}\n- **Price:** {p.price}\n- **Pros:** {', '.join(p.pros)}\n\n"
        
    report += "## 📊 Technical Benchmarks\n"
    report += "| Product | Chipset | AnTuTu | Sensor | OIS |\n| :--- | :--- | :--- | :--- | :--- |\n"
    for b in state["benchmarks"]:
        report += f"| {b.product_name} | {b.chipset} | {b.antutu_score} | {b.camera_sensor} | {'✅' if b.ois_support else '❌'} |\n"
        
    # Save the file
    save_report_to_file(report)
    
    return {"final_report": report}
