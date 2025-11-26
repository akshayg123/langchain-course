from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
#from langchain.agents import create_agent
from langchain_classic.agents import AgentExecutor, create_react_agent  
from langchain_tavily import TavilySearch
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse

#PromptTemplate is used for creating prompt templates with variable placeholders
#RunnableLambda is used to create a runnable that executes a lambda function
#PydanticOutputParser is used to parse the output of the agent into a pydantic model

load_dotenv()
tools=[TavilySearch()]
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)
output_parser=PydanticOutputParser(pydantic_object=AgentResponse)

react_prompt=PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input","agent_scratchpad","tools","tool_names"]).partial(format_instructions=output_parser.get_format_instructions())

# .partial is used to create a new PromptTemplate with some variables pre-filled

agent=create_react_agent(
    llm=llm,  
    tools=tools,
    prompt=react_prompt
)
# AgentExecutor is used to create an executor that runs the agent with the provided tools
agent_executor=AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

#extract_output returns x['output'] from the final result
extract_output=RunnableLambda(
    lambda x: x['output']
)

#parse_output takes x['output'] and returns it in a structured format using output_parser
parse_output=RunnableLambda(
    lambda x: output_parser.parse(x)
)

#here output of previous one is next one's input and so on(chaining)
chain=agent_executor | extract_output | parse_output




def main():
    result=chain.invoke(
        input={
            "input":"Search 3 job openings for cloud security architects in india and provide the URLs of the sources used",
        }

    )
    print(result)
    print("----------------------------Parsed Output----------------------------")
    print("Final Answer: ", result['output'])

if __name__=="__main__":
    main()