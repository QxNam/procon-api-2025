from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from pytz import timezone

Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    startsAt = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    content = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(tz=timezone("Asia/Saigon")))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    password = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone("Asia/Saigon")))

    submissions = relationship(
        "Submission", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    problem_id = Column(Integer, nullable=False)
    ops = Column(JSON, nullable=False)
    pair_count = Column(Integer)
    step_count = Column(Integer)
    step_factor = Column(Float)
    time_running = Column(Float)
    score = Column(Float)
    submitted_at = Column(DateTime(timezone=True), default=datetime.now(tz=timezone("Asia/Saigon")))

    user = relationship("User", back_populates="submissions")
