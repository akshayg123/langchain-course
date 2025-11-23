import json
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
load_dotenv()



#doc strings(multi-line commends) are important for tools to describe their functionality



tavily=TavilyClient()
@tool
def search(query: str) -> str:
    """
    Tool that searches over the internet
    Args:
        query : The query to search for
    Returns:
        The search results
    """


    print(f"Searching for: {query}")
    return tavily.search(query=query)


llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
tools=[search]
agent=create_agent(
    model=llm,
    tools=tools
)
def main():
    print("Hello from main2.py!")
    result= agent.invoke(
        {
            "messages":HumanMessage(content="search for 3 job postings for ai engineer using langchain in india on linkedln and list their details")
        }
    )
    print(result)




if __name__ == "__main__":
    main()  