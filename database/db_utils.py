from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, Question, JournalEntry, WeeklySummary, MonthlySummary

import bcrypt

class DBManager:

    # Initialize the database
    def __init__(self):
        engine = create_engine('sqlite:///journal_app.db')  # Create SQLite database
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

        self.salt = bcrypt.gensalt()

    # User related operations
    def add_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), self.salt)
        user = User(username=username, password=hashed_password)
        self.session.add(user)
        self.session.commit()

    def verify_login(self, username, password):
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            return bcrypt.checkpw(password.encode('utf-8'), user.password)
        return False

    def get_user_id(self, username):
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            return user.id
        return -1

    # Journal Entry related operations
    def save_journal_entry(self, user_id, question_id, answer):
        entry = JournalEntry(user_id=user_id, question_id=question_id, answer=answer)
        self.session.add(entry)
        self.session.commit()

    # Weekly Summary related operations
    def save_weekly_summary(self, user_id, summary):
        weekly_summary = WeeklySummary(user_id=user_id, summary=summary)
        self.session.add(weekly_summary)
        self.session.commit()

    # Monthly Summary related operations
    def save_monthly_summary(self, user_id, summary):
        monthly_summary = MonthlySummary(user_id=user_id, summary=summary)
        self.session.add(monthly_summary)
        self.session.commit()

    # Question related operations
    def add_question_to_user(self, user_id, question_text):
        question = Question(user_id=user_id, question_text=question_text)
        self.session.add(question)
        self.session.commit()

    def delete_question(self, user_id, question_id):
        question = self.session.query(Question).filter_by(user_id=user_id, id=question_id).first()
        if question:
            self.session.delete(question)
            self.session.commit()

    def get_questions(self, user_id):
        questions = self.session.query(Question).filter_by(user_id=user_id).all()
        return questions

    def delete_questions(self, questions: List[Question]):
        for question in questions:
            self.session.delete(question)
        self.session.commit()

    # History related operations
    def get_weekly_summaries(self, user_id):
        summaries = self.session.query(WeeklySummary).filter_by(user_id=user_id).all()
        return [s.summary for s in summaries]

    def get_monthly_summaries(self, user_id):
        summaries = self.session.query(MonthlySummary).filter_by(user_id=user_id).all()
        return [s.summary for s in summaries]
