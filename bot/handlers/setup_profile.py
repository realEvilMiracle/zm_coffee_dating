from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from db.crud import create_or_update_user

router = Router()


class InitProfileState(StatesGroup):
    location = State()
    department = State()
    position = State()
    hobbies = State()
    photo = State()
    confirm = State()


START_TEXT = (
    "Мы работаем из разных уголков мира!🌎\n"
    "Расскажи, где ты сейчас – интересно узнать географию нашей команды."
)


@router.callback_query(F.data == "setup_profile")
async def handle_setup_profile(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "Давай оформим твой профиль!\n"
        "Вот основная информация о тебе, которую я нашел")
    await callback.message.answer(
        f"{callback.from_user.full_name}\n"
        f"@{callback.from_user.username}\n\n")
    await callback.message.answer(START_TEXT)
    await state.set_state(InitProfileState.location)


@router.message(InitProfileState.location)
async def enter_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer(
        "Добавим немного деталей!✨\n"
        "Напиши пару слов о себе: чем увлекаешься, что тебе интересно, "
        "может, у тебя есть необычное хобби? "
        "Это поможет твоим собеседникам найти с тобой общие темы!")
    await message.answer("В каком отделе ты работаешь?")
    await state.set_state(InitProfileState.department)


@router.message(InitProfileState.department)
async def enter_department(message: Message, state: FSMContext):
    await state.update_data(department=message.text)
    await message.answer("А на какой должности?")
    await state.set_state(InitProfileState.position)


@router.message(InitProfileState.position)
async def enter_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    await message.answer(
        "Добавим немного деталей!✨\n"
        "Напиши пару слов о себе: чем увлекаешься, что тебе интересно, "
        "может, у тебя есть необычное хобби? "
        "Это поможет твоим собеседникам найти с тобой общие темы!")
    await state.set_state(InitProfileState.hobbies)


@router.message(InitProfileState.hobbies)
async def enter_hobbies(message: Message, state: FSMContext):
    await state.update_data(hobbies=message.text)
    await message.answer(
        "Фото – это плюс к нетворкингу!😉\n"
        "Давай добавим твоё фото в профиль, чтобы знакомства стали чуть более личными. "
        "Жду снимок!")
    await state.set_state(InitProfileState.photo)


@router.message(InitProfileState.photo, F.photo)
async def enter_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Фото не было загружено. Произошла ошибка. Попробуйте ещё раз.")
        return

    photo_file_id = message.photo[-1].file_id

    await state.update_data(photo=photo_file_id)

    data = await state.get_data()

    kb = InlineKeyboardBuilder()

    kb.button(text="Да, идем дальше", callback_data="confirm_profile")
    kb.button(text="Нет, изменить профиль", callback_data="restart_profile")

    department = data["department"]
    position = data["position"]
    location = data["location"]
    hobbies = data["hobbies"]

    await message.answer_photo(
        photo=photo_file_id,
        caption=f"{message.from_user.full_name}\n"
                f"@{message.from_user.username}\n\n"
                f"{department} - {position}\n"
                f"{location}\n\n"
                f"О себе: {hobbies}\n"
    )

    await message.answer(
        "Теперь твой профиль выглядит так. "
        "Все нравится? Если да – двигаемся дальше! "
        "Если нет – давай поправим.", reply_markup=kb.as_markup())

    await state.set_state(InitProfileState.confirm)


@router.callback_query(InitProfileState.confirm, F.data == "confirm_profile")
async def handle_confirm_profile(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await create_or_update_user(
        telegram_id=callback.from_user.id,
        data={
            "username": callback.from_user.username,
            "full_name": callback.from_user.full_name,
            "location": data["location"],
            "department": data["department"],
            "position": data["position"],
            "hobbies": data["hobbies"],
            "photo_file_id": data["photo"],
            "is_active": True,
        }
    )

    await callback.message.answer(
        "Готово! ☕\n"
        "Теперь остаётся только ждать понедельника – именно тогда я найду для тебя классного собеседника. "
        "Не пропусти!")
    await state.clear()


@router.callback_query(InitProfileState.confirm, F.data == "restart_profile")
async def restart_profile(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(START_TEXT)
    await state.set_state(InitProfileState.location)
