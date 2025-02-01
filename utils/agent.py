import json
from typing import List
from together.types.chat_completions import ChatCompletionMessage
from utils.tools import AVAIALBLE_TOOLS_FORMAT, get_coin_price, translate_to_english
from prompts import TOOL_RESPONSE_SYSTEM_PROMPT

class SimpleAgent:
    """
    A simple agent that handles tool responses and formats messages.
    """
    def __init__(self):
        """
        Initializes the SimpleAgent with available tools and an empty message list.
        """
        self.tools = self.get_tools()
        self.messages = []

    def get_tools(self):
        """
        Returns the available tools format.

        Returns:
            dict: The available tools format.
        """
        return AVAIALBLE_TOOLS_FORMAT
    
    def get_llama_message_format(self, role, content):
        """
        Formats a message for the Llama model.

        Args:
            role (str): The role of the message sender (e.g., "user", "assistant").
            content (str): The content of the message.

        Returns:
            dict: A dictionary representing the formatted message.
        """
        return {
            "role": role,
            "content": content,
        }

    def parse_tool_response(self, response: ChatCompletionMessage):
        """
        Parses the tool response from the chat completion message.

        Args:
            response (ChatCompletionMessage): The chat completion message containing the tool response.

        Returns:
            list: A list of tool calls with function names and arguments, or None if parsing fails.
        """
        if response.content:
            return None

        tool_calls = []
        if response.tool_calls:
            for tool_call in response.tool_calls:
                function = tool_call.function
                function_name = function.name
                args_string = function.arguments
                try:
                    args = json.loads(args_string)
                    tool_calls.append({
                        "function": function_name,
                        "arguments": args,
                    })
                except json.JSONDecodeError as error:
                    print(f"Error parsing function arguments: {error}")
                    return None
        return tool_calls

    def handle_tool_response(self, parsed_response, messages: List):
        """
        Handles the tool response by calling the appropriate function and appending the result to messages.

        Args:
            parsed_response (dict): The parsed tool response containing the function name and arguments.
            messages (List): The list of messages to append the tool response to.

        Returns:
            List: The updated list of messages with the tool response appended.
        """
        available_functions = {"get_coin_price": get_coin_price, "translate_to_english": translate_to_english}
        function_name = parsed_response["function"]
    
        if function_name not in available_functions:
            messages.append({
                "role": "system",
                "content": "There's no such tool available. Try to answer the query without using a tool."
            })
            return messages
    
        function_to_call = available_functions[function_name]
        tool_response = function_to_call(**parsed_response["arguments"])
        messages.append(
            {
                "role": "assistant",
                "content": TOOL_RESPONSE_SYSTEM_PROMPT.format(tool_response=tool_response),
            }
        )
        return messages