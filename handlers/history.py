from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.db import get_history


router = Router()


def history_back_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="main_menu"
                )
            ]
        ]
    )


@router.callback_query(F.data == "history_menu")
async def show_history(
    callback: CallbackQuery
):

    history = get_history(
        callback.from_user.id,
        limit=10
    )

    if not history:

        await callback.message.edit_text(
            "🕘 <b>История операций</b>\n\n"
            "Пока история пустая.",
            reply_markup=history_back_menu(),
            parse_mode="HTML"
        )

        await callback.answer()

        return

    text = (
        "🕘 <b>Последние операции</b>\n\n"
    )

    for index, item in enumerate(
        history,
        start=1
    ):

        action = item["action"]

        source_format = (
            item["source_format"]
            if item["source_format"]
            else "-"
        )

        target_format = (
            item["target_format"]
            if item["target_format"]
            else "-"
        )

        created_at = (
            item["created_at"]
            .replace("T", " ")
        )

        text += (
            f"<b>{index}.</b> {action}\n"
            f"Формат: "
            f"{source_format} → "
            f"{target_format}\n"
            f"Дата: {created_at}\n\n"
        )

    await callback.message.edit_text(
        text,
        reply_markup=history_back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()
