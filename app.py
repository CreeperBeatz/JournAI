import json
import streamlit as st
from modules.utilities import context_as_system_message
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
st.title("JournAI Chat")

# Initialize session state variables
sthelper.set_session_state_defaults()

# Load the newest conversations
conversation_options = list_conversations(username)

with st.sidebar:
    if st.button("➕ New Conversation"):
        st.session_state.conversation_id = None
        default_index = 0

    options_list = list(conversation_options.keys())
    default_index = options_list.index(st.session_state.conversation_id) if st.session_state.conversation_id in options_list else None

    st.session_state.conversation_id = st.radio(
        "Choose a conversation",
        options=conversation_options,
        format_func=lambda x: conversation_options[x]['title'],
        index=default_index
    )


if not st.session_state.conversation_id:
    # No conversation chosen, begin new conversation
    user_questions = question_manager.get_questions(username)
    st.session_state.chatbot = ChatBot(name)
    st.session_state.conversation = Conversation(
        system_message=st.session_state.chatbot.system_message)
    st.session_state.conversation_id = st.session_state.conversation.id
    st.session_state.questions = None
elif st.session_state.conversation_id != st.session_state.conversation.id:
    # New conversation chosen, load it from files
    user_questions = question_manager.get_questions(username)
    st.session_state.chatbot = ChatBot(name)
    st.session_state.conversation = load_conversation(username, st.session_state.conversation_id)
    st.session_state.conversation_id = st.session_state.conversation.id
    st.session_state.questions = None

# Display all messages so far
for turn in st.session_state.conversation.history:
    role = turn["role"]
    if role not in ["system"]:
        with st.chat_message(turn["role"]):
            # Visualization of messages with no content
            if turn.get("content"):
                st.write(turn["content"])
            else:
                st.write("*Calling an internal functionality*")

user_prompt = st.chat_input()
if user_prompt is not None:
    st.session_state.conversation.add_human_message(user_prompt)
    with st.chat_message("user"):
        st.write(user_prompt)

# Add buttons explaining the app
if len(st.session_state.conversation.history) < 2:
    if question_manager.get_questions(username):
        if st.button("Fill in my daily questions", use_container_width=True):
            st.session_state.conversation.add_human_message(
                "Can we go over my daily questions one by one and answer them?"
            )
    else:
        if st.button("Learn about JournAI", use_container_width=True, type="primary"):
            st.session_state.conversation.add_system_message(
                "The user is currently chatting with the assistant through an app with the following"
                "layout:\n On the top left, there is a little button that opens the Sidebar menu. On "
                "it, the history of the previous conversations"
                "the user had is visualized, as well as a button for starting a new conversation "
                "(➕ New Conversation). The menu has 2 items: Home, where the conversations are located,"
                " and User Settings, where user credentials can be changed."
                "In a new paragraph, you should also tell the user "
                "about what the goals of daily journaling can be. Since it's your first conversation "
                "with the user, explain everything in detail. Use a warm tone that you would expect "
                "from a psychologist and use markdown where needed."
                "In a new paragraph, tell the user that the biggest strength of this application is that"
                "it can provide insights based on your daily answers in new conversations. "
                "The user can ask the bot in the"
                "end of the week for insights about their answers, repeating patterns or progress."
            )
            st.session_state.conversation.add_human_message(
                "What is the layout of the app? How can I use this app to daily journal? What are your "
                "capabilities in that sense?"
            )
            RERUN_AT_END = True

last_role = st.session_state.conversation.history[-1]["role"]

