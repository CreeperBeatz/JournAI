import time

from st_pages import Page, show_pages
import streamlit as st
from streamlit.source_util import _on_pages_changed, get_pages
from streamlit_extras.switch_page_button import switch_page

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


def render_chat(chat_name):
    pass


def new_chat(chat_name):
    if not st.session_state["chats"].get(chat_name):
        st.session_state["chats"][chat_name] = {
            "answer": [],
            "question": [],
            "messages": [
                {"role": "system", "content": st.session_state["params"]["prompt"]}
            ],
            "is_delete": False,
            "display_name": chat_name,
        }
    return chat_name


def switch_chat(chat_name):
    if st.session_state.get("current_chat") != chat_name:
        st.session_state["current_chat"] = chat_name
        render_chat(chat_name)


def switch_chat_name(chat_name):
    if st.session_state.get("current_chat") != chat_name:
        st.session_state["current_chat"] = chat_name
        render_sidebar()
        render_chat(chat_name)
        st.stop()


def delete_chat(chat_name):
    if chat_name in st.session_state['chats']:
        st.session_state['chats'][chat_name]['is_delete'] = True

    current_chats = [chat for chat, value in st.session_state['chats'].items() if not value['is_delete']]
    if len(current_chats) == 0:
        switch_chat(new_chat(f"Chat{len(st.session_state['chats'])}"))
        st.stop()

    if st.session_state["current_chat"] == chat_name:
        del st.session_state["current_chat"]
        switch_chat_name(current_chats[0])


def edit_chat(chat_name, zone):
    def edit():
        if not st.session_state['edited_name']:
            print('name is empty!')
            return None

        if (st.session_state['edited_name'] != chat_name
                and st.session_state['edited_name'] in st.session_state['chats']):
            print('name is duplicated!')
            return None

        if st.session_state['edited_name'] == chat_name:
            print('name is not modified!')
            return None

        st.session_state['chats'][chat_name]['display_name'] = st.session_state['edited_name']

    edit_zone = zone.empty()
    time.sleep(0.1)
    with edit_zone.container():
        st.text_input('New Name', st.session_state['chats'][chat_name]['display_name'],
                      key='edited_name')
        column1, _, column2 = st.columns([1, 5, 1])
        column1.button('✅', on_click=edit)
        column2.button('❌')


def render_sidebar_chat_management(zone):
    new_chat_button = zone.button(label="➕ New Chat", use_container_width=True)
    if new_chat_button:
        new_chat_name = f"Chat{len(st.session_state['chats'])}"
        st.session_state["current_chat"] = new_chat_name
        new_chat(new_chat_name)

    with st.sidebar.container():
        for chat_name in st.session_state["chats"].keys():
            if st.session_state['chats'][chat_name]['is_delete']:
                continue
            if chat_name == st.session_state.get('current_chat'):
                column1, column2, column3 = zone.columns([7, 1, 1])
                column1.button(
                    label='💬 ' + st.session_state['chats'][chat_name]['display_name'],
                    on_click=switch_chat_name,
                    key=chat_name,
                    args=(chat_name,),
                    type='primary',
                    use_container_width=True,
                )
                column2.button(label='📝', key='edit', on_click=edit_chat, args=(chat_name, zone))
                column3.button(label='🗑️', key='remove', on_click=delete_chat, args=(chat_name,))
            else:
                zone.button(
                    label='💬 ' + st.session_state['chats'][chat_name]['display_name'],
                    on_click=switch_chat_name,
                    key=chat_name,
                    args=(chat_name,),
                    use_container_width=True,
                )

    if new_chat_button:
        switch_chat(new_chat_name)


def render_sidebar():
    chat_name_container = st.sidebar.container()
    render_sidebar_chat_management(chat_name_container)
