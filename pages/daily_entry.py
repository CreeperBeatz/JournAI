import os
from typing import List

from database.db_utils import DBManager
from database.models import Question
from modules.config_manager import PAGE_CONFIG
import streamlit as st

from modules.emotions_tracker import emotion_picker
from modules.streamlit_helper import setup_pages

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)
setup_pages()

# Get user id from state
user_id = st.session_state.user_id

db_manager = DBManager()
daily_questions: List[Question] = db_manager.get_questions_for_user(user_id)
show_emotion_picker = db_manager.get_emotion_analysis(user_id)
if not daily_questions and not show_emotion_picker:
    st.info("No questions available")
    st.stop()

st.title("Daily Questions")

any_saved = False  # Flag to check if any answer was saved or updated

if daily_questions:
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

if show_emotion_picker:
    with st.expander("Emotions analysis", expanded=True):

        emotion_entry = db_manager.get_emotion_entry(user_id)

        st.image("images/emotion_wheel.png")
        main_emotion = emotion_picker(
            "What was the main emotion you felt during the day?",
            "main",
            emotion_entry.main_emotion if emotion_entry else None,
        )
        st.divider()
        secondary_emotion = emotion_picker(
            "Is there a secondary emotion you felt during the day?",
            "secondary",
            emotion_entry.secondary_emotion if emotion_entry else None,
        )

        db_manager.save_emotion_entry(user_id, main_emotion, secondary_emotion)
