REACT_PROMPT_TEMPLATE="""
Answer the following questions as best you can. You have access to the following tools:

{tools}

You must use the following format:

Question: the input question you must answer
Thought: [Your step-by-step reasoning about the question, the necessary tools, and the next action to take.]
Action: the name of the tool to use, must be one of [{tool_names}]
Action Input: the input to the tool (a single string)
Observation: [The result of the tool's execution, which will be provided to you]
... (this Thought/Action/Observation block can repeat multiple times)

When you have determined the final answer to the user's question, or if you cannot use any more tools, you MUST use the Final Answer format.

Thought: I now know the final answer.
Final Answer: the final answer to the original input question formatted according to format_instructions :{format_instructions}

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""