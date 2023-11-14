import streamlit as st
from database.db_utils import DBManager
from modules.config_manager import PAGE_CONFIG
from modules.streamlit_helper import setup_pages_with_login, period_picker, PeriodOptions
from modules.utilities import ExtendedEnum

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)


class MenuOptions(ExtendedEnum):
    answers_by_date = "Answers by Date"
    mood_review = "Mood Review"
    insights = "Insights"

week_start, week_end, chosen_week = period_picker("Choose a week", PeriodOptions.WEEK)
st.markdown(f"You have chosen: *{chosen_week}*")

choice = st.selectbox("Select Analysis", MenuOptions.values(), label_visibility='visible')

db_manager = DBManager()

match choice:
    case MenuOptions.answers_by_date.value:
        st.text("Answers by date TODO")
    case MenuOptions.mood_review.value:
        st.text("Mood review TODO")
    case MenuOptions.insights.value:
        st.text("Insights TODO")
    case _:
        pass