🚀 Smart Job Hunter
AI-Powered Job Search Agent (LangChain + Groq + Tavily)
Smart Job Hunter is an intelligent AI agent that acts as a personal technical recruiter. Unlike standard job boards, it performs live web searches to find real-time listings, filters them against a candidate’s specific resume context, and returns structured, actionable results with "fit reasoning."

🔍 The Problem & The Solution
The Problem: Standard job portals flood candidates with irrelevant roles. They don't explain why a job is a good fit, nor do they filter based on granular details like "Must have 2 years of React experience but not Angular."

The Solution: This agent doesn't just keyword match. It:

Searches the live web (using Tavily) for fresh listings.

Reads the Job Description and compares it against your Resume context.

Filters out noise (e.g., senior roles if you are a junior).

Returns Structured Data (JSON) instead of a wall of text.

✨ Key Features
🔎 Live Web Search: Uses Tavily AI to bypass outdated datasets and find current openings.

🤖 Tool-Calling Agent: Built with LangChain, the agent autonomously decides when to search and when to submit final results.

⚡ Blazing Fast Inference: Powered by Groq (Llama-3.3-70b) for near-instant reasoning.

🧩 Structured Output: Uses Pydantic models to force the LLM to return strict JSON data, ensuring the UI renders clean job cards every time.

🎯 Resume-Aware Filtering: The agent is aware of your specific skills (from constants/data.py) and filters jobs accordingly.

🖥️ Interactive UI: A clean Streamlit dashboard to manage parameters and view results.

🧠 Architecture & Workflow
User Input: User selects a role (e.g., "AI Engineer") and Location via Streamlit.

Agent Orchestration: The AgentExecutor receives the prompt + Resume Context.

Step 1 - Search: The agent calls the TavilySearchResults tool to get raw job data.

Step 2 - Reasoning: The LLM filters the raw data based on the resume constraints.

Step 3 - Submission: The agent calls the custom SubmitJobReportTool (Pydantic-validated) to save the final list.

Render: The Streamlit UI parses the structured result and renders job cards.

```
graph LR
    A[User Input] --> B[LangChain Agent];
    B -->|Tool Call| C[Tavily Search];
    C -->|Raw Results| B;
    B -->|Reasoning & Filtering| B;
    B -->|Structured Output| D[SubmitJobReport Tool];
    D -->|Session State| E[Streamlit UI];
```
🛠️ Tech Stack
Language: Python 3.10+

Frontend: Streamlit

Orchestration: LangChain (Community & Core)

LLM Inference: Groq (llama-3.3-70b-versatile)

Search Engine: Tavily AI

Data Validation: Pydantic (v1/v2 compatibility)

Environment: python-dotenv

📂 Project Structure
Plaintext

search_agent/
├── app.py                  # Main application & agent logic (Streamlit)
├── constants/
│   └── data.py             # Resume context & static data
├── models/
│   ├── __init__.py
│   └── schema.py           # Pydantic models for structured output
├── .env                    # API Keys (GitIgnored)
├── pyproject.toml          # Dependencies
└── README.md               # Documentation
🚀 Running Locally
This project uses uv for fast dependency management, but standard pip works too.

1. Clone the Repository
```
git clone https://github.com/YuvrajJais9257/langchain_course_tutorials.git
cd search_agent
```
2. Configure Environment Variables
Create a .env file in the root directory:
```
GROQ_API_KEY=gsk_...
TAVILY_API_KEY=tvly-...
```
3. Install Dependencies
Using uv (Recommended):
```
uv sync
```
Or using standard pip:

```
pip install -r requirements.txt
```
4. Run the Application
```
uv run streamlit run app.py
```
Or:

```
streamlit run app.py
```
⚠️ Versioning Note
This project utilizes LangChain 0.1.x (AgentExecutor). While LangGraph is the newer standard for complex stateful flows, AgentExecutor was chosen here to demonstrate a clean, linear tool-calling pipeline that is easy to understand for resume/portfolio purposes.

🔮 Future Improvements
[ ] Resume Upload: Allow users to upload PDF resumes instead of using a static file.

[ ] Database Integration: Save applied jobs to a SQLite/Postgres database.

[ ] Cover Letter Gen: Add a button to generate a custom cover letter for a selected job.

[ ] Migration: Upgrade from AgentExecutor to LangGraph for more complex loops.

👤 Author
Yuvraj Jaiswal Backend / Full-Stack Engineer Focused on AI Agents, Scalable APIs, and Real-World Systems.