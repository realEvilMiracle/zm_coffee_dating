from sqlalchemy import Column, Integer, BigInteger, String, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, UTC

from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String)
    full_name = Column(String)
    department = Column(String)
    position = Column(String)

    location = Column(String)
    hobbies = Column(Text)
    photo_file_id = Column(String)

    is_active = Column(Boolean, default=True)
    last_matched_with = Column(BigInteger, nullable=True)
    last_matched_at = Column(DateTime, nullable=True)
    last_match_is_success = Column(Boolean, nullable=True)

    created_at = Column(DateTime, default=datetime.now(UTC))


class MeetingFeedback(Base):
    __tablename__ = "meeting_feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id))
    partner_id = Column(ForeignKey(User.id))

    user = relationship("User", foreign_keys=[user_id], backref="given_feedbacks")
    partner = relationship("User", foreign_keys=[partner_id], backref="received_feedbacks")

    is_met = Column(Boolean, nullable=False)  # удалось ли пообщаться
    comment = Column(Text, nullable=True)  # отзыв
    date = Column(Date, nullable=False)  # дата опроса
