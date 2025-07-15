import random
from datetime import datetime, UTC
from itertools import zip_longest
from aiogram import Bot
from db.crud import get_active_users, create_or_update_user
from db.session import get_session

IF_NOT_FOUND_MESSAGE = ("Приносим свои извинения - мы не смогли подобрать Вам партнера."
                        "Но не отчаивайтесь - в следующий раз, мы обязательно кого-нибудь Вам найдем!")


async def run_matching(bot: Bot):
    async for session in get_session():
        users = await get_active_users(session)
        random.shuffle(users)

        pairs = list(zip_longest(users[::2], users[1::2]))

        for user1, user2 in pairs:

            if not user1:
                await bot.send_message(
                    user2.telegram_id,
                    IF_NOT_FOUND_MESSAGE,
                )

                await create_or_update_user(user2.telegram_id, {"last_matched_with": None})

                continue

            if not user2:
                await bot.send_message(
                    user1.telegram_id,
                    IF_NOT_FOUND_MESSAGE,
                )

                await create_or_update_user(user1.telegram_id, {"last_matched_with": None})

                continue

            for sender, partner in [(user1, user2), (user2, user1)]:
                try:
                    await bot.send_message(
                        sender.telegram_id,
                        "Понедельник – значит, время для нового знакомства! 🚀\n"
                        f"Твоя пара на эту неделю – {partner.full_name} @{partner.username}.\n"
                        f"🗣️ Тема для разговора: {partner.hobbies}\n"
                        "Знаешь, что делает людей интересными? "
                        "Их истории, идеи и то, как они смотрят на мир. "
                        "Так что не стесняйся – обсудите всё, что вас увлекает. "
                        "Может, у вас похожие хобби, а может, совсем разные взгляды – "
                        "в любом случае это шанс узнать что-то новое! 😉"
                    )

                    await bot.send_photo(
                        sender.telegram_id,
                        partner.photo_file_id,
                        caption=f"{partner.full_name}\n"
                                f"@{partner.username}\n\n"
                                f"{partner.department} - {partner.position}\n"
                                f"{partner.location}\n\n"
                                f"О себе: {partner.hobbies}\n"
                    )

                    sender.last_matched_with = partner.telegram_id
                    sender.last_matched_at = datetime.now(UTC)

                    await bot.send_message(
                        sender.telegram_id,
                        "Не откладывай на потом! 🚀\n"
                        "До конца недели у вас есть время, чтобы поговорить. "
                        "Не упускай шанс узнать что-то новое!"
                    )
                except Exception as e:
                    print(f"Ошибка при отправке мэтча: {e}")
        await session.commit()
