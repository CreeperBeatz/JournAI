import streamlit as st
from modules.config import PAGE_CONFIG
import logging
import modules.streamlit_helper as sthelper
from modules.chatbot import ChatBot
from modules.question_manager import save_questions_description
from modules.conversation_manager import save_conversation, load_conversation, list_conversations
import modules.question_manager as ques_manager
from model.conversation import Conversation
import json

logging.basicConfig(level=logging.INFO)
st.set_page_config(**PAGE_CONFIG)
username = sthelper.authenticate()
sthelper.setup_pages()

# Page content
st.title("JournAI")
st.markdown("Welcome to JournAI!\n\n")

# Initialize chatbot
if "chatbot" not in st.session_state.keys():
    st.session_state.chatbot = ChatBot(function_descriptions=[save_questions_description])

# Initialize chosen conversation
if "conversation_id" not in st.session_state.keys():
    st.session_state.conversation_id = None

# Load the newest conversations
conversation_options = list_conversations(username)

with st.sidebar:
    # Create a placeholder for the button
    new_conversation_placeholder = st.empty()

    # Get index (int) of session state choice
    options_list = list(conversation_options.keys())
    default_index = options_list.index(
        st.session_state.conversation_id) if st.session_state.conversation_id in options_list else None

    st.session_state.conversation_id = st.radio(
        "Choose a conversation",
        options=conversation_options,
        format_func=lambda x: conversation_options[x]['title'],
        index=default_index,
    )

    # use the placeholder to add the "New Conversation" button
    if new_conversation_placeholder.button("➕ New Conversation"):
        st.session_state.conversation_id = None

if not st.session_state.conversation_id:
    # No conversation chosen, begin new conversation
    st.session_state.current_conversation = Conversation(system_message=st.session_state.chatbot.system_message)
elif st.session_state.conversation_id != st.session_state.current_conversation.id:
    # New conversation chosen, load it from files
    st.session_state.current_conversation = load_conversation(username, st.session_state.conversation_id)


# Display all messages
for turn in st.session_state.current_conversation.history:
    role = turn["role"]
    if role != "system":
        with st.chat_message(turn["role"]):
            st.write(turn["content"])

user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.current_conversation.add_turn("user", user_prompt)
    with st.chat_message("user"):
        st.write(user_prompt)

if not st.session_state.current_conversation.history:
    st.stop()

last_role = st.session_state.current_conversation.history[-1]["role"]
if last_role != "assistant" and last_role != "system":
    with st.chat_message("assistant"):

        # Awaiting anwer from user for destructive function call
        if "questions" in st.session_state.keys() and st.session_state.questions:
            if st.button("Do you want to save questions?"):
                ques_manager.save_questions("test", st.session_state.questions)
                # FIXME this function role doesnt work
                st.session_state.current_conversation.add_turn("function", "Succesfully saved.")
            st.session_state.questions = None


        with st.spinner("Loading..."):
            ai_response = st.session_state.chatbot.chat(st.session_state.current_conversation)

            # if function call for saving questions
            if ai_response.function_call:
                if ai_response.function_call.name == "save_questions":
                    st.warning(ai_response.function_call.arguments)
                    st.session_state.questions = json.loads(ai_response.function_call.arguments)['questions']

            if ai_response.content:
                st.write(ai_response.content)
                st.session_state.current_conversation.add_turn("assistant", ai_response.content)



# Save the conversation
save_conversation(username, st.session_state.current_conversation)
# TODO Get title for conversation
# TODO Update sidebar

st.sidebar.divider()
sthelper.show_sidebar_logout_button()
