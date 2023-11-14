import streamlit as st
import datetime
from database.db_utils import DBManager
from modules.config_manager import PAGE_CONFIG
from modules.streamlit_helper import period_picker, PeriodOptions, setup_pages_no_login
from modules.utilities import ExtendedEnum

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)

# Early escape if user is not logged in
if "current_user" not in st.session_state.keys():
    st.warning("Please log in to see this menu!")
    setup_pages_no_login()
    exit(0)


class MenuOptions(ExtendedEnum):
    answers_by_date = "Answers by Date"
    mood_review = "Mood Review"
    insights = "Insights"


user_id = st.session_state['user_id']
db_manager = DBManager()
first_answer_date = db_manager.get_first_journal_entry_date(user_id)
week_start, week_end, chosen_week = period_picker(
    "Choose a week",
    PeriodOptions.WEEK,
    first_answer_date,
    datetime.datetime.now()
)
st.markdown(f"You have chosen: *{chosen_week}*")

choice = st.selectbox("Select Analysis", MenuOptions.values(), label_visibility='visible')

match choice:
    case MenuOptions.answers_by_date.value:
        st.text("Answers by date TODO")
    case MenuOptions.mood_review.value:
        st.text("Mood review TODO")
    case MenuOptions.insights.value:
        st.text("Insights TODO")
    case _:
        pass
