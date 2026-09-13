from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def download_media_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎥  СКАЧАТЬ ВИДЕО",
                    callback_data="download_type_video"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🎵  СКАЧАТЬ MP3",
                    callback_data="download_type_mp3"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✕  ОТМЕНА",
                    callback_data="main_menu"
                )
            ]
        ]
    )
