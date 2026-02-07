import os
from dotenv import load_dotenv
from graph import app  # This is the 'compiled' workflow from graph.py
from langchain_core.messages import HumanMessage

# 1. Load your API keys from the .env file
load_dotenv()

def run_recommender(user_query: str):
    # 2. Prepare the Initial State (The first page of our 'Notepad')
    # Rationale: We must provide the keys defined in state.py so the agents
    # know what they are working with.
    inputs = {
        "messages": [HumanMessage(content=user_query)],
        "user_requirements": {},
        "shortlisted_products": [],
        "benchmarks": [],
        "final_recommendation": "",
        "next_step": ""
    }

    print(f"\n--- 🚀 Starting Agentic Research for: '{user_query}' ---\n")
    
    # 3. Stream the execution
    # Rationale: 'app.stream' allows us to see the output of each node as it finishes.
    # This is much better for debugging than waiting for the whole thing to end.
    for output in app.stream(inputs):
        for node_name, state_update in output.items():
            print(f"\n✅ Node '{node_name}' finished.")
            if "messages" in state_update:
                last_msg = state_update["messages"][-1]
                
                # Handle list-style content blocks from Gemini
                if isinstance(last_msg.content, list):
                    text_content = last_msg.content[0].get('text', '')
                else:
                    text_content = last_msg.content
                    
                print(f"REPORT:\n{text_content}")
                print("-" * 50)

if __name__ == "__main__":
    # Test input: You can change this to any tech product!
    test_query = "Find me a smartphone under 30000 INR with the best camera performance."
    run_recommender(test_query)
    