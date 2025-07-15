from aiogram import Router
from aiogram.types import Message, FSInputFile
import re
from datetime import datetime
from bot import ADMINS
from db.crud import get_feedback_stats  # реализуем ниже
from utils.excel_export import write_feedback_to_excel  # реализуем

router = Router()


@router.message(lambda msg: msg.text.startswith("/analytics"))
async def handle_analytics(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("⛔ Доступ запрещён.")
        return

    match = re.match(r"/analytics (\d{2}-\d{2}-\d{4}) - (\d{2}-\d{2}-\d{4})", message.text)
    if not match:
        await message.answer("⚠️ Неверный формат. Используйте: /analytics дд-мм-гггг - дд-мм-гггг")
        return

    date_from = datetime.strptime(match.group(1), "%d-%m-%Y").date()
    date_to = datetime.strptime(match.group(2), "%d-%m-%Y").date()

    data = await get_feedback_stats(date_from, date_to)
    path = await write_feedback_to_excel(data)

    await message.answer_document(FSInputFile(path), caption="📊 Статистика по встречам")
