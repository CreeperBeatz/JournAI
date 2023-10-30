import os
from typing import List

from database.db_utils import DBManager
from database.models import Question
from modules.config_manager import PAGE_CONFIG
import streamlit as st

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)

user_id = st.session_state.get("user_id")

if not user_id:
    st.warning("Please log in to see this page!")
    exit()

db_manager = DBManager()
daily_questions: List[Question] = db_manager.get_questions_for_user(user_id)
if not daily_questions:
    st.info("No questions available for today.")
    st.stop()

st.title("Daily Questions")

any_saved = False  # Flag to check if any answer was saved or updated

with st.form(key='daily_questions_form'):
    for question in daily_questions:
        if question.is_deleted:
            continue

        st.subheader(question.question_text)

        existing_entry = db_manager.get_journal_entry(user_id, question.id)

        if existing_entry:
            initial_answer = existing_entry.answer
        else:
            initial_answer = ""

        # Allow for multiline text
        answer = st.text_area(question.question_hint, initial_answer)

        # Store the new answer for each question
        st.session_state[f"{question.id}_new_answer"] = answer

    if st.form_submit_button("Submit Answers"):
        for question in daily_questions:
            if question.is_deleted:
                continue

            new_answer = st.session_state.get(f"{question.id}_new_answer", None)

            if new_answer is None:
                continue

            db_manager.save_journal_entry(user_id, question.id, new_answer)
            any_saved = True  # Set the flag to true if any answer is saved or updated

        if any_saved:
            st.success("Your answers have been successfully saved.")
