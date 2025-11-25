from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import check_firewall_rules, get_firewall_rows, search_internet

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
tools = [check_firewall_rules, get_firewall_rows, search_internet]
agent = create_agent(model=llm, tools=tools)


def main():
    print("Agent is running!")
    print("1. Check Firewall Rule")
    print("2. Get Firewall Rows")
    print("3. Search Internet")
    print("type 'exit' to quit")
    while True:
        option = input("Select an option (1 or 2 or 3): ")
        if option.lower() == "exit":
            print("Exiting the firewall agent.")
            break
        if option not in ["1", "2", "3"]:
            print("Invalid option. Please select 1, 2, or 3.")
            continue
        if option == "1":
            rule = input("Enter the firewall rule to check: ")
            query = f"Check if the firewall rule '{rule}' exists in the firewall log."
        elif option == "2":
            rule = input("Enter the firewall rule to check: ")
            query = f"Retrieve all log entries related to the firewall rule '{rule}'."
        elif option == "3":
            query = input("Enter the search query: ")
        result = agent.invoke({"messages": [{"role": "user", "content": query}]})
        print("\nresult:\n", result, "\n")
        print(
            "------------------------------------------------------------------------------"
        )
        print(result["messages"][-1])


if __name__ == "__main__":
    main()
