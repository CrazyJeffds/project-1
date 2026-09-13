from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def download_quality_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📱 360p",
                    callback_data="download_quality_360"
                ),

                InlineKeyboardButton(
                    text="📱 480p",
                    callback_data="download_quality_480"
                )
            ],

            [
                InlineKeyboardButton(
                    text="💻 720p HD",
                    callback_data="download_quality_720"
                ),

                InlineKeyboardButton(
                    text="🖥 1080p FULL HD",
                    callback_data="download_quality_1080"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⚡ АВТО",
                    callback_data="download_quality_auto"
                )
            ],

            [
                InlineKeyboardButton(
                    text="‹ НАЗАД",
                    callback_data="download_back_preview"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✕ ОТМЕНА",
                    callback_data="main_menu"
                )
            ]
        ]
    )
