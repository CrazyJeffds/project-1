import os

from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from keyboards.converter_menu import torture_menu


router = Router()


ITEMS = [
    {
        "name": "🔪 Нож",
        "file": "assets/knife.jpg"
    },
    {
        "name": "🪚 Бензопила",
        "file": "assets/chainsaw.jpg"
    },
    {
        "name": "🔨 Молоток",
        "file": "assets/hammer.jpg"
    },
    {
        "name": "💥 Гранатомёт",
        "file": "assets/launcher.jpg"
    }
]


def gallery_keyboard(index: int):

    prev_index = (index - 1) % len(ITEMS)
    next_index = (index + 1) % len(ITEMS)

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=f"torture_show_{prev_index}"
                ),
                InlineKeyboardButton(
                    text=f"{index + 1}/{len(ITEMS)}",
                    callback_data="torture_ignore"
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=f"torture_show_{next_index}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="torture_back"
                )
            ]
        ]
    )


async def send_item(
    callback: CallbackQuery,
    index: int
):

    item = ITEMS[index]

    if not os.path.exists(item["file"]):

        await callback.answer(
            f"Файл не найден: {item['file']}",
            show_alert=True
        )

        return

    photo = FSInputFile(
        item["file"]
    )

    # Если уже открыта картинка галереи,
    # старую удаляем
    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer_photo(
        photo=photo,
        caption=(
            f"<b>{item['name']}</b>\n\n"
            f"Объект {index + 1} из {len(ITEMS)}"
        ),
        reply_markup=gallery_keyboard(index),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(
    F.data == "torture_knife"
)
async def show_knife(
    callback: CallbackQuery
):

    await send_item(
        callback,
        0
    )


@router.callback_query(
    F.data == "torture_chainsaw"
)
async def show_chainsaw(
    callback: CallbackQuery
):

    await send_item(
        callback,
        1
    )


@router.callback_query(
    F.data == "torture_hammer"
)
async def show_hammer(
    callback: CallbackQuery
):

    await send_item(
        callback,
        2
    )


@router.callback_query(
    F.data == "torture_launcher"
)
async def show_launcher(
    callback: CallbackQuery
):

    await send_item(
        callback,
        3
    )


@router.callback_query(
    F.data.startswith("torture_show_")
)
async def gallery_navigation(
    callback: CallbackQuery
):

    index = int(
        callback.data.replace(
            "torture_show_",
            ""
        )
    )

    await send_item(
        callback,
        index
    )


# ==============================
# НАЗАД В МЕНЮ ПЫТОК
# ==============================

@router.callback_query(
    F.data == "torture_back"
)
async def torture_back(
    callback: CallbackQuery
):

    # Удаляем фотографию галереи
    try:
        await callback.message.delete()
    except Exception:
        pass

    # Отправляем обычное меню заново
    await callback.message.answer(
        "🩸 <b>Пытки</b>\n\n"
        "Выбери предмет для просмотра:",
        reply_markup=torture_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(
    F.data == "torture_ignore"
)
async def ignore_button(
    callback: CallbackQuery
):

    await callback.answer()
