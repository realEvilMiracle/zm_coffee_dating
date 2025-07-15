from datetime import date
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db.models import User, MeetingFeedback
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session


async def get_user_by_telegram_id_in_session(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def get_user_by_telegram_id(telegram_id: int) -> User | None:
    async for session in get_session():
        return await get_user_by_telegram_id_in_session(session=session, telegram_id=telegram_id)


async def get_active_users(session: AsyncSession) -> List[User]:
    result = await session.execute(select(User).where(User.is_active == True))
    return result.scalars().all()


async def get_active_matched_users(session: AsyncSession) -> List[User]:
    result = await session.execute(select(User).where(User.is_active == True, User.last_matched_with != None))
    return result.scalars().all()


async def get_failure_active_users(session: AsyncSession) -> List[User]:
    result = await session.execute(
        select(User).where(
            User.is_active == True,
            User.last_matched_with != None,
            User.last_match_is_success == False))
    return result.scalars().all()


async def create_or_update_user(telegram_id: int, data: dict) -> None:
    async for session in get_session():
        user = await get_user_by_telegram_id_in_session(session=session, telegram_id=telegram_id)

        if user is None:
            user = User(telegram_id=telegram_id)
        for key, value in data.items():
            setattr(user, key, value)

        session.add(user)

        await session.commit()


async def save_feedback(user_id: int, partner_id: int, is_met: bool, comment: str | None) -> None:
    async for session in get_session():
        feedback = MeetingFeedback(
            user_id=user_id,
            partner_id=partner_id,
            is_met=is_met,
            comment=comment,
            date=date.today()
        )
        session.add(feedback)
        await session.commit()


async def get_feedback_stats(date_from, date_to) -> List[MeetingFeedback]:
    async for session in get_session():
        result = await session.execute(
            select(MeetingFeedback)
            .options(
                joinedload(MeetingFeedback.user),
                joinedload(MeetingFeedback.partner),
            )
            .where(
                MeetingFeedback.date >= date_from,
                MeetingFeedback.date < date_to
            )
        )
        return result.scalars().all()
