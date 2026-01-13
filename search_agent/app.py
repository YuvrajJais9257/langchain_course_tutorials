import streamlit as st
import os
from dotenv import load_dotenv
from constants.data import RESUME_CONTEXT

# --- LangChain Imports ---
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool, tool, BaseTool
from typing import Type, List
# from tavily import TavilyClient
# from langchain_tavily import TavilySearch
from models.schema import AgentResponse, Source

load_dotenv()

# --- Setup Session State for Results ---
if "agent_result" not in st.session_state:
    st.session_state.agent_result = None
if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ GROQ_API_KEY is missing from your .env file!")
    st.stop()
if not os.getenv("TAVILY_API_KEY"):
    st.error("⚠️ TAVILY_API_KEY is missing. Get one at tavily.com!")
    st.stop()

# --- Streamlit UI Setup ---

st.set_page_config(
    page_title="Job Search Agent with Tavily",
    page_icon="🚀",
    layout="wide",
)
st.title("🚀 Smart Job Hunter")
st.markdown(
    """
    This app uses Groq's LLM and Tavily's web search to find job postings
    that match your skills and career goals.
    """
)

# Sidebar for controls

with st.sidebar:
    st.header("Search Parameters")

    target_role = st.selectbox(
        "Target Role",
        [
            "Full Stack Engineer (MERN/Python)", # Most occurring job title
            "GenAI Application Developer",       # Highest growth for <2yrs exp
            "DevOps & Platform Engineer",        # High demand in GCCs
            "Cloud Security Associate",          # Critical scarcity role
            "Data & Analytics Engineer",         # Replacement for traditional Analyst
            "QA Automation Specialist"           # Strong demand in product firms
        ]
    )

    location = st.text_input("Location", value="Remote", placeholder="e.g., Remote, Bangalore")
    
    additional_filters = st.text_input(
        "Extra Filters", 
        placeholder="e.g., 'Series A startup', 'Must use LangChain'"
    )

    st.markdown("---")
    search_button = st.button("🔍 Find Opportunities", type="primary", use_container_width=True)

# --- Final Answer Tool ---
# @tool
# def save_search_results(answer:str, source:list):
#     """
#     Call this tool only when you have found the job postings.
#     It submits the final report to the user.
#     """
#     try:
#         validated_sources=[Source(**s) if isinstance(s, dict) else s for s in source]
#         response_obj = AgentResponse(answer=answer, source=validated_sources)
#         return "Results submitted successfully."
#     except Exception as e:
#         return f"Error saving results: {str(e)}"

class SubmitJobReportTool(BaseTool):
    name: str = "submit_job_report"
    description: str = "Submit the final job search results including the summary and list of sources."
    args_schema: Type[AgentResponse] = AgentResponse

    def _run(self, answer: str, source: List):
        """
        The method that runs when the agent calls the tool.
        """
        try:
            # 'source' usually comes in as a list of dictionaries. 
            # We convert them to Source objects for consistency if needed.
            validated_sources = []
            for s in source:
                if isinstance(s, dict):
                    validated_sources.append(Source(**s))
                else:
                    validated_sources.append(s)
            
            response_obj = AgentResponse(answer=answer, source=validated_sources)
            
            # SAVE TO SESSION STATE
            st.session_state.agent_result = response_obj
            return "Results submitted successfully."
        except Exception as e:
            return f"Error saving results: {str(e)}"

# Instantiate the tool
submit_tool = SubmitJobReportTool()

# ---  Main Logic ---
if search_button:
    with st.spinner(f"Searching active listings for {target_role}..."):
        try:
            search_tool=TavilySearchResults(max_results=5)
            tools=[search_tool, submit_tool]
            llm = ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"),
                model="llama-3.3-70b-versatile",
                temperature=0.1,
            )

            prompt = ChatPromptTemplate.from_messages([
            ("system", """
                You are a junior-tech job search assistant.

                TASK:
                - Find 5 junior (0–2 years) job listings matching the user's role and location.
                - Prefer "Junior", "Entry Level", or "Associate" titles.

                RULES:
                - Exclude Senior, Lead, or 3+ years roles.
                - Once 5 jobs are found, submit the report immediately.
            """),
                ("human", "{user_query}"),
                ("placeholder", "{agent_scratchpad}"),
            ])

            agent =create_tool_calling_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,    max_iterations=5)

            query_str = (
              f"Find active job postings for '{target_role}' in '{location}'. "
              f"Focus on 'Junior', 'Entry Level', or 'Associate' roles. "
              f"Search for '0-2 years experience' or 'max 2 years experience'. "
              f"Exclude roles requiring 'Senior', 'Lead', or '5+ years'. "
              f"{additional_filters}"
            )
            # response= agent_executor.invoke({
            #     "resume_data": RESUME_CONTEXT,
            #     "role": target_role,
            #     "location": location,
            #     "user_query": query_str
            # })
            
            agent_executor.invoke({
                "resume_data": RESUME_CONTEXT,
                "role": target_role,
                "location": location,
                "user_query": query_str
            })

            # st.success("✅ Search Complete!")
            # st.markdown("### Here are the job postings I found for you:")
            # st.markdown(response['output'])

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            
if st.session_state.agent_result:
    result = st.session_state.agent_result
    
    st.success("✅ Search Complete!")
    
    # Render the summary
    st.markdown("### 📝 Agent Summary")
    st.info(result.answer)
    
    # Render the jobs as specific UI elements (Cards/Expanders)
    st.markdown("### 🔗 Found Opportunities")
    
    # Now we can iterate programmatically!
    for idx, src in enumerate(result.source):
        with st.expander(f"Job {idx+1}: {src.title or 'View Job'}"):
            st.write(f"**Source URL:** {src.url}")
            st.link_button("Apply Now 🚀", src.url)

else:
    st.info("👈 Select a role in the sidebar and click **Find Opportunities** to start.")

# tavily = TavilyClient()

# @tool
# def search(query: str) -> str:
#     """
#     Search the web for up-to-date information based on a user query.
#     Use this tool when the question requires current or factual data.
#     """
#     print(f"[TOOL] Searching the web for: {query}")
#     return tavily.search(query=query, num_results=3)

# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     model="llama-3.3-70b-versatile",
#     temperature=0.7,
# )
# tools=[TavilySearch()]
# agent = create_agent(model=llm, 
#                         #  tools=[search]
#                         tools=tools
#                      )

# def main():
#     result = agent.invoke({
#         "messages": [
#             HumanMessage(
#                 content=(
#                     "Find 3 AI Engineer job postings in the Bay Area "
#                     "that mention LangChain. "
#                     "List job title, company, location, and a brief description."
#                 )
#             )
#         ]
#     })

#     print(result["messages"][-1].content)

# if __name__ == "__main__":
#     main()
