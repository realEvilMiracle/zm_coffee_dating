import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
from bot.handlers import setup_profile, edit_profile, main_menu, disable_dating, base_menu, greetings, feedback, \
    enable_dating, analytics
from bot.scheduler.setup_scheduler import setup_scheduler

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN")


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация хендлеров
    dp.include_routers(
        base_menu.router,
        greetings.router,
        setup_profile.router,
        edit_profile.router,
        main_menu.router,
        disable_dating.router,
        enable_dating.router,
        feedback.router,
        analytics.router,
    )

    setup_scheduler(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
