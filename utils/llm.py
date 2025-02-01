from together import Together

client = Together()

def call_llm(model, messages, tools=None, tool_choice=None, max_tokens=1024, temperature=0):
    """
    Calls the LLM (Large Language Model) with the specified parameters.

    Args:
        model (str): The model to use for the LLM.
        messages (list): A list of messages to send to the LLM.
        tools (list, optional): A list of tools to use with the LLM. Defaults to None.
        tool_choice (str, optional): The tool choice to use with the LLM. Defaults to None.
        max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 1024.
        temperature (float, optional): The temperature to use for the LLM. Defaults to 0.

    Returns:
        dict: The response from the LLM.

    Raises:
        Exception: If there is an error calling the LLM.
    """
    try:
        return client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            max_tokens=max_tokens,
            temperature=temperature,
        )
    except Exception as e:
        raise Exception(f"Error calling LLM: {e}")