from st_pages import Page, show_pages


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
        Page("pages/weekly_summary.py", "Week Review", "📃"),
        Page("pages/monthly_summary.py", "Month Review", "📰"),
        Page("pages/yearly_summary.py", "Year Review", "📖"),
    ])
