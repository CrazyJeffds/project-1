import logging

from aiogram import Router, F
from aiogram.types import (
    PreCheckoutQuery,
    Message
)


router = Router()


@router.pre_checkout_query()
async def pre_checkout_handler(
    query: PreCheckoutQuery
):

    logging.info(
        f"Проверка платежа | "
        f"user_id={query.from_user.id} | "
        f"amount={query.total_amount} | "
        f"currency={query.currency}"
    )

    if query.currency != "XTR":

        await query.answer(
            ok=False,
            error_message="Неверная валюта платежа."
        )

        return

    await query.answer(
        ok=True
    )


@router.message(F.successful_payment)
async def successful_payment_handler(
    message: Message
):

    payment = message.successful_payment

    logging.info(
        f"ПЛАТЁЖ УСПЕШЕН | "
        f"user_id={message.from_user.id} | "
        f"amount={payment.total_amount} | "
        f"currency={payment.currency} | "
        f"charge_id="
        f"{payment.telegram_payment_charge_id}"
    )

    await message.answer(
        "❤️ <b>Спасибо за поддержку!</b>\n\n"
        f"⭐ Ты отправил: "
        f"<b>{payment.total_amount} Stars</b>\n\n"
        "Поддержка помогает развивать проект 🚀",
        parse_mode="HTML"
    )
