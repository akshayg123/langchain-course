import os
import os.path
from dotenv import load_dotenv
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt1 import REACT_PROMPT_TEMPLATE
from schemas1 import AgentResponse
from tools1 import get_failed_login_attempts
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


GEMINI_KEY=os.environ["GOOGLE_API_KEY"]

tools=[get_failed_login_attempts]
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)
structured_llm=llm.with_structured_output(AgentResponse)

react_prompt=PromptTemplate(
    template=REACT_PROMPT_TEMPLATE,
    input_variables=["tools","tool_names","input","agent_scratchpad"]
).partial(format_instructions="")


agent=create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt
)

agent_executor=AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

chain=agent_executor | structured_llm


def main():
    query="Fetch today's failed login attempts from Splunk and summarize suspicious IPs and hosts with recommendations"
    
    result = chain.invoke({
        "tools": "get_failed_login_attempts: Fetches IPs, hosts, and accounts with failed logins from Splunk.",
        "tool_names": "get_failed_login_attempts",
        "format_instructions": "Provide structured report: summary, suspicious IPs/hosts, likely attack pattern, recommended actions",
        "input": query,
        "agent_scratchpad": ""
    })

if __name__=="__main__":
    main()




