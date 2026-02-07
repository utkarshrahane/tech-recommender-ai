import streamlit as st
from graph import app
from langchain_core.messages import HumanMessage
import os

# --- Page Config ---
st.set_page_config(page_title="Tech Scout 2026", page_icon="📱", layout="centered")

st.title("🕵️‍♂️ Tech Scout: Expert Recommendations")
st.markdown("Select your requirements and let the agentic team do the heavy lifting.")

# --- The Input Form ---
# Rationale: st.form groups widgets together so the page doesn't rerun on every click.
with st.form("scout_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        product_type = st.selectbox("Product", ["Smartphone"], index=0)
        budget = st.slider("Budget (INR)", 10000, 150000, 30000, step=1000)
    
    with col2:
        priority = st.selectbox(
            "Primary Focus", 
            ["Camera Performance", "Gaming & Speed", "Battery Life", "Balanced"]
        )
        # We can add a simple checkbox for specific 'Expert' modes
        include_benchmarks = st.checkbox("Include Technical Benchmarks", value=True)

    # The magic button
    submit_button = st.form_submit_button(label="🚀 Generate Expert Report")

# --- Agent Execution ---
if submit_button:
    # 1. Clear previous results from the screen
    st.divider()
    
    # 2. Run the Workflow
    with st.status(f"Agents are scouting for the best {product_type}...", expanded=True) as status:
        
        # We build the instruction solely from our 'grounded' inputs
        instruction = f"Recommend the best {product_type} under {budget} INR. Focus: {priority}."
        
        inputs = {"messages": [HumanMessage(content=instruction)]}
        final_report = ""
        
        for output in app.stream(inputs):
            for node_name, state_update in output.items():
                status.write(f"✅ **{node_name.title()}** complete.")
                
                if node_name == "summarizer":
                    if os.path.exists("recommendation_report.md"):
                        with open("recommendation_report.md", "r") as f:
                            final_report = f.read()
        
        status.update(label="Report Generated!", state="complete", expanded=False)

    # 3. Display the Output
    if final_report:
        st.success("Your recommendation is ready!")
        st.markdown(final_report)
        
        # Download option
        st.download_button(
            label="💾 Save Report as Markdown",
            data=final_report,
            file_name=f"{product_type.lower()}_report.md",
            mime="text/markdown"
        )