from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📥  СКАЧАТЬ",
                    callback_data="download"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🎬  ВИДЕО",
                    callback_data="video_tools"
                ),
                InlineKeyboardButton(
                    text="🎵  АУДИО",
                    callback_data="audio_tools"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🖼  ИЗОБРАЖЕНИЯ",
                    callback_data="image_tools"
                ),
                InlineKeyboardButton(
                    text="📄  ДОКУМЕНТЫ",
                    callback_data="document_tools"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🧰  ИНСТРУМЕНТЫ",
                    callback_data="extra_tools"
                ),
                InlineKeyboardButton(
                    text="🗜  СЖАТИЕ",
                    callback_data="compress_tools"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⚙️  НАСТРОЙКИ",
                    callback_data="settings_menu"
                ),
                InlineKeyboardButton(
                    text="🕘  ИСТОРИЯ",
                    callback_data="history_menu"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🎮  ИГРЫ",
                    callback_data="games_menu"
                ),
                InlineKeyboardButton(
                    text="🩸  ГАЛЕРЕЯ",
                    callback_data="torture_menu"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❤️  ПОДДЕРЖАТЬ ПРОЕКТ",
                    callback_data="support_project"
                )
            ]
        ]
    )
