import datetime
from datetime import date, datetime
from typing import List, Optional, Type

from sqlalchemy import create_engine, and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, Question, JournalEntry, WeeklySummary, MonthlySummary, \
    EmotionEntry

import bcrypt


class DBManager:

    # Initialize the database
    def __init__(self):
        engine = create_engine('sqlite:///journal_app.db')  # Create SQLite database
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

        self.salt = bcrypt.gensalt()

    # region User related operations
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

    def get_emotion_analysis(self, user_id) -> bool:
        user = self.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise NoResultFound("No user with that user_id")

        if user.emotions_analysis:
            return True
        return False

    def reverse_emotion_analysis_state(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise NoResultFound("No user with that user_id")

        user.emotions_analysis = not user.emotions_analysis
        self.session.commit()

    def get_all_users(self) -> list[Type[User]]:
        return self.session.query(User).all()


    # endregion

    # region Journal Entry related operations
    def get_journal_entry(self, user_id, question_id, entry_date: date = date.today()):
        entry = self.session.query(JournalEntry).filter(
            and_(
                JournalEntry.user_id == user_id,
                JournalEntry.question_id == question_id,
                JournalEntry.date == entry_date
            )
        ).first()
        return entry

    def save_journal_entry(self, user_id, question_id, answer, entry_date: date = date.today()):
        existing_entry = self.get_journal_entry(user_id, question_id, entry_date)

        if existing_entry:
            existing_entry.answer = answer
        else:
            new_entry = JournalEntry(
                user_id=user_id,
                question_id=question_id,
                answer=answer,
                date=entry_date
            )
            self.session.add(new_entry)

        self.session.commit()

    def get_first_journal_entry_date(self, user_id):
        entry = self.session.query(JournalEntry).filter(JournalEntry.user_id == user_id).order_by(JournalEntry.date).first()
        return entry.date if entry else datetime.min

    # endregion

    # region Emotion Entry related operations
    def get_emotion_entry(self, user_id, entry_date: date = date.today()):
        entry = self.session.query(EmotionEntry).filter(
            and_(
                EmotionEntry.user_id == user_id,
                EmotionEntry.date == entry_date
            )
        ).first()
        return entry

    def save_emotion_entry(self, user_id, main_emotion: str, secondary_emotion: str,
                           entry_date: date = date.today()):
        existing_entry = self.get_emotion_entry(user_id, entry_date)

        if existing_entry:
            existing_entry.main_emotion = main_emotion
            existing_entry.secondary_emotion = secondary_emotion
        else:
            new_entry = EmotionEntry(
                user_id=user_id,
                main_emotion=main_emotion,
                secondary_emotion=secondary_emotion,
                date=entry_date
            )
            self.session.add(new_entry)

        self.session.commit()

    # endregion

    # region Weekly Summary related operations
    def save_weekly_summary(self, user_id, summary):
        weekly_summary = WeeklySummary(user_id=user_id, summary=summary)
        self.session.add(weekly_summary)
        self.session.commit()

    # Monthly Summary related operations
    def save_monthly_summary(self, user_id, summary):
        monthly_summary = MonthlySummary(user_id=user_id, summary=summary)
        self.session.add(monthly_summary)
        self.session.commit()

    # endregion

    # region Question related operations
    def add_question_to_user(self, user_id, question_text, question_hint=None):
        question = Question(user_id=user_id, question_text=question_text, question_hint=question_hint)
        self.session.add(question)
        self.session.commit()

    def get_questions_for_user(self, user_id):
        questions = self.session.query(Question).filter_by(user_id=user_id, is_deleted=False).all()
        return questions

    def delete_question(self, user_id, question_id):
        question = self.session.query(Question).filter_by(user_id=user_id, id=question_id).first()
        if question:
            question.is_deleted = True
            self.session.commit()

    def delete_questions(self, questions: List[Question]):
        for question in questions:
            self.delete_question(question.user_id, question.id)
        self.session.commit()

    # endregion

    # region History related operations
    def get_weekly_summaries(self, user_id):
        summaries = self.session.query(WeeklySummary).filter_by(user_id=user_id).all()
        return [s.summary for s in summaries]

    def get_monthly_summaries(self, user_id):
        summaries = self.session.query(MonthlySummary).filter_by(user_id=user_id).all()
        return [s.summary for s in summaries]

    # endregion
