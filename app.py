import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from modules.chatbot import ChatBot
from modules.config import config, PAGE_CONFIG
import logging
import modules.streamlit_helper as sthelper
from model.conversation import Conversation
from modules.utilities import save_conversation, load_conversation, list_conversations

logging.basicConfig(level=logging.INFO)
st.set_page_config(**PAGE_CONFIG)

# Ensure user is logged in
username = sthelper.authenticate()
sthelper.setup_pages()

# Page content
st.title("JournAI")
st.markdown("Welcome to JournAI!\n\n")

# Load the newest conversations
conversation_options = list_conversations(username)

with st.sidebar:
    # Create a placeholder for the button
    new_conversation_placeholder = st.empty()

    chosen_conversation = st.radio(
        "Choose a conversation",
        options=conversation_options,
        format_func=lambda x: conversation_options[x]['title'],
        index=None,
    )

    # use the placeholder to add the "New Conversation" button
    if new_conversation_placeholder.button("➕ New Conversation"):
        chosen_conversation = None

if chosen_conversation:
    st.session_state.current_conversation = load_conversation(username, chosen_conversation)
else:
    st.session_state.get("current_conversation")
    st.session_state.current_conversation = Conversation()

# Initialize chatbot instance
# TODO fix spaghetti code
chatbot = ChatBot()

# Display all messages
for turn in st.session_state.current_conversation.history.messages:
    prefix_map = {
        HumanMessage: "user",
        AIMessage: "assistant"
    }
    with st.chat_message(prefix_map[type(turn)]):
        st.write(turn.content)

user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.current_conversation.add_user_turn(user_prompt)
    with st.chat_message("user"):
        st.write(user_prompt)

if st.session_state.current_conversation.history.messages:
    if type(st.session_state.current_conversation.history.messages[-1]) is HumanMessage:
        with st.chat_message("assistant"):
            with st.spinner("Loading..."):
                ai_response = chatbot.predict(st.session_state.current_conversation)
                st.write(ai_response)
        st.session_state.current_conversation.add_ai_turn(ai_response)
    # Save the conversation
    save_conversation(username, st.session_state.current_conversation)

st.sidebar.divider()
sthelper.show_sidebar_logout_button()
