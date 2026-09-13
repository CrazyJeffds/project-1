import logging

from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    LabeledPrice
)

from keyboards.support_menu import support_menu


router = Router()


@router.callback_query(F.data == "support_project")
async def open_support_menu(callback: CallbackQuery):

    logging.info(
        f"Открыто меню поддержки | "
        f"user_id={callback.from_user.id}"
    )

    await callback.message.edit_text(
        "❤️ <b>Поддержать проект</b>\n\n"
        "Если тебе нравится бот, можешь "
        "поддержать его развитие ⭐\n\n"
        "Выбери количество Stars:",
        reply_markup=support_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("support_amount_")
)
async def create_support_invoice(
    callback: CallbackQuery
):

    try:
        amount = int(
            callback.data.replace(
                "support_amount_",
                ""
            )
        )

    except ValueError:
        await callback.answer(
            "❌ Ошибка суммы",
            show_alert=True
        )
        return

    allowed_amounts = [
        25,
        50,
        100,
        250,
        500
    ]

    if amount not in allowed_amounts:
        await callback.answer(
            "❌ Недопустимая сумма",
            show_alert=True
        )
        return

    logging.info(
        f"Создание счёта | "
        f"user_id={callback.from_user.id} | "
        f"stars={amount}"
    )

    await callback.message.answer_invoice(
        title="❤️ Поддержать проект",

        description=(
            f"Добровольная поддержка проекта "
            f"на {amount} Telegram Stars"
        ),

        payload=(
            f"donation:"
            f"{callback.from_user.id}:"
            f"{amount}"
        ),

        currency="XTR",

        prices=[
            LabeledPrice(
                label="Поддержка проекта",
                amount=amount
            )
        ],

        provider_token=""
    )

    await callback.answer()
