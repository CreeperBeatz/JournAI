import time
import streamlit_authenticator as stauth
import yaml
from st_pages import Page, show_pages
import streamlit as st
from streamlit.source_util import _on_pages_changed, get_pages
from streamlit_extras.switch_page_button import switch_page

from modules.config import config

DEFAULT_PAGE = "app.py"


def setup_pages():
    # Define pages
    pages = [
        Page("app.py", "Home", "🏠"),
        Page("pages/settings.py", "User Settings", "⚙️"),
    ]

    show_pages(pages)


def show_only_first_page() -> None:
    """
    Clear all pages except the first one, if there is more than one page.

    Returns:
        None
    """
    current_pages = get_pages(DEFAULT_PAGE)

    if len(current_pages.keys()) == 1:
        return

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()


def go_home_if_no_auth_status() -> None:
    """
    Redirect to the home page if there is no authentication status in the session state or if the authentication status is False.

    Returns:
        None
    """
    if "authentication_status" not in st.session_state:
        switch_page("home")

    authentication_status = st.session_state.authentication_status
    if not authentication_status:
        switch_page("home")


def show_sidebar_logout_button():
    """
    Puts a logout button on the sidebar if the user is logged in.
    """

    if "authenticator" not in st.session_state or "authentication_status" not in st.session_state:
        return

    authenticator = st.session_state.authenticator
    authentication_status = st.session_state.authentication_status

    if authentication_status:
        authenticator.logout("Logout", "sidebar")


def authenticate() -> str:
    """

    Returns:
        Username, name
    """
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

    st.session_state.authenticator = authenticator

    try:
        name, authentication_status, username = authenticator.login("main")
    except KeyError as e:
        # Error in the library, log out the user
        authenticator.logout()
        st.stop()

    if authentication_status is False:
        show_only_first_page()
        st.error("Username/password is incorrect")
        st.stop()
    elif authentication_status is None:
        show_only_first_page()
        try:
            if authenticator.register_user(pre_authorization=False):
                st.success('User registered successfully. You can log in now.')
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)
        st.stop()
    return username, name
