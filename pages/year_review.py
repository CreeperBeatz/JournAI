from modules.config_manager import PAGE_CONFIG
import streamlit as st
from modules.streamlit_helper import setup_pages

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)
setup_pages()
