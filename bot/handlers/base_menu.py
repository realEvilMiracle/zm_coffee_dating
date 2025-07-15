from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.crud import get_user_by_telegram_id

router = Router()


@router.message(F.text, Command("start"))
@router.callback_query(F.data == "base_menu")
async def handle_base_menu(ctx: Message or CallbackQuery):
    user = await get_user_by_telegram_id(telegram_id=ctx.from_user.id)

    kb = InlineKeyboardBuilder()

    callback_data = "greetings"

    if user is not None:
        callback_data = "main_menu"

    kb.button(text="ZM Dating", callback_data=callback_data)

    if hasattr(ctx, 'message'):
        ctx = ctx.message

    try:
        await ctx.edit_text("Основное меню бота", reply_markup=kb.as_markup())
    except Exception as e:
        print(f"Ошибка обновления сообщения: {e}")
        await ctx.answer("Основное меню бота", reply_markup=kb.as_markup())
