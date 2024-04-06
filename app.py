import json

import streamlit as st
from modules.config import PAGE_CONFIG
import logging
import modules.streamlit_helper as sthelper
from modules.chatbot import ChatBot
from modules.conversation_manager import save_conversation, load_conversation, list_conversations
import modules.question_manager as question_manager
import modules.answer_manager as answer_manager
from model.conversation import Conversation

logging.basicConfig(level=logging.INFO)
st.set_page_config(**PAGE_CONFIG)
username, name = sthelper.authenticate()
sthelper.setup_pages()

# Some functionalities need the script to rerun after reaching EoT (ex. multi-step replies)
RERUN_AT_END = False

# Page content
st.title("JournAI")
st.markdown("Welcome to JournAI!\n\n")

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
    user_questions = question_manager.get_questions(username)
    st.session_state.chatbot = ChatBot(name)
    st.session_state.current_conversation = Conversation(
        system_message=st.session_state.chatbot.system_message)
    st.session_state.conversation_id = st.session_state.current_conversation.id
    st.session_state.questions = None
elif st.session_state.conversation_id != st.session_state.current_conversation.id:
    # New conversation chosen, load it from files
    user_questions = question_manager.get_questions(username)
    st.session_state.chatbot = ChatBot(name)
    st.session_state.current_conversation = load_conversation(username, st.session_state.conversation_id)
    st.session_state.conversation_id = st.session_state.current_conversation.id
    st.session_state.questions = None

# Display all messages
for turn in st.session_state.current_conversation.history:
    role = turn["role"]
    if role != "system":
        with st.chat_message(turn["role"]):
            # FIXME visualization of messages with no content
            if turn.get("content"):
                st.write(turn["content"])
            else:
                st.write("*Calling an internal functionality*")

user_prompt = st.chat_input()
if user_prompt is not None:
    st.session_state.current_conversation.add_human_message(user_prompt)
    with st.chat_message("user"):
        st.write(user_prompt)

last_role = st.session_state.current_conversation.history[-1]["role"]

# Function call answer
if st.session_state.current_conversation.history[-1].get("function_call"):
    with st.chat_message("function"):
        with st.spinner("Loading..."):
            try:
                arguments = json.loads(st.session_state.current_conversation.history[-1]["function_call"]["arguments"])
                match st.session_state.current_conversation.history[-1]["function_call"]["name"]:
                    case "get_questions":
                        questions = question_manager.get_questions(username)
                        st.write(questions)
                        st.session_state.current_conversation.add_function_response(
                            name="get_questions",
                            content=str(questions)
                        )
                        RERUN_AT_END = True
                    case "save_questions":
                        # region save questions
                        questions_list = json.loads(arguments)["questions"]

                        multiline_questions = '\n * '.join(questions_list)
                        confirmation_message = f"Do you want to save these as your daily questions?\n * {multiline_questions}"

                        st.write(confirmation_message)
                        col1, col2, _ = st.columns([1, 1, 5])
                        with col1:
                            if st.button("Yes", type="primary", use_container_width=True):
                                question_manager.save_questions(username, questions_list)
                                st.session_state.current_conversation.add_function_response(
                                    name="save_questions",
                                    content="Saved successfully!"
                                )
                        with col2:
                            if st.button("No", use_container_width=False):
                                st.session_state.current_conversation.add_function_response(
                                    name="save_questions",
                                    content="Questions not saved: User rejected."
                                )
                        # endregion
                    case "get_answers":
                        from_date = arguments["from_date"]
                        to_date = arguments["to_date"]
                        answers = answer_manager.get_answers(username, from_date, to_date)
                        st.session_state.current_conversation.add_function_response("get_answers", str(answers))
                        st.write(answers)
                        RERUN_AT_END = True
                    case "save_answer":
                        print(arguments)
                        question = arguments["question"]
                        answer = arguments["answer"]
                        if question not in question_manager.get_questions(username):
                            raise ValueError("Question isn't a daily question of the user!")

                        confirmation_message = (f"Do you want to save this as an answer for your daily question?\n"
                                                f" * **Question**: {question}\n"
                                                f" * **Answer**: {answer}")
                        st.write(confirmation_message)
                        col1, col2, _ = st.columns([1, 1, 5])
                        with col1:
                            if st.button("Yes", type="primary", use_container_width=True):
                                answer_manager.save_answer(username, question, answer)
                                st.session_state.current_conversation.add_function_response(
                                    name="save_answer",
                                    content="Saved successfully!"
                                )
                        with col2:
                            if st.button("No", use_container_width=False):
                                st.session_state.current_conversation.add_function_response(
                                    name="save_answer",
                                    content="Questions not saved: User rejected."
                                )
                    case _:
                        st.error("Critical Error: function not recognized")
            except ValueError as e:
                st.session_state.current_conversation.add_function_response("get_answers", str(e))
                st.write(e)

# Turn for AI assistant
if last_role != "assistant" and last_role != "system":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = st.session_state.chatbot.chat(st.session_state.current_conversation)
            st.session_state.current_conversation.add_ai_message(ai_response)

            # if function call
            if ai_response.function_call:
                RERUN_AT_END = True

            # if message present
            if ai_response.content:
                st.write(ai_response.content)

# Get title for conversation
if st.session_state.current_conversation.title == "New Conversation" and len(
        st.session_state.current_conversation.history) > 1:
    title = st.session_state.chatbot.get_title(st.session_state.current_conversation)
    st.session_state.current_conversation.title = title

# TODO Get summary for the conversation
# TODO Update sidebar
# TODO append to RAG

# Save the conversation
save_conversation(username, st.session_state.current_conversation)
st.sidebar.divider()
sthelper.show_sidebar_logout_button()

if RERUN_AT_END:
    st.rerun()
