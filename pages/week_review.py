import streamlit as st
import datetime
from database.db_utils import DBManager
from modules.config_manager import PAGE_CONFIG
from modules.streamlit_helper import period_picker, PeriodOptions, setup_pages
from modules.utilities import ExtendedEnum
import modules.summary_manager as summary_manager

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)
setup_pages()

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

# TODO GPT Chats
# TODO Save GPT chats in permanent storage
