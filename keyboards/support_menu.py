from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def support_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⭐ 25",
                    callback_data="support_amount_25"
                ),
                InlineKeyboardButton(
                    text="⭐ 50",
                    callback_data="support_amount_50"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐ 100",
                    callback_data="support_amount_100"
                ),
                InlineKeyboardButton(
                    text="⭐ 250",
                    callback_data="support_amount_250"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐ 500",
                    callback_data="support_amount_500"
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
