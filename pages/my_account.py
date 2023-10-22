import streamlit as st
from database.db_utils import DBManager
from modules.streamlit_helper import setup_pages_no_login, generate_question_line
from modules.config_manager import PAGE_CONFIG

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)

db_manager = DBManager()

QUESTIONS_KEY = "questions"
TRASH_QUESTIONS_KEY = "trash_questions"

if "current_user" in st.session_state.keys():
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
        questions = db_manager.get_dummy_questions(1)
        st.session_state[QUESTIONS_KEY] = questions
    if TRASH_QUESTIONS_KEY not in st.session_state.keys():
        st.session_state[TRASH_QUESTIONS_KEY] = []

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
        if col2.button('↩️', key=f"untrash_{q.id}"):
            st.session_state[QUESTIONS_KEY].append(q)
            st.session_state[TRASH_QUESTIONS_KEY].remove(q)
            st.rerun()

    if st.button('Delete All'):
        if st.button('Are you sure?'):
            db_manager.delete_questions(st.session_state[TRASH_QUESTIONS_KEY])
            del st.session_state[TRASH_QUESTIONS_KEY]
            st.rerun()

    st.markdown("---")
    if st.button("Logout", type="primary"):
        for key, _ in st.session_state.items():
            del st.session_state[key]
        setup_pages_no_login()
        st.rerun()
else:
    st.text("Please log in to see this menu!")
