import streamlit as st
from streamlit_authenticator import Authenticate
from modules.config import PAGE_CONFIG
import yaml
from yaml.loader import SafeLoader
import modules.streamlit_helper as sthelper
import modules.question_manager as question_manager

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)

sthelper.go_home_if_no_auth_status()
sthelper.show_sidebar_logout_button()

authenticator: Authenticate = st.session_state.authenticator
name = st.session_state.name
username = st.session_state.username

st.header(f"Welcome *{name}*")

try:
    if authenticator.update_user_details(username):
        st.success("Entries updated successfully")
except Exception as e:
    st.error(e)

try:
    if authenticator.reset_password(username):
        st.success("Password modified successfully")
except Exception as e:
    st.error(e)

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

with open("config.yaml", "w") as file:
    yaml.dump(config, file, default_flow_style=False)

with st.container(border=True):
    user_questions = question_manager.get_questions(username)
    if user_questions:
        st.markdown("#### Your daily questions are as follows:")
        questions_list = '* ' + '\n * '.join(user_questions)
        st.markdown(questions_list)
        st.markdown("\nIf you want to change your daily questions, ask the chatbot to do so!")
    else:
        st.markdown("#### You haven't set up your daily questions yet!\n\n Ask the Chatbot to set them "
                    "up for you, by going to the Home page and writing 'Help me set up my daily "
                    "questions'.")