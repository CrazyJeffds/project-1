import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):

    logging.info(
        f"/start | user_id={message.from_user.id}"
    )

    text = (
        "◈ <b>NEON TOOLS</b>\n\n"

        "━━━━━━━━━━━━━━━━━━\n"
        "⚡ <b>МЕДИА И ФАЙЛОВЫЕ ИНСТРУМЕНТЫ</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"

        "📥 Скачивание медиа\n"
        "🎬 Работа с видео\n"
        "🎵 Работа с аудио\n"
        "🖼 Работа с изображениями\n"
        "📄 Работа с документами\n"
        "🧰 Дополнительные инструменты\n\n"

        "━━━━━━━━━━━━━━━━━━\n"
        "◈ Выбери нужный раздел"
    )

    await message.answer(
        text,
        reply_markup=main_menu(),
        parse_mode="HTML"
    )
