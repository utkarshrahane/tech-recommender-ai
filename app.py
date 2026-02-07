import streamlit as st
import pandas as pd
from graph import app
from state import ProductRequest
from langchain_core.messages import HumanMessage
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Tech Scout AI", 
    page_icon="📱", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.title("🕵️‍♂️ Tech Scout: Expert Recommendations")
st.caption("A Multi-Agent System powered by LangGraph & Gemini 3")

# --- Main Input Form ---
with st.container():
    st.subheader("📋 Configure Your Search")
    with st.form("scout_form", border=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            product_type = st.selectbox("Product Category", ["Smartphone"], index=0)
        with col2:
            budget = st.select_slider(
                "Maximum Budget (INR)",
                options=[10000, 15000, 20000, 25000, 30000, 40000, 50000, 75000, 100000],
                value=30000
            )
        with col3:
            priority = st.selectbox(
                "Primary Priority", 
                ["Camera Performance", "Gaming & Speed", "Battery Endurance", "Balanced All-Rounder"]
            )
        
        submit_button = st.form_submit_button(label="🚀 Generate Analysis", use_container_width=True)

# --- Logic & Agent Execution ---
if submit_button:
    try:
        # 1. Pydantic Validation (Step 1 of our robust pipeline)
        user_req = ProductRequest(
            category=product_type,
            budget=budget,
            priority=priority
        )

        # 2. State Initialization
        inputs = {
            "request": user_req,
            "messages": [],
            "shortlist": [],
            "benchmarks": []
        }

        # 3. Visual Feedback: Agent Progress
        with st.status("🛠️ System Initializing...", expanded=True) as status:
            final_state = None
            
            # Streaming the graph execution
            for output in app.stream(inputs):
                for node_name, state_update in output.items():
                    status.write(f"✅ **{node_name.capitalize()} Agent** has finished.")
                    # Capture the latest state to extract Pydantic objects later
                    final_state = state_update 
            
            status.update(label="✨ Analysis Complete!", state="complete", expanded=False)

        # 4. Display Results in Tabs (The "Senior Developer" UI approach)
        tab1, tab2, tab3 = st.tabs(["📄 Recommendations", "📊 Technical Comparison", "📈 Charts"])

        # Fetch data from the generated files or state
        report_path = "recommendation_report.md"
        
        with tab1:
            if os.path.exists(report_path):
                with open(report_path, "r", encoding="utf-8") as f:
                    report_content = f.read()
                    st.markdown(report_content)
                    
                    st.download_button(
                        label="💾 Download Report (Markdown)",
                        data=report_content,
                        file_name=f"{product_type.lower()}_report.md",
                        mime="text/markdown"
                    )
            else:
                st.error("Report generation failed. Please check agent logs.")

        with tab2:
            st.subheader("Validated Hardware Benchmarks")
            # We access the 'benchmarks' key from the shared state
            # Note: In a real run, you'd pull this from the final state object
            # For this demo, let's assume final_state contains the latest benchmarks
            if "benchmarks" in final_state and final_state["benchmarks"]:
                df = pd.DataFrame([b.model_dump() for b in final_state["benchmarks"]])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Searching for technical benchmarks...")

        with tab3:
            st.subheader("Performance Visualization")
            if "benchmarks" in final_state and final_state["benchmarks"]:
                # Rationale: Visualizing AnTuTu scores helps the user make a quick decision
                chart_data = pd.DataFrame([
                    {"Product": b.product_name, "AnTuTu Score": b.antutu_score} 
                    for b in final_state["benchmarks"] if b.antutu_score
                ])
                if not chart_data.empty:
                    st.bar_chart(chart_data.set_index("Product"))
                else:
                    st.warning("Synthetic scores not available for these specific models.")

    except Exception as e:
        st.error(f"Configuration Error: {str(e)}")

# --- Footer ---
st.divider()
st.caption("Built with ❤️ using LangGraph, Pydantic, and Gemini 3 Flash Preview")