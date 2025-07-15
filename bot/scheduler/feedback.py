from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.crud import get_failure_active_users, get_active_matched_users
from db.session import get_session


async def send_feedback_request(bot: Bot):
    async for session in get_session():
        users = await get_active_matched_users(session)

        kb = InlineKeyboardBuilder()
        kb.button(text="Да, мы пообщались", callback_data="success_feedback")
        kb.button(text="Нет, мы еще не общались", callback_data="failure_feedback")

        for user in users:
            try:
                await bot.send_message(
                    user.telegram_id,
                    "Как дела с ZM Dating? ☕\n"
                    "Неделя подходит к концу – успел ли ты пообщаться?",
                    reply_markup=kb.as_markup()
                )
            except Exception as e:
                print(f"Ошибка отправки пользователю {user.telegram_id}: {e}")


async def send_second_feedback_request(bot: Bot):
    async for session in get_session():
        users = await get_failure_active_users(session)

        kb = InlineKeyboardBuilder()
        kb.button(text="Да, мы пообщались", callback_data="success_feedback")
        kb.button(text="Нет, не смогли пообщаться", callback_data="second_failure_feedback")

        for user in users:
            try:
                await bot.send_message(
                    user.telegram_id,
                    "Ну как, успели поболтать? 🤔\n"
                    "Давай по-честному – удалось встретиться или пока нет?",
                    reply_markup=kb.as_markup()
                )
            except Exception as e:
                print(f"Ошибка отправки пользователю {user.telegram_id}: {e}")
