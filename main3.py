from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from tools import check_firewall_rules, get_firewall_rows
from dotenv import load_dotenv
load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
tools=[check_firewall_rules, get_firewall_rows]
agent=create_agent(
    model=llm,
    tools=tools
)



def main():
    print("firewall agent is running!")
    print("1. Check Firewall Rule")
    print("2. Get Firewall Rows")
    print("type 'exit' to quit")
    while True:
        option=input("Select an option (1 or 2): ") 
        if option.lower() == 'exit':
            print("Exiting the firewall agent.")
            break
        if option not in ['1', '2']:
            print("Invalid option. Please select 1 or 2.")
            continue
        rule=input("Enter the firewall rule to check: ")
        if option =="1":
            query=f"Check if the firewall rule '{rule}' exists in the firewall log."
        else:
            query=f"Retrieve all log entries related to the firewall rule '{rule}'."
        result=agent.invoke(
            {
                "messages": [
                    {
                    "role":"user",
                    "content":query
                    }
                ]
            }
        )
        print("\nresult:\n" , result,"\n")
        print("------------------------------------------------------------------------------")
        print(result["messages"][-1])



if __name__ == "__main__":
    main()