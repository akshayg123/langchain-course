import os
import re

from langchain_core.tools import tool
from tavily import TavilyClient

LOG_PATH = r"C:\Users\HP\Documents\dummy_firewall.txt"


# connect to your firewall or create a dummy log file for testing
@tool
def check_firewall_rules(rule: str) -> str:
    """
    Tool that checks if a firewall rule exists in the firewall log file.
    Args:
        rule : The firewall rule to check for
    Returns:
        A message indicating whether the rule exists or not
    """
    print(f"Checking for firewall rule: {rule}")
    if not os.path.exists(LOG_PATH):
        return "Firewall log file does not exist."
    with open(LOG_PATH, "r") as file:
        log_contents = file.read()
    if re.search(re.escape(rule), log_contents):
        return f"The rule '{rule}' exists in the firewall log."
    else:
        return f"The rule '{rule}' does not exist in the firewall log."


@tool
def get_firewall_rows(rule: str) -> str:
    """
    Tool that retrieves all log entries related to a specific firewall rule.
    Args:
        rule : The firewall rule to search for in the log
    Returns:
        All log entries related to the specified rule
    """
    print(f"retrieving log entries for firewall rule: {rule}")
    if not os.path.exists(LOG_PATH):
        return "Firewall log file does not exist."
    with open(LOG_PATH, "r") as file:
        lines = file.readlines()
    matches = [i.strip() for i in lines if re.search(re.escape(rule), i, re.IGNORECASE)]
    if not matches:
        return f"No log entries found for the rule '{rule}'."
    return "\n".join(matches)


@tool
def search_internet(query: str) -> str:
    """
    Tool that searches over the internet
    Args:
        query : The query to search for
    Returns:
        The search results
    """
    tavily = TavilyClient()
    print(f"Searching for: {query}")
    return tavily.search(query=query)
