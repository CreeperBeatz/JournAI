from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, BLOB, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from datetime import date
# Consider using bcrypt or Argon2 for hashing

Base = declarative_base()

# User Table representing user information
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(BLOB, nullable=False)  # Make sure to use a strong hashing algorithm

    # Relationships
    questions = relationship('Question', back_populates='user')
    journal_entries = relationship('JournalEntry', back_populates='user')
    weekly_summaries = relationship('WeeklySummary', back_populates='user')
    monthly_summaries = relationship('MonthlySummary', back_populates='user')
    yearly_summaries = relationship('YearlySummary', back_populates='user')


# Questions Table
class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question_text = Column(String(255), nullable=False)
    question_hint = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_deleted = Column(Boolean, default=False)

    # Relationship to User
    user = relationship('User', back_populates='questions')


# Journal Entries Table
class JournalEntry(Base):
    __tablename__ = 'journal_entries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    answer = Column(Text)
    date = Column(Date, nullable=False, default=date.today())

    # Relationships
    user = relationship('User', back_populates='journal_entries')
    question = relationship('Question')


# Weekly Summary Table
class WeeklySummary(Base):
    __tablename__ = 'weekly_summaries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    summary = Column(Text)
    week_ending = Column(DateTime, default=datetime.utcnow)

    # Relationship to User
    user = relationship('User', back_populates='weekly_summaries')


# Monthly Summary Table
class MonthlySummary(Base):
    __tablename__ = 'monthly_summaries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    summary = Column(Text)
    month_ending = Column(DateTime, default=datetime.utcnow)

    # Relationship to User
    user = relationship('User', back_populates='monthly_summaries')


# Yearly Summary Table
class YearlySummary(Base):
    __tablename__ = 'yearly_summaries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    summary = Column(Text)
    year_ending = Column(DateTime, default=datetime.utcnow)

    # Relationship to User
    user = relationship('User', back_populates='yearly_summaries')  # Fixed back_populates
