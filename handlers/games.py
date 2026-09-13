import random

from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import main_menu


router = Router()


def games_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎲 Угадай число 1–10",
                    callback_data="game_guess_start"
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


def guess_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1",
                    callback_data="guess_1"
                ),
                InlineKeyboardButton(
                    text="2",
                    callback_data="guess_2"
                ),
                InlineKeyboardButton(
                    text="3",
                    callback_data="guess_3"
                ),
                InlineKeyboardButton(
                    text="4",
                    callback_data="guess_4"
                ),
                InlineKeyboardButton(
                    text="5",
                    callback_data="guess_5"
                )
            ],
            [
                InlineKeyboardButton(
                    text="6",
                    callback_data="guess_6"
                ),
                InlineKeyboardButton(
                    text="7",
                    callback_data="guess_7"
                ),
                InlineKeyboardButton(
                    text="8",
                    callback_data="guess_8"
                ),
                InlineKeyboardButton(
                    text="9",
                    callback_data="guess_9"
                ),
                InlineKeyboardButton(
                    text="10",
                    callback_data="guess_10"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Новая игра",
                    callback_data="game_guess_start"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 В игры",
                    callback_data="games_menu"
                )
            ]
        ]
    )


@router.callback_query(F.data == "games_menu")
async def open_games_menu(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "🎮 <b>Игры</b>\n\n"
        "Выбери игру:",
        reply_markup=games_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(F.data == "game_guess_start")
async def start_guess_game(
    callback: CallbackQuery,
    state: FSMContext
):
    secret_number = random.randint(1, 10)

    await state.update_data(
        guess_secret=secret_number,
        guess_attempts=0
    )

    await callback.message.edit_text(
        "🎲 <b>Угадай число</b>\n\n"
        "Я загадал число от <b>1 до 10</b>.\n\n"
        "Нажми на число ниже 👇\n\n"
        "🎯 Попыток: 0",
        reply_markup=guess_keyboard(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("guess_")
)
async def process_guess(
    callback: CallbackQuery,
    state: FSMContext
):
    try:
        guessed_number = int(
            callback.data.replace(
                "guess_",
                ""
            )
        )
    except ValueError:
        await callback.answer()
        return

    data = await state.get_data()

    secret_number = data.get(
        "guess_secret"
    )

    attempts = data.get(
        "guess_attempts",
        0
    )

    if secret_number is None:
        await callback.answer(
            "Начни новую игру",
            show_alert=True
        )
        return

    attempts += 1

    await state.update_data(
        guess_attempts=attempts
    )

    if guessed_number == secret_number:

        await callback.message.edit_text(
            "🎉 <b>Ты угадал!</b>\n\n"
            f"🎯 Число: <b>{secret_number}</b>\n"
            f"🔢 Попыток: <b>{attempts}</b>\n\n"
            "Хочешь сыграть ещё?",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="🔄 Новая игра",
                            callback_data="game_guess_start"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🎮 Меню игр",
                            callback_data="games_menu"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🏠 Главное меню",
                            callback_data="main_menu"
                        )
                    ]
                ]
            ),
            parse_mode="HTML"
        )

        await callback.answer(
            "🎉 Правильно!"
        )

        return

    if guessed_number < secret_number:
        hint = "⬆️ Моё число <b>БОЛЬШЕ</b>"
    else:
        hint = "⬇️ Моё число <b>МЕНЬШЕ</b>"

    await callback.message.edit_text(
        "🎲 <b>Угадай число</b>\n\n"
        f"Ты выбрал: <b>{guessed_number}</b>\n\n"
        f"{hint}\n\n"
        f"🎯 Попыток: <b>{attempts}</b>",
        reply_markup=guess_keyboard(),
        parse_mode="HTML"
    )

    await callback.answer(
        "Не угадал 😈"
    )
