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
username, name = sthelper.authenticate()
sthelper.setup_pages()

# Page content
st.title("JournAI")
st.markdown("Welcome to JournAI!\n\n")

# Initialize chatbot
#if "chatbot" not in st.session_state.keys():
#    st.session_state.chatbot = ChatBot(function_descriptions=[save_questions_description])

# Initialize chosen conversation
if "conversation_id" not in st.session_state.keys():
    st.session_state.conversation_id = None

# Load the newest conversations
conversation_options = list_conversations(username)

with st.sidebar:
    if st.button("➕ New Conversation"):
        default_index = None
        st.session_state.conversation_id = None
    else:
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

if not st.session_state.conversation_id:
    # No conversation chosen, begin new conversation
    user_questions = ques_manager.load_questions(username)
    st.session_state.chatbot = ChatBot([save_questions_description], user_questions, name)
    st.session_state.current_conversation = Conversation(
        system_message=st.session_state.chatbot.system_message)
    st.session_state.conversation_id = st.session_state.current_conversation.id
    st.session_state.questions = None
elif st.session_state.conversation_id != st.session_state.current_conversation.id:
    # New conversation chosen, load it from files
    user_questions = ques_manager.load_questions(username)
    st.session_state.chatbot = ChatBot([save_questions_description], user_questions, name)
    st.session_state.current_conversation = load_conversation(username, st.session_state.conversation_id)
    st.session_state.conversation_id = st.session_state.current_conversation.id
    st.session_state.questions = None

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

        # Awaiting answer from user for destructive function call
        if "questions" in st.session_state.keys() and st.session_state.questions:
            multiline_questions = '\n * '.join(st.session_state.questions)
            ai_answer = f"Do you want to save these as your daily questions?\n * {multiline_questions}"
            st.write(ai_answer)
            col1, col2, _ = st.columns([1, 1, 5])
            with col1:
                if st.button("Yes", type="primary", use_container_width=True):
                    ques_manager.save_questions("test", st.session_state.questions)
                    st.session_state.current_conversation.add_turn("assistant", ai_answer)
                    st.session_state.current_conversation.add_turn("user", "yes")
                    st.session_state.current_conversation.add_turn(
                        "function",
                        "Successfully saved.",
                        "save_questions"
                    )
                    st.session_state.questions = None
            with col2:
                if st.button("No", use_container_width=True):
                    st.session_state.current_conversation.add_turn("assistant", ai_answer)
                    st.session_state.current_conversation.add_turn("user", "No")
                    st.session_state.questions = None
        elif "answers" in st.session_state.keys() and st.session_state.current_conversation:
            pass
        else:
            with st.spinner("Loading..."):
                ai_response = st.session_state.chatbot.chat(st.session_state.current_conversation)

                # if function call for saving questions
                if ai_response.function_call:
                    if ai_response.function_call.name == "save_questions":
                        st.session_state.questions = json.loads(ai_response.function_call.arguments)[
                            'questions']
                        st.rerun()

                if ai_response.content:
                    st.write(ai_response.content)
                    st.session_state.current_conversation.add_turn("assistant", ai_response.content)

if st.session_state.current_conversation.title == "New Conversation" and len(st.session_state.current_conversation.history) > 1:
    title = st.session_state.chatbot.get_title(st.session_state.current_conversation)
    st.session_state.current_conversation.title = title

# Save the conversation
save_conversation(username, st.session_state.current_conversation)
# TODO Get title for conversation
# TODO Update sidebar

st.sidebar.divider()
sthelper.show_sidebar_logout_button()
