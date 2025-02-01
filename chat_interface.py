import streamlit as st
from utils.agent import SimpleAgent
from utils.rate_limiter import check_rate_limit
from utils.llm import call_llm
from config import MODEL
from prompts import SYSTEM_PROMPT

# Initialize the agent
agent = SimpleAgent()
system_prompt = {
    "role": "system",
    "content": SYSTEM_PROMPT
}
agent.messages.append(system_prompt)

# Streamlit UI
st.title("Crypto AI Assistant")
st.write("Ask me anything about cryptocurrency prices!")

# Display chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chat_placeholder = st.empty()

def render_chat():
    with chat_placeholder.container():
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

render_chat()

# User input
if user_input := st.chat_input("Enter your query:"):
    try:
        check_rate_limit()
        user_message = agent.get_llama_message_format("user", user_input)
        agent.messages.append(user_message)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        render_chat()  # Update chat history immediately

        response = call_llm(
            model=MODEL,
            messages=agent.messages,
            tools=agent.tools,
            tool_choice="auto"
        )

        agent_response = agent.get_llama_message_format(response.choices[0].message.role, response.choices[0].message.content)

        parsed_response = agent.parse_tool_response(response.choices[0].message)

        if parsed_response:
            for tool_call in parsed_response:
                agent.messages = agent.handle_tool_response(tool_call, agent.messages)

                res = call_llm(
                    model=MODEL,
                    messages=agent.messages,
                )
                agent_response = agent.get_llama_message_format(res.choices[0].message.role, res.choices[0].message.content)
                agent.messages.append(agent_response)
        else:
            agent.messages.append(agent_response)

        st.session_state.chat_history.append({"role": "assistant", "content": agent_response['content']})
        render_chat()  # Update chat history immediately
    except Exception as e:
        st.error(f"Error: {e}")