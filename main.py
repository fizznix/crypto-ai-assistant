from utils.rate_limiter import check_rate_limit
from utils.llm import call_llm
from utils.agent import SimpleAgent
from config import MODEL
from prompts import SYSTEM_PROMPT
from utils.logger import logger 

def process_user_query(agent: SimpleAgent, user_input: str):
    """
    Processes the user's query by sending it to the LLM and handling the response.

    Args:
        agent (SimpleAgent): The agent handling the conversation.
        user_input (str): The user's input query.
    """
    # Format the user message and append it to the agent's messages
    user_message = agent.get_llama_message_format("user", user_input)
    agent.messages.append(user_message)

    # Call the LLM with the user's message
    response = call_llm(
        model=MODEL,
        messages=agent.messages,
        tools=agent.tools,
        tool_choice="auto"
    )

    # Format the agent's response and log the tool calls
    agent_response = agent.get_llama_message_format(response.choices[0].message.role, response.choices[0].message.content)
    logger.debug(f"Tools to be called - {response.choices[0].message.tool_calls}")

    # Parse the tool response from the LLM's response
    parsed_response = agent.parse_tool_response(response.choices[0].message)

    if parsed_response:
        # Handle each tool call in the parsed response
        for tool_call in parsed_response:
            agent.messages = agent.handle_tool_response(tool_call, agent.messages)
            logger.debug("Tool response: %s", agent.messages[-1]["content"])

            # Call the LLM again with the updated messages
            res = call_llm(
                model=MODEL,
                messages=agent.messages,
            )
            agent_response = agent.get_llama_message_format(res.choices[0].message.role, res.choices[0].message.content)
            agent.messages.append(agent_response)
            logger.debug("Answer from the agent: %s", res.choices[0].message.content)
    else:
        # If no tool call is found, append the agent's response to the messages
        agent.messages.append(agent_response)
        logger.debug("No function call found in the response")
        logger.debug(agent_response['content'])

def main():
    """
    The main function to run the agent and process user queries in a loop.
    """
    agent = SimpleAgent()
    system_prompt = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
    agent.messages.append(system_prompt)

    while True:
        user_input = input("Enter your query: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        check_rate_limit()
        process_user_query(agent, user_input)

if __name__ == "__main__":
    main()