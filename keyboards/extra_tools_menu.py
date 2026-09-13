from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def extra_tools_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔳 QR-код",
                    callback_data="tool_qr"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Информация о файле",
                    callback_data="tool_file_info"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎤 Голосовое → MP3",
                    callback_data="tool_voice_mp3"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭕ Кружок → MP4",
                    callback_data="tool_videonote_mp4"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏷 Стикер → PNG",
                    callback_data="tool_sticker_png"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="main_menu"
                )
            ]
        ]
    )
