from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.handlers.base_menu import handle_base_menu
from db.crud import get_user_by_telegram_id, create_or_update_user

router = Router()


@router.callback_query(F.data == "disable_dating")
async def handle_disable_dating(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()

    kb.button(text="Нет, я хочу остаться", callback_data="stay_dating")
    kb.button(text="Да, уверен отключить", callback_data="confirm_disable")

    await callback.message.edit_text(
        "Приостановить участие? 🤔\n"
        "Ты можешь отключить ZM Dating в любой момент, но новые знакомства сами себя не найдут!",
        reply_markup=kb.as_markup()
    )


@router.callback_query(F.data == "stay_dating")
async def handle_stay_dating(callback: CallbackQuery):
    await handle_base_menu(callback)


@router.callback_query(F.data == "confirm_disable")
async def handle_confirm_disable(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)

    if user:
        await create_or_update_user(user.telegram_id, {"is_active": False})

    await callback.message.edit_text(
        "Ты вне игры, но это не навсегда! 🚪\n"
        "В любое время можешь снова включить ZM Dating и продолжить знакомиться с командой. "
        "Я всегда на связи!")

    await handle_base_menu(callback)
