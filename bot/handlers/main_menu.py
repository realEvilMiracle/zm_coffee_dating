from aiogram import Router, F
from aiogram.enums import InputMediaType
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.crud import get_user_by_telegram_id

router = Router()


@router.callback_query(F.data == "main_menu")
async def handle_main_menu(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)

    if not user:
        await callback.message.answer("Приносим свои извинения - произошла ошибка на сервере: Профиль не найден.")

    kb = InlineKeyboardBuilder()

    kb.button(text="Редактировать профиль", callback_data="edit_profile")

    if user.is_active:
        kb.button(text="Отключить ZM Dating", callback_data="disable_dating")
    else:
        kb.button(text="Начать ZM Dating", callback_data="enable_dating")

    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer("Главное меню", reply_markup=kb.as_markup())
    else:
        await callback.message.edit_text("Главное меню", reply_markup=kb.as_markup())
