import streamlit as st
from database.db_utils import DBManager
from database.models import Question
from modules.streamlit_helper import setup_pages_no_login, generate_question_line
from modules.config_manager import PAGE_CONFIG

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)

db_manager = DBManager()

QUESTIONS_KEY = "questions"
TRASH_QUESTIONS_KEY = "trash_questions"
DELETE_CONFIRM_KEY = "delete_confirm"

if "current_user" in st.session_state.keys():
    user_id = st.session_state['user_id']
    st.markdown("# Personal Details")

    # TODO
    st.text("TODO")

    st.markdown("---\n\n## Account setup\n")
    openAI_key = st.text_input("OpenAI API Key", type='password')

    if st.button('Save'):
        st.text("TODO Saving")

    st.markdown("---\n\n## Questions")

    # Save questions in session state
    if QUESTIONS_KEY not in st.session_state.keys():
        questions = db_manager.get_questions(user_id)
        st.session_state[QUESTIONS_KEY] = questions
    if TRASH_QUESTIONS_KEY not in st.session_state.keys():
        st.session_state[TRASH_QUESTIONS_KEY] = []

    # region Add New Questions
    st.subheader("Add New Questions")
    question_text = st.text_input("Question Text")
    if st.button("Add Question") and question_text:
        db_manager.add_question_to_user(user_id, question_text)
        question = Question(user_id=user_id, question_text=question_text)
        del st.session_state[QUESTIONS_KEY]  # Delete so ID is loaded on next run
        st.rerun()

    # endregion

    # region Visualize Active Questions and Trash
    st.subheader("Active Questions")
    for q in st.session_state[QUESTIONS_KEY]:
        col1, col2 = st.columns([4, 1])
        col1.write(q.question_text)
        if col2.button('🗑️', key=f"trash_{q.id}"):
            st.session_state[TRASH_QUESTIONS_KEY].append(q)
            st.session_state[QUESTIONS_KEY].remove(q)
            st.rerun()

    st.subheader('Trash')
    for q in st.session_state[TRASH_QUESTIONS_KEY]:
        col1, col2 = st.columns([4, 1])
        col1.write(q.question_text)
        if col2.button('⬆️', key=f"untrash_{q.id}"):
            st.session_state[QUESTIONS_KEY].append(q)
            st.session_state[TRASH_QUESTIONS_KEY].remove(q)
            st.rerun()
    # endregion

    # region Delete Trash functionality
    if st.button('Delete Trash'):
        st.session_state[DELETE_CONFIRM_KEY] = True  # Set the state
        st.rerun()

    if st.session_state.get(DELETE_CONFIRM_KEY):
        st.markdown("Are you sure you want to delete these question(s)?")
        if st.button('Yes', type="primary"):
            db_manager.delete_questions(st.session_state[TRASH_QUESTIONS_KEY])
            st.session_state[TRASH_QUESTIONS_KEY] = []
            st.session_state[DELETE_CONFIRM_KEY] = False  # Reset the state
            st.rerun()
    # endregion

    st.markdown("---")
    if st.button("Logout", type="primary"):
        for key, _ in st.session_state.items():
            del st.session_state[key]
        setup_pages_no_login()
        st.rerun()
else:
    st.text("Please log in to see this menu!")
