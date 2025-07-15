from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from db.crud import get_user_by_telegram_id, create_or_update_user

router = Router()


class EditProfileState(StatesGroup):
    location = State()
    department = State()
    position = State()
    hobbies = State()
    photo = State()


@router.callback_query(F.data == "edit_profile")
async def handle_edit_profile(ctx: CallbackQuery or Message):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="main_menu"))
    kb.row(InlineKeyboardButton(text="Изменить локацию", callback_data="edit_location"))
    kb.row(InlineKeyboardButton(text="Изменить отдел", callback_data="edit_department"))
    kb.row(InlineKeyboardButton(text="Изменить должность", callback_data="edit_position"))
    kb.row(InlineKeyboardButton(text="Изменить интересы", callback_data="edit_hobbies"))
    kb.row(InlineKeyboardButton(text="Изменить фото", callback_data="edit_photo"))

    user = await get_user_by_telegram_id(telegram_id=ctx.from_user.id)

    if hasattr(ctx, "message"):
        ctx = ctx.message

    if not user:
        await ctx.answer("Произошла ошибка на сервер - профиль не найден.")
        return

    await ctx.answer_photo(
        photo=user.photo_file_id,
        caption=f"{user.full_name}\n"
                f"@{user.username}\n\n"
                f"{user.department} - {user.position}\n"
                f"{user.location}\n\n"
                f"О себе: {user.hobbies}\n"
    )

    await ctx.answer("Вот твой профиль. Что-то меняем или все ок?", reply_markup=kb.as_markup())


UPDATED_PROFILE_TEXT = "Профиль обновлен! 🔄\nТеперь он выглядит так"


@router.callback_query(F.data == "edit_location")
async def handle_edit_location(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileState.location)
    await callback.message.answer(
        "Обновим географию! 📍\n"
        "Напиши свою текущую локацию – это поможет мне находить для тебя интересных собеседников.")


@router.message(EditProfileState.location)
async def save_location(message: Message, state: FSMContext):
    await create_or_update_user(message.from_user.id, {"location": message.text})
    await state.clear()
    await message.answer(UPDATED_PROFILE_TEXT)
    await handle_edit_profile(message)


@router.callback_query(F.data == "edit_department")
async def handle_edit_department(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileState.department)
    await callback.message.answer("В каком отделе ты работаешь?")


@router.message(EditProfileState.department)
async def save_department(message: Message, state: FSMContext):
    await create_or_update_user(message.from_user.id, {"department": message.text})
    await state.clear()
    await message.answer(UPDATED_PROFILE_TEXT)
    await handle_edit_profile(message)


@router.callback_query(F.data == "edit_position")
async def handle_edit_position(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileState.position)
    await callback.message.answer("На какой должности находишься?")


@router.message(EditProfileState.position)
async def save_position(message: Message, state: FSMContext):
    await create_or_update_user(message.from_user.id, {"position": message.text})
    await state.clear()
    await message.answer(UPDATED_PROFILE_TEXT)
    await handle_edit_profile(message)


@router.callback_query(F.data == "edit_hobbies")
async def handle_edit_hobbies(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileState.hobbies)
    await callback.message.answer(
        "Добавим немного индивидуальности! 🚀\n"
        "Расскажи что-то новенькое о своих увлечениях – это сделает твой профиль более живым и интересным.")


@router.message(EditProfileState.hobbies)
async def save_hobbies(message: Message, state: FSMContext):
    await create_or_update_user(message.from_user.id, {"hobbies": message.text})
    await state.clear()
    await message.answer(UPDATED_PROFILE_TEXT)
    await handle_edit_profile(message)


@router.callback_query(F.data == "edit_photo")
async def handle_edit_photo(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileState.photo)
    await callback.message.answer(
        "Давай обновим твой аватар! 📸\n"
        "Отправь фото, которое будет отображаться в твоём профиле.")


@router.message(EditProfileState.photo, F.photo)
async def save_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Фото не было загружено. Произошла ошибка. Попробуйте ещё раз.")
        return

    await create_or_update_user(message.from_user.id, {"photo_file_id": message.photo[-1].file_id})
    await state.clear()
    await message.answer(UPDATED_PROFILE_TEXT)
    await handle_edit_profile(message)
