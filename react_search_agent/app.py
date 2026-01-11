from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers import PydanticOutputParser
from schemas import AgentResponse

#brain
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)

#tools
search_tool = TavilySearchResults(max_results=5)

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS

#prompt
react_prompt = hub.pull("hwchase17/react")
output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input","agent_scratchpad","tool_names"]
).partial(format_instructions=output_parser.get_format_instructions())

#agent
react_agent=create_react_agent(
    llm=llm,
    tools=[search_tool],
    prompt=react_prompt_with_format_instructions,
)

react_agent_executor = AgentExecutor(
    agent=react_agent,
    tools=[search_tool],
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

#test_run
result=react_agent_executor.invoke(
    {"input": "Find the latest AI Engineer job openings and provide links to apply."}
)

print("\n" + "="*50)
print("FINAL ANSWER:")
print("="*50)
print(result["output"])