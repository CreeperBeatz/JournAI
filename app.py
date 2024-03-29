import streamlit as st
import streamlit_authenticator as stauth
from modules.config import config, PAGE_CONFIG
import logging
import modules.streamlit_helper as sthelper
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
# from decouple import config
from langchain.memory import ConversationBufferWindowMemory

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
    st.warning("Please enter your username and password")
    st.stop()

sthelper.setup_pages()
sthelper.show_sidebar_logout_button()

# TODO Chat
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""You are a very kindl and friendly AI assistant. You are
    currently having a conversation with a human. Answer the questions
    in a kind and friendly tone with some sense of humor.

    chat_history: {chat_history},
    Human: {question}
    AI:"""
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

# check for messages in session and create if not exists
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello there, am ChatGPT clone"}
    ]


# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = llm_chain.predict(question=user_prompt)
            st.write(ai_response)
    new_ai_message = {"role": "assistant", "content": ai_response}
    st.session_state.messages.append(new_ai_message)
