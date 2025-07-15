from typing import List

from openpyxl import Workbook
from datetime import datetime
import os

from db.models import MeetingFeedback

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)


def format_user(user) -> str:
    if user.username:
        return f"@{user.username}"

    return f"ID:{user.telegram_id}"


async def write_feedback_to_excel(feedback_list: List[MeetingFeedback]):
    wb = Workbook()
    ws = wb.active
    ws.append(["Опрошенный", "Партнер", "Получилось ли пообщаться", "Отзыв", "Дата"])

    for fb in feedback_list:
        user_display = format_user(fb.user)
        partner_display = format_user(fb.partner)

        ws.append([
            user_display,
            partner_display,
            "Да" if fb.is_met else "Нет",
            fb.comment or "",
            fb.date.strftime("%d-%m-%Y")
        ])

    filename = f"{EXPORT_DIR}/feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    wb.save(filename)

    return filename
