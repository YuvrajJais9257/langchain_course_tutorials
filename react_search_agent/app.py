from dotenv import load_dotenv
load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

# Tool
tools = [TavilySearchResults(max_results=3)]

# LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

# Prompt from LangChain Hub
react_prompt = hub.pull("hwchase17/react")

# Create ReAct agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

# Smoke test
result = agent_executor.invoke(
    {"input": "Who created LangChain and what problem does it solve?"}
)

print("\n" + "="*50)
print("FINAL ANSWER:")
print("="*50)
print(result["output"])