from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

GREETINGS_TEXT = ("Привет! Ты в ZM Dating – пространстве для общения и нетворкинга.\n"
                  "Каждый понедельник я буду предлагать тебе коллегу для встречи – это отличный шанс узнать, "
                  "с кем ты работаешь, поделиться идеями и просто провести время за приятным разговором.\n"
                  "Жми «Начать», чтобы окунуться в мир новых знакомств.")


@router.callback_query(F.data == "greetings")
async def handle_greetings(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()

    kb.button(text="Начать", callback_data="setup_profile")
    kb.button(text="Выход", callback_data="base_menu")

    await callback.message.answer(GREETINGS_TEXT, reply_markup=kb.as_markup())
