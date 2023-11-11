import streamlit as st
from modules.config_manager import PAGE_CONFIG
from modules.streamlit_helper import setup_pages_no_login, setup_pages_with_login

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)

if "current_user" in st.session_state.keys():
    setup_pages_with_login()
else:
    setup_pages_no_login()


# Page content
st.title("Daily Journal App")
st.markdown("Welcome to the Daily Journaling app JournAI!\n\n"
            "To start filling in your Journal:\n\n"
            "1. Go to the **Login** page and Register (Google OAuth will be supported... sometime "
            "in the future)\n"
            "2. Go to 'My Account'\n"
            "3. Add the questions you want to answer daily\n"
            "You're Ready! Now you can head to the 'Daily Entry' page and start filling out or editing "
            "your daily entries!\n\n"
            "At the end of each week on Sunday, you can get a weekly summary for each of your questions "
            "generated by ChatGPT, which you can later refine with more instructions, or modify the "
            "summary itself by hand.\n")
