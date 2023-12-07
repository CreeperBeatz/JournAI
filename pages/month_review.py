from modules.config_manager import PAGE_CONFIG
import streamlit as st
from modules.streamlit_helper import setup_pages

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)
setup_pages()

# Get user id from state
user_id = st.session_state.user_id

# TODO summary of weeks
# TODO chat with GPT about what you want about them