# Function call answer
if st.session_state.conversation.history[-1].get("function_call"):
    with st.chat_message("function"):
        with st.spinner("Loading..."):
            try:
                arguments = json.loads(st.session_state.conversation.history[-1]["function_call"]["arguments"])
                match st.session_state.conversation.history[-1]["function_call"]["name"]:
                    case "get_questions":
                        questions = question_manager.get_questions(username)
                        st.write(questions)
                        st.session_state.conversation.add_function_response(
                            name="get_questions",
                            content=str(questions)
                        )
                        RERUN_AT_END = True
                    case "save_questions":
                        # region save questions
                        questions_list = arguments["questions"]

                        multiline_questions = '\n * '.join(questions_list)
                        confirmation_message = (f"Do you want to save these as your daily questions? \n\n"
                                                f"<sub>(Due to a bug, you have to click the button "
                                                f"twice)</sub>\n"
                                                f"* {multiline_questions}")

                        st.markdown(confirmation_message, unsafe_allow_html=True)
                        col1, col2, _ = st.columns([1, 1, 5])
                        with col1:
                            if st.button("Yes", type="primary", use_container_width=True):
                                question_manager.save_questions(username, questions_list)
                                st.session_state.conversation.add_function_response(
                                    name="save_questions",
                                    content="Saved successfully!"
                                )
                        with col2:
                            if st.button("No", use_container_width=True):
                                st.session_state.conversation.add_function_response(
                                    name="save_questions",
                                    content="Questions not saved: User rejected."
                                )
                        # endregion
                    case "get_answers":
                        from_date = arguments["from_date"]
                        to_date = arguments["to_date"]
                        answers = answer_manager.get_answers(username, from_date, to_date)
                        st.session_state.conversation.add_function_response("get_answers", str(answers))
                        st.write(answers)
                        RERUN_AT_END = True
                    case "save_answer":
                        try:
                            question = arguments["question"]
                            answer = arguments["answer"]
                            answer_manager.save_answer(username, question, answer)
                            st.session_state.conversation.add_function_response(
                                name="save_answer",
                                content="Saved successfully!"
                            )
                        except ValueError as e:
                            st.session_state.conversation.add_function_response(
                                name="save_answer",
                                content=str(e)
                            )
                        RERUN_AT_END = True
                    case _:
                        st.error("Critical Error: function not recognized")
            except ValueError as e:
                st.session_state.conversation.add_function_response("get_answers", str(e))
                st.write(e)

# RAG Turn (only after first User Query, for optimisation)
if last_role == "user" and len(st.session_state.conversation.history) == 2:
    with st.spinner("Loading previous conversations..."):
        query_text = st.session_state.conversation.history[-1]["content"]
        query_embedding = st.session_state.chatbot.get_embedding(query_text)
        try:
            context, _ = st.session_state.embeddings_db.search_similar(
                username=username,
                query_embedding=query_embedding
            )
        except RuntimeError as e:
            logging.error("Couldnt retrieve embeddings!")
            logging.error(e)
            context = ""
        st.session_state.conversation.add_system_message(
            context_as_system_message(context)
        )

# AI assistant turn (After RAG)
if last_role != "assistant" and len(st.session_state.conversation.history) > 1:
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = st.session_state.chatbot.chat(st.session_state.conversation)
            st.session_state.conversation.add_ai_message(ai_response)

            # if function call
            if ai_response.function_call:
                RERUN_AT_END = True

            # if message present
            if ai_response.content:
                st.write(ai_response.content)

# Get title for conversation
if st.session_state.conversation.title == "New Conversation" and len(
        st.session_state.conversation.history) > 1:
    title = st.session_state.chatbot.get_title(st.session_state.conversation)
    st.session_state.conversation.title = title

# Save the conversation
if st.session_state.conversation.new_messages:
    save_conversation(username, st.session_state.conversation)
    st.session_state.conversation.new_messages = False
    if len(st.session_state.conversation.history) > 1:
        summary = st.session_state.chatbot.get_summary(st.session_state.conversation)
        vector = st.session_state.chatbot.get_embedding(summary)
        st.session_state.embeddings_db.insert_document(
            uuid=st.session_state.conversation.id,
            username=username,
            text=summary,
            embedding=vector,
            date=st.session_state.conversation.creation_date
        )
        logging.info(f"Current Conversation UUID: {st.session_state.conversation.id}")
        logging.info("Successful save")

st.sidebar.divider()
sthelper.show_sidebar_logout_button()

if RERUN_AT_END:
    st.rerun()