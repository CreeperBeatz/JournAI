import streamlit as st
from sqlalchemy.exc import IntegrityError

from database.db_utils import DBManager
from modules.config_manager import PAGE_CONFIG
from modules.streamlit_helper import setup_pages, setup_pages_with_login

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)
setup_pages()

# Page content
st.title("Welcome to JournAI")


# Early escape if user is not logged in
if "current_user" in st.session_state.keys():
    exit(0)

menu = ["Login", "Sign Up"]
choice = st.selectbox("Login or Signup", menu, label_visibility='hidden')

db_manager = DBManager()

if choice == "Login":
    st.subheader("Login to an Existing Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        login_result = db_manager.verify_login(username, password)
        if login_result:
            st.success("Logged In as {}".format(username))
            st.session_state['current_user'] = username
            st.session_state['user_id'] = db_manager.get_user_id(username)
            # Setup pages for successful login
            setup_pages_with_login()
        else:
            st.warning("Incorrect Username/Password")

elif choice == "Sign Up":
    st.subheader("Create a New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    verify_password = st.text_input("Verify Password", type='password')

    if st.button("Signup"):
        if password == verify_password:
            try:
                db_manager.add_user(username, password)
                st.success("You have successfully created an account.")
            except IntegrityError as e:
                st.error("User with this username already exists!")
        else:
            st.error("Passwords don't match!")
