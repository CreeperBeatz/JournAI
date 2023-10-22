from st_pages import Page, show_pages
import streamlit as st
import streamlit.components.v1 as components
import json


def generate_question_line(key_dict, icon, button_key):
    key_dict[button_key] = icon
    icon_config = f"""
            <script>
                var elements = window.parent.document.getElementsByClassName('css-x78sv8 eqr7zpz4');
                let dict = {json.dumps(key_dict)};
                let keys = Object.keys(dict);
                let icons = Object.values(dict);
                for (var i = 0; i < elements.length; ++i) {{
                    for (var j = 0; j < keys.length; ++j){{
                        if (elements[i].innerText == keys[j])
                        elements[i].innerHTML = icons[j];
                    }}
                }}
            </script>
            """
    components.html(f"{icon_config}", height=0, width=0)
    return {'label': button_key, 'key': button_key}


def setup_pages_no_login():
    show_pages([
        Page("app.py", "Home", "🎃"),
        Page("pages/login.py", "Login", "💫")
    ])


def setup_pages_with_login():
    show_pages([
        Page("app.py", "Home", "🎃"),
        Page("pages/my_account.py", "My Account", "🦱"),
        Page("pages/daily_entry.py", "Daily Entry", "✒️"),
        Page("pages/weekly_summary.py", "Weekly Summary", "📃"),
        Page("pages/monthly_summary.py", "Monthly Summary", "📰"),
        Page("pages/yearly_summary.py", "Yearly Summary", "📖"),
    ])
