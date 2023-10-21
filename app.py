import streamlit as st
from database.db_utils import DBManager

# Initialize Streamlit
st.title("Daily Journal App")

menu = ["Login", "SignUp"]
choice = st.selectbox("Menu", menu)

db_manager = DBManager()

if choice == "Home":
    st.subheader("Home")

elif choice == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        login_result = db_manager.verify_login(username, password)
        if login_result:
            st.success("Logged In as {}".format(username))
            # TODO Display daily questions
        else:
            st.warning("Incorrect Username/Password")

elif choice == "SignUp":
    st.subheader("Create a New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Signup"):
        db_manager.add_user(username, password)
        st.success("You have successfully created an account.")