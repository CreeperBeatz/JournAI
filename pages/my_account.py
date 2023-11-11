import streamlit as st
from database.db_utils import DBManager
from database.models import Question
from modules.streamlit_helper import setup_pages_no_login
from modules.config_manager import PAGE_CONFIG

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)

db_manager = DBManager()

QUESTIONS_KEY = "questions"
TRASH_QUESTIONS_KEY = "trash_questions"
DELETE_CONFIRM_KEY = "delete_confirm"

# Early escape if user is not logged in
if "current_user" not in st.session_state.keys():
    st.text("Please log in to see this menu!")
    exit(0)

user_id = st.session_state['user_id']
st.markdown("# Personal Details")

st.text("TODO")

st.markdown("---\n\n# Account setup\n")
st.markdown("---\n\n## Questions")

# Initialize questions in session state if not present
if QUESTIONS_KEY not in st.session_state.keys():
    questions = db_manager.get_questions_for_user(user_id)  # Consider adding error handling
    st.session_state[QUESTIONS_KEY] = questions

if TRASH_QUESTIONS_KEY not in st.session_state.keys():
    st.session_state[TRASH_QUESTIONS_KEY] = []

# Add New Questions
st.subheader("Add New Questions")
question_text = st.text_input("Question Text")
question_hint = st.text_input("Question Hint")
if st.button("Add Question") and question_text:
    db_manager.add_question_to_user(user_id, question_text, question_hint)  # Consider adding error handling
    del st.session_state[QUESTIONS_KEY]  # Trigger reload of IDs
    st.rerun()

# Visualize Active Questions and Trash
st.subheader("Active Questions")
st.divider()
for q in st.session_state[QUESTIONS_KEY]:
    col1, col2 = st.columns([6, 1])
    col1.markdown(f"#### {q.question_text} \n\n{q.question_hint}")
    st.divider()
    if col2.button('‎\n\n🗑️\n\n‎', key=f"trash_{q.id}", use_container_width=True):
        # TODO: Consider updating this status in the database
        st.session_state[TRASH_QUESTIONS_KEY].append(q)
        st.session_state[QUESTIONS_KEY].remove(q)
        st.rerun()

st.subheader('Trash')
for q in st.session_state[TRASH_QUESTIONS_KEY]:
    col1, col2 = st.columns([6, 1])
    col1.markdown(f"#### {q.question_text} \n\n{q.question_hint}")
    if col2.button('‎\n\n⬆️\n\n‎', key=f"untrash_{q.id}", use_container_width=True):
        st.session_state[QUESTIONS_KEY].append(q)
        st.session_state[TRASH_QUESTIONS_KEY].remove(q)
        st.rerun()

# Delete Trash functionality
if st.button('Delete Trash'):
    st.session_state[DELETE_CONFIRM_KEY] = True
    st.rerun()

if st.session_state.get(DELETE_CONFIRM_KEY):
    st.markdown("Are you sure you want to delete these question(s)?")
    if st.button('Yes', type="primary"):
        # Consider adding error handling
        db_manager.delete_questions(st.session_state[TRASH_QUESTIONS_KEY])
        st.session_state[TRASH_QUESTIONS_KEY] = []
        st.session_state[DELETE_CONFIRM_KEY] = False
        st.rerun()

st.markdown("---")

# Locked Functionality questions
# Emotions

if st.button("Logout", type="primary"):
    for key, _ in st.session_state.items():
        del st.session_state[key]
    setup_pages_no_login()
    st.rerun()
