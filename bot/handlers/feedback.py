from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from db.crud import get_user_by_telegram_id, create_or_update_user, save_feedback

router = Router()


class SetFeedbackState(StatesGroup):
    success = State()


@router.callback_query(F.data == "success_feedback")
async def handle_success_feedback(callback: CallbackQuery, state: FSMContext):
    user = await get_user_by_telegram_id(callback.from_user.id)

    if not user:
        await callback.message.answer("Произошла ошибка на сервере - пользователь не найден")
        return

    partner_id = user.last_matched_with

    if partner_id is None:
        await callback.message.answer("Произошла ошибка на сервере - партнер не был найден")
        return

    partner = await get_user_by_telegram_id(partner_id)

    if not partner:
        await callback.message.answer("Произошла ошибка на сервере - партнер не был найден")
        return

    await callback.message.answer(
        "Класс! 🎉\n"
        "Делись впечатлениями – как прошла встреча? "
        f"Расскажи, чем тебя удивил {partner.full_name} @{partner.username}!")

    await state.set_state(SetFeedbackState.success)


@router.message(SetFeedbackState.success)
async def enter_feedback(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user_by_telegram_id(message.from_user.id)

    if not user:
        await message.answer("Произошла ошибка на сервере - пользователь не найден")
        return

    partner = await get_user_by_telegram_id(user.last_matched_with)

    if partner is None:
        await message.answer("Произошла ошибка на сервере - партнер не был найден")
        return

    await save_feedback(user_id=user.id, partner_id=partner.id, is_met=True, comment=message.text)

    await create_or_update_user(message.from_user.id, {
        "last_match_is_success": None,
        "last_matched_with": None,
        "last_matched_at": None
    })

    await message.answer(
        "На этом все, но мы еще встретимся! 😉\n"
        "Скоро новый мэтч и новые знакомства. Жду тебя на следующей неделе!")


@router.callback_query(F.data == "failure_feedback")
async def handle_failure_feedback(callback: CallbackQuery):
    await callback.message.answer(
        "Время на исходе! ⏳\n"
        "Остался всего день, чтобы завести новое знакомство. "
        "Ещё не поздно сделать первый шаг!")

    await create_or_update_user(callback.from_user.id, {"last_match_is_success": False})


@router.callback_query(F.data == "second_failure_feedback")
async def handle_second_failure_feedback(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)

    if not user:
        await callback.answer("Произошла ошибка на сервере - пользователь не найден")
        return

    partner = await get_user_by_telegram_id(user.last_matched_with)

    if not partner:
        await callback.answer("Произошла ошибка на сервере - пользователь не найден")
        return

    await save_feedback(user_id=user.id, partner_id=partner.id, is_met=False, comment=None)

    await create_or_update_user(callback.from_user.id, {
        "last_match_is_success": None,
        "last_matched_with": None,
        "last_matched_at": None
    })

    await callback.message.answer(
        "Не расстраивайся! 🤷‍♂️\n"
        "Бывает, что планы не совпадают. "
        "Попробуем снова на следующей неделе!")
