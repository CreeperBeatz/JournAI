from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, Question, JournalEntry, WeeklySummary, MonthlySummary

import bcrypt

engine = create_engine('sqlite:///journal_app.db')  # Create SQLite database
Session = sessionmaker(bind=engine)
session = Session()


# Initialize the database
def init_db():
    Base.metadata.create_all(engine)


# User related operations
def add_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hashed_password)
    session.add(user)
    session.commit()


def verify_login(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user:
        return bcrypt.checkpw(password.encode('utf-8'), user.password)
    return False


# Journal Entry related operations
def save_journal_entry(user_id, question_id, answer):
    entry = JournalEntry(user_id=user_id, question_id=question_id, answer=answer)
    session.add(entry)
    session.commit()


# Weekly Summary related operations
def save_weekly_summary(user_id, summary):
    weekly_summary = WeeklySummary(user_id=user_id, summary=summary)
    session.add(weekly_summary)
    session.commit()


# Monthly Summary related operations
def save_monthly_summary(user_id, summary):
    monthly_summary = MonthlySummary(user_id=user_id, summary=summary)
    session.add(monthly_summary)
    session.commit()


# Question related operations
def add_question(question_text):
    question = Question(question_text=question_text)
    session.add(question)
    session.commit()


def delete_question(question_id):
    question = session.query(Question).filter_by(id=question_id).first()
    if question:
        session.delete(question)
        session.commit()


def get_daily_questions():
    questions = session.query(Question).all()  # Assuming all questions are daily for this example
    return [q.question_text for q in questions]


# History related operations
def get_weekly_summaries(user_id):
    summaries = session.query(WeeklySummary).filter_by(user_id=user_id).all()
    return [s.summary for s in summaries]


def get_monthly_summaries(user_id):
    summaries = session.query(MonthlySummary).filter_by(user_id=user_id).all()
    return [s.summary for s in summaries]
