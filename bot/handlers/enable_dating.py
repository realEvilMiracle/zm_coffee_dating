from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.handlers.base_menu import handle_base_menu
from db.crud import get_user_by_telegram_id, create_or_update_user

router = Router()


@router.callback_query(F.data == "enable_dating")
async def handle_enable_dating(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)

    if not user:
        await callback.message.answer("Приносим свои извинения - произошла ошибка на сервере: Профиль не найден.")

    await create_or_update_user(user.telegram_id, {"is_active": True})

    await handle_base_menu(callback)
