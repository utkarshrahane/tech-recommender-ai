# Agentic Tech Recommender

A Multi-Agent System (MAS) built with **LangGraph** and **Gemini 1.5** that acts as a personalized tech consultant.

## 🤖 Architecture
The system uses a Supervisor-Worker pattern to:
1. **Research:** Scrape latest tech blogs and YouTube reviews.
2. **Benchmark:** Extract technical performance data.
3. **Analyze:** Evaluate "Value for Money" and recommend the Top 3 products.

## 🛠️ Tech Stack
- **Framework:** LangGraph (Stateful Multi-Agent orchestration)
- **LLM:** Google Gemini 1.5 (via Google AI Studio)
- **Search:** Tavily AI (Agent-optimized search)
- **Language:** Python 3.10+

## 🚀 Getting Started
1. Clone the repo: `git clone <your-repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `GOOGLE_API_KEY` and `TAVILY_API_KEY` to a `.env` file.
4. Run: `python main.py`