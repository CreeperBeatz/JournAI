from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesGcmEngine
from sqlalchemy import BLOB
from datetime import datetime
import os

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(BLOB, nullable=False)  # byte hash array

    # Relationship to Journal Entries
    journal_entries = relationship('JournalEntry', back_populates='user')

    # Relationship to Weekly Summaries
    weekly_summaries = relationship('WeeklySummary', back_populates='user')

    # Relationship to Monthly Summaries
    monthly_summaries = relationship('MonthlySummary', back_populates='user')


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False)


class JournalEntry(Base):
    __tablename__ = 'journal_entries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    answer = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship to User
    user = relationship('User', back_populates='journal_entries')

    # Relationship to Question
    question = relationship('Question')


class WeeklySummary(Base):
    __tablename__ = 'weekly_summaries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    summary = Column(Text)
    week_ending = Column(DateTime, default=datetime.utcnow)

    # Relationship to User
    user = relationship('User', back_populates='weekly_summaries')


class MonthlySummary(Base):
    __tablename__ = 'monthly_summaries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    summary = Column(Text)
    month_ending = Column(DateTime, default=datetime.utcnow)

    # Relationship to User
    user = relationship('User', back_populates='monthly_summaries')

class YearlySummary(Base):
    __tablename__ = 'yearly_summaries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    summary = Column(Text)
    month_ending = Column(DateTime, default=datetime.utcnow)

    # Relationship to User
    user = relationship('User', back_populates='monthly_summaries')
