from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def settings_menu(
    video_quality,
    audio_bitrate
):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=(
                        f"🎬 Качество видео: "
                        f"{video_quality}p"
                    ),
                    callback_data=(
                        "settings_video_quality"
                    )
                )
            ],

            [
                InlineKeyboardButton(
                    text=(
                        f"🎵 MP3: "
                        f"{audio_bitrate} kbps"
                    ),
                    callback_data=(
                        "settings_audio_bitrate"
                    )
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


def video_quality_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="360p",
                    callback_data="vq_360"
                ),
                InlineKeyboardButton(
                    text="480p",
                    callback_data="vq_480"
                )
            ],

            [
                InlineKeyboardButton(
                    text="720p",
                    callback_data="vq_720"
                ),
                InlineKeyboardButton(
                    text="1080p",
                    callback_data="vq_1080"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="settings_menu"
                )
            ]
        ]
    )


def audio_bitrate_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="128 kbps",
                    callback_data="ab_128"
                ),
                InlineKeyboardButton(
                    text="192 kbps",
                    callback_data="ab_192"
                )
            ],

            [
                InlineKeyboardButton(
                    text="256 kbps",
                    callback_data="ab_256"
                ),
                InlineKeyboardButton(
                    text="320 kbps",
                    callback_data="ab_320"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="settings_menu"
                )
            ]
        ]
    )
