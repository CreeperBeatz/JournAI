import streamlit as st
from modules.config import config, PAGE_CONFIG
import logging
import modules.streamlit_helper as sthelper
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from modules.file_manager import save_conversation, load_conversation, list_conversations
from model.conversation import Conversation

logging.basicConfig(level=logging.INFO)
st.set_page_config(**PAGE_CONFIG)
username = sthelper.authenticate()
sthelper.setup_pages()

# TODO Chat
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""You are a friendly AI assistant. You are
    currently having a conversation with a human. 

    chat_history: {chat_history},
    user: {question}
    assistant:"""
)

llm = ChatOpenAI(openai_api_key=config["openai"]["token"])
memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4)
llm_chain = LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt
)

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
    st.warning(chosen_conversation)

if chosen_conversation:
    st.session_state.current_conversation = load_conversation(username, chosen_conversation)
else:
    st.session_state.get("current_conversation")
    st.session_state.current_conversation = Conversation()

# Display all messages
for turn in st.session_state.current_conversation.history:
    with st.chat_message(turn["role"]):
        st.write(turn["content"])

user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.current_conversation.add_turn("user", user_prompt)
    with st.chat_message("user"):
        st.write(user_prompt)

if st.session_state.current_conversation.history:
    if st.session_state.current_conversation.history[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Loading..."):
                ai_response = llm_chain.predict(question=user_prompt)
                st.write(ai_response)
        st.session_state.current_conversation.add_turn("assistant", ai_response)
    # Save the conversation
    save_conversation(username, st.session_state.current_conversation)

st.sidebar.divider()
sthelper.show_sidebar_logout_button()
