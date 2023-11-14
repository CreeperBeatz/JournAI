from modules.config_manager import PAGE_CONFIG
import streamlit as st
from modules.streamlit_helper import setup_pages_no_login

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)

# Early escape if user is not logged in
if "current_user" not in st.session_state.keys():
    st.warning("Please log in to see this menu!")
    setup_pages_no_login()
    exit(0)
