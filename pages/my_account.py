import streamlit as st
from database.db_utils import DBManager
from modules.streamlit_helper import setup_pages_no_login, generate_question_line
from modules.config_manager import PAGE_CONFIG

# Initialize Streamlit
st.set_page_config(**PAGE_CONFIG)

key_dict = {}
st.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css'
         '/all.min.css"/>', unsafe_allow_html=True)

if "current_user" in st.session_state.keys():
    st.markdown("# Personal Details")

    # TODO
    st.text("TODO")

    st.markdown("---\n\n## Account setup\n")
    openAI_key = st.text_input("OpenAI API Key", type='password')

    if st.button('Save'):
        st.text("TODO Saving")

    st.markdown("---\n\n## Questions")
    question_list = ["how do you feel?", "why are you gay?"]

    key_dict = {}
    for question in question_list:
        st.button(**generate_question_line(key_dict,
                                           '<i class="fa-solid fa-circle-user fa-bounce"></i>',
                                           button_key=question))

    st.markdown("---")
    if st.button("Logout", type="primary"):
        del st.session_state["current_user"]
        setup_pages_no_login()
        st.warning("Successfully logged out")
else:
    st.text("Please log in to see this menu!")
