import streamlit as st
from database.db_utils import add_user, add_question_to_user, delete_question, get_daily_questions_for_user, \
    verify_login

# Initialize Streamlit
st.title("Daily Journal App")

menu = ["Home", "Login", "SignUp"]
choice = st.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Home")

elif choice == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        login_result = verify_login(username, password)
        if login_result:
            st.success("Logged In as {}".format(username))

            user_id = ...  # Retrieve the user's ID from the database

            # Display daily questions
            questions = get_daily_questions_for_user(user_id)
            answers = {}
            for q in questions:
                answers[q] = st.text_input(q)

            if st.button("Submit Journal Entry"):
                # Pass the answers to get the summary
                #summary = get_summary(answers)
                st.write("Your Summary: ", "summary")

        else:
            st.warning("Incorrect Username/Password")

elif choice == "SignUp":
    st.subheader("Create a New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Signup"):
        add_user(username, password)
        st.success("You have successfully created an account.")