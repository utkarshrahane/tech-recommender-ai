import os
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

# Rationale: 'search_depth="advanced"' and 'include_raw_content' 
# forces the tool to find high-quality articles and extract their text.
# tools/search_tool.py
search_tool = TavilySearch(
    max_results=5, 
    search_depth="advanced",
    # We can add 'time_range' if using the latest Tavily API
    # Or simply rely on the 'advanced' depth which prioritizes news
)