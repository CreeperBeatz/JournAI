import calendar
from enum import Enum

from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages
import streamlit as st
import datetime


class PeriodOptions(Enum):
    WEEK = 1,
    MONTH = 2,
    YEAR = 3,


def setup_pages_no_login():
    show_pages([
        Page("app.py", "Home", "🎃"),
    ])


def setup_pages_with_login():
    show_pages([
        Page("app.py", "Home", "🎃"),
        Page("pages/my_account.py", "My Account", "🦱"),
        Page("pages/daily_entry.py", "Daily Entry", "✒️"),
        Page("pages/week_review.py", "Week Review", "📃"),
        Page("pages/month_review.py", "Month Review", "📰"),
        Page("pages/year_review.py", "Year Review", "📖"),
    ])

    if st.sidebar.button("Logout", type="primary"):
        for key, _ in st.session_state.items():
            del st.session_state[key]
        setup_pages_no_login()
        st.rerun()


def setup_pages():
    if user_authenticated():
        setup_pages_with_login()
    else:
        setup_pages_no_login()

def user_authenticated():
    # TODO make comprehensive with Cookie Support
    if "current_user" in st.session_state.keys():
        return True
    return False



def period_picker(label: str = "Select a date",
                  period: PeriodOptions = PeriodOptions.WEEK,
                  start_date_limit: datetime.date = None,
                  end_date_limit: datetime.date = None,
                  ):
    if start_date_limit and end_date_limit:
        selected_date = st.date_input(label, min_value=start_date_limit, max_value=end_date_limit)
    elif start_date_limit:
        selected_date = st.date_input(label, min_value=start_date_limit)
    elif end_date_limit:
        selected_date = st.date_input(label, max_value=end_date_limit)
    else:
        selected_date = st.date_input(label)

    if period == PeriodOptions.WEEK:
        start_date = selected_date - datetime.timedelta(days=selected_date.weekday())
        end_date = start_date + datetime.timedelta(days=6)
        month_year = selected_date.strftime("%B %Y")
        period_str = f"Week {selected_date.isocalendar()[1]}, {month_year}"

    elif period == PeriodOptions.MONTH:
        start_date = selected_date.replace(day=1)
        last_day = calendar.monthrange(selected_date.year, selected_date.month)[1]
        end_date = selected_date.replace(day=last_day)
        period_str = selected_date.strftime("%B %Y")

    elif period == PeriodOptions.YEAR:
        start_date = datetime.date(selected_date.year, 1, 1)
        end_date = datetime.date(selected_date.year, 12, 31)
        period_str = str(selected_date.year)

    else:
        raise ValueError("Invalid period option")

    return start_date, end_date, period_str

# Further logic can go here, using the week_start and week_end as needed
