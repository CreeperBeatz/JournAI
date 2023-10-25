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

if daily_questions:
    st.title("Daily Questions")

    with st.form(key='daily_questions_form'):
        for question in daily_questions:
            # Skip deleted questions
            if question.is_deleted:
                continue

            st.subheader(question.question_text)
            existing_entry = db_manager.get_journal_entry(user_id, question.id)

            # prefill the answer field with existing answer if any
            answer = st.text_input(f"Answer for {question.question_text}",
                                   existing_entry.answer if existing_entry else "")

            # To store the new answer for each question
            st.session_state[f"{question.id}_new_answer"] = answer

        # When the user presses the "Submit" button, the answers get updated or created in the database
        submitted = st.form_submit_button("Submit Answers")

        if submitted:
            for question in daily_questions:
                if question.is_deleted:
                    continue

                new_answer = st.session_state.get(f"{question.id}_new_answer", None)

                if new_answer is not None:
                    db_manager.save_journal_entry(user_id, question.id, new_answer)
                    st.success(f"Answer for {question.question_text} has been saved.")
else:
    st.info("No questions available for today.")