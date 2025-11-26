from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor, create_react_agent
#from langchain.agents.react.agent import AgentExecutor, create_react_agent
#from langchain.agents.react.agent import create_react_agent
#from langchain_core.agents import AgentExecutor
from langchain_tavily import TavilySearch
#from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
tools = [TavilySearch()]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)  

structured_llm=llm.with_structured_output(AgentResponse)
#with_structured_output is used to create a new LLM that returns output in a structured format defined by the provided pydantic model
#instead of using PydanticOutputParser, we are using with_structured_output method of the LLM

react_prompt=PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input","agent_scratchpad","tools","tool_names"]
).partial(format_instructions="")


# The agent needs to output text to trigger tools.(so use llm=llm not structured llm)
agent=create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt
)

agent_executer=AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

extract_output=RunnableLambda(
    lambda x: x['output']
)


# Logic: Agent thinks/searches -> Returns Text Answer -> Structured LLM converts Text to Pydantic
chain = agent_executer | extract_output | structured_llm

def main():
    query = (
        "Search for 3 job openings for 'Cloud Security Architect' in India. "
        "IMPORTANT: You must ONLY include jobs that explicitly list the Salary, CTC, or Compensation "
        "(e.g., '20-30 LPA', '50,00,000 INR', etc.) in the search result snippet. "
        "If a job does not mention the money/salary, ignore it and search again. "
        "Provide the Job Title, Company, Salary Amount, and the Source URL."
    )
    result =chain.invoke(
        input={
            "input": query
        }
    )
    print(result)

if __name__ == "__main__":
    main()