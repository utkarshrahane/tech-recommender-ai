import os
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

# Rationale: 'search_depth="advanced"' and 'include_raw_content' 
# forces the tool to find high-quality articles and extract their text.
search_tool = TavilySearch(
    k=3, 
    search_depth="advanced", 
    include_raw_content=True
)