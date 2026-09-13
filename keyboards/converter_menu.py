from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def video_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Конвертировать видео",
                    callback_data="video_convert"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✂️ Обрезать видео",
                    callback_data="trim_video"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗜 Сжать видео",
                    callback_data="compress_video"
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


def video_format_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="MP4",
                    callback_data="convert_format_mp4"
                ),
                InlineKeyboardButton(
                    text="MOV",
                    callback_data="convert_format_mov"
                )
            ],
            [
                InlineKeyboardButton(
                    text="AVI",
                    callback_data="convert_format_avi"
                ),
                InlineKeyboardButton(
                    text="WMV",
                    callback_data="convert_format_wmv"
                )
            ],
            [
                InlineKeyboardButton(
                    text="WEBM",
                    callback_data="convert_format_webm"
                ),
                InlineKeyboardButton(
                    text="MP3",
                    callback_data="video_to_mp3"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="video_tools"
                )
            ]
        ]
    )


def audio_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="MP3",
                    callback_data="audio_format_mp3"
                ),
                InlineKeyboardButton(
                    text="WAV",
                    callback_data="audio_format_wav"
                )
            ],
            [
                InlineKeyboardButton(
                    text="FLAC",
                    callback_data="audio_format_flac"
                ),
                InlineKeyboardButton(
                    text="AAC",
                    callback_data="audio_format_aac"
                )
            ],
            [
                InlineKeyboardButton(
                    text="M4A",
                    callback_data="audio_format_m4a"
                ),
                InlineKeyboardButton(
                    text="M4R",
                    callback_data="audio_format_m4r"
                )
            ],
            [
                InlineKeyboardButton(
                    text="OGG",
                    callback_data="audio_format_ogg"
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


def document_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 PDF → Word",
                    callback_data="pdf_to_word"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🖼 Фото → PDF",
                    callback_data="images_to_pdf"
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


def image_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="JPG → PNG",
                    callback_data="jpg_to_png"
                )
            ],
            [
                InlineKeyboardButton(
                    text="PNG → JPG",
                    callback_data="png_to_jpg"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Фото → PDF",
                    callback_data="images_to_pdf"
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


def compress_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎬 Сжать видео",
                    callback_data="compress_video"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🖼 Сжать изображение",
                    callback_data="compress_image"
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


def torture_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔪 Нож",
                    callback_data="torture_knife"
                ),
                InlineKeyboardButton(
                    text="🪚 Бензопила",
                    callback_data="torture_chainsaw"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔨 Молоток",
                    callback_data="torture_hammer"
                ),
                InlineKeyboardButton(
                    text="💥 Гранатомёт",
                    callback_data="torture_launcher"
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


def back_menu():
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
