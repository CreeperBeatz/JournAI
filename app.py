import streamlit as st
import streamlit_authenticator as stauth
import yaml

from modules.config import config, PAGE_CONFIG
import logging
import modules.streamlit_helper as sthelper
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from modules.conversations import list_conversations, Conversation, load_conversation, save_conversation

logging.basicConfig(level=logging.INFO)
st.set_page_config(**PAGE_CONFIG)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

st.session_state.authenticator = authenticator

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    sthelper.show_only_first_page()
    st.error("Username/password is incorrect")
    st.stop()
elif authentication_status is None:
    sthelper.show_only_first_page()
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully. You can log in now.')
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)
    st.stop()

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



if chosen_conversation:
    st.session_state.current_conversation = load_conversation(username, chosen_conversation)
else:
    st.session_state.get("current_conversation")
    st.session_state.current_conversation = Conversation()

# Display all messages
for turn in st.session_state.current_conversation.turns:
    with st.chat_message(turn["role"]):
        st.write(turn["text"])

user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.current_conversation.add_turn("user", user_prompt)
    with st.chat_message("user"):
        st.write(user_prompt)

if st.session_state.current_conversation.turns:
    if st.session_state.current_conversation.turns[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Loading..."):
                ai_response = llm_chain.predict(question=user_prompt)
                st.write(ai_response)
        st.session_state.current_conversation.add_turn("assistant", ai_response)
    # Save the conversation
    save_conversation(username, st.session_state.current_conversation)

st.sidebar.divider()
sthelper.show_sidebar_logout_button()
