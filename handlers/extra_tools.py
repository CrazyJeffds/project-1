import asyncio

from pathlib import Path

import qrcode

from PIL import Image

from aiogram import (
    Router,
    F
)

from aiogram.types import (
    CallbackQuery,
    Message,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from aiogram.fsm.context import FSMContext

from keyboards.extra_tools_menu import (
    extra_tools_menu
)

from states.extra_states import (
    ExtraStates
)

from database.db import (
    add_history
)


router = Router()


def back_to_extra_tools():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="extra_tools"
                )
            ]
        ]
    )


# =========================================
# МЕНЮ ИНСТРУМЕНТОВ
# =========================================

@router.callback_query(
    F.data == "extra_tools"
)
async def open_extra_tools(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.clear()

    await callback.message.edit_text(
        "🧰 <b>Дополнительные инструменты</b>\n\n"
        "Выбери действие:",
        reply_markup=extra_tools_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================
# QR-КОД
# =========================================

@router.callback_query(
    F.data == "tool_qr"
)
async def qr_start(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        ExtraStates.waiting_for_qr_text
    )

    await callback.message.edit_text(
        "🔳 <b>Создание QR-кода</b>\n\n"
        "Отправь текст или ссылку.",
        reply_markup=back_to_extra_tools(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.message(
    ExtraStates.waiting_for_qr_text,
    F.text
)
async def qr_create(
    message: Message,
    state: FSMContext
):

    Path(
        "storage/converted"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = Path(
        "storage/converted"
    ) / (
        f"qr_{message.from_user.id}.png"
    )

    image = qrcode.make(
        message.text
    )

    image.save(
        output_path
    )

    await message.answer_photo(
        FSInputFile(
            output_path
        ),
        caption="✅ QR-код готов"
    )

    add_history(
        message.from_user.id,
        "QR-код"
    )

    try:
        output_path.unlink()
    except FileNotFoundError:
        pass

    await state.clear()


# =========================================
# ИНФОРМАЦИЯ О ФАЙЛЕ
# =========================================

@router.callback_query(
    F.data == "tool_file_info"
)
async def file_info_start(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        ExtraStates.waiting_for_file_info
    )

    await callback.message.edit_text(
        "📋 <b>Информация о файле</b>\n\n"
        "Отправь файл, видео или аудио.",
        reply_markup=back_to_extra_tools(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.message(
    ExtraStates.waiting_for_file_info
)
async def file_info_handler(
    message: Message,
    state: FSMContext
):

    file_object = (
        message.document
        or message.video
        or message.audio
    )

    if not file_object:

        await message.answer(
            "❌ Отправь файл, видео или аудио."
        )

        return

    file_name = (
        getattr(
            file_object,
            "file_name",
            None
        )
        or "Без имени"
    )

    file_size_bytes = (
        getattr(
            file_object,
            "file_size",
            0
        )
        or 0
    )

    file_size_mb = (
        file_size_bytes
        / 1024
        / 1024
    )

    mime_type = (
        getattr(
            file_object,
            "mime_type",
            None
        )
        or "неизвестно"
    )

    text = (
        "📋 <b>Информация о файле</b>\n\n"
        f"📄 Имя: <code>{file_name}</code>\n"
        f"📦 Размер: <b>{file_size_mb:.2f} MB</b>\n"
        f"🧩 MIME: <code>{mime_type}</code>"
    )

    duration = getattr(
        file_object,
        "duration",
        None
    )

    width = getattr(
        file_object,
        "width",
        None
    )

    height = getattr(
        file_object,
        "height",
        None
    )

    if duration is not None:

        text += (
            f"\n⏱ Длительность: "
            f"<b>{duration} сек</b>"
        )

    if width and height:

        text += (
            f"\n📐 Разрешение: "
            f"<b>{width}×{height}</b>"
        )

    await message.answer(
        text,
        parse_mode="HTML"
    )

    add_history(
        message.from_user.id,
        "Информация о файле"
    )

    await state.clear()


# =========================================
# ГОЛОСОВОЕ -> MP3
# =========================================

@router.callback_query(
    F.data == "tool_voice_mp3"
)
async def voice_start(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        ExtraStates.waiting_for_voice
    )

    await callback.message.edit_text(
        "🎤 <b>Голосовое → MP3</b>\n\n"
        "Отправь голосовое сообщение.",
        reply_markup=back_to_extra_tools(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.message(
    ExtraStates.waiting_for_voice,
    F.voice
)
async def voice_to_mp3(
    message: Message,
    state: FSMContext
):

    Path(
        "storage/uploads"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    Path(
        "storage/converted"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    input_path = Path(
        "storage/uploads"
    ) / (
        f"{message.voice.file_unique_id}.ogg"
    )

    output_path = Path(
        "storage/converted"
    ) / (
        f"{message.voice.file_unique_id}.mp3"
    )

    telegram_file = await message.bot.get_file(
        message.voice.file_id
    )

    await message.bot.download_file(
        telegram_file.file_path,
        destination=input_path
    )

    process = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-c:a",
        "libmp3lame",
        "-b:a",
        "192k",
        str(output_path),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE
    )

    _, stderr = await process.communicate()

    if process.returncode != 0:

        await message.answer(
            "❌ Не удалось преобразовать голосовое."
        )

    else:

        await message.answer_audio(
            FSInputFile(
                output_path
            ),
            caption="✅ Голосовое → MP3"
        )

        add_history(
            message.from_user.id,
            "Голосовое → MP3",
            "ogg",
            "mp3"
        )

    for path in [
        input_path,
        output_path
    ]:

        try:
            path.unlink()
        except FileNotFoundError:
            pass

    await state.clear()


# =========================================
# КРУЖОК -> MP4
# =========================================

@router.callback_query(
    F.data == "tool_videonote_mp4"
)
async def videonote_start(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        ExtraStates.waiting_for_video_note
    )

    await callback.message.edit_text(
        "⭕ <b>Кружок → MP4</b>\n\n"
        "Отправь видеосообщение-кружок.",
        reply_markup=back_to_extra_tools(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.message(
    ExtraStates.waiting_for_video_note,
    F.video_note
)
async def videonote_to_mp4(
    message: Message,
    state: FSMContext
):

    Path(
        "storage/uploads"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    input_path = Path(
        "storage/uploads"
    ) / (
        f"{message.video_note.file_unique_id}.mp4"
    )

    telegram_file = await message.bot.get_file(
        message.video_note.file_id
    )

    await message.bot.download_file(
        telegram_file.file_path,
        destination=input_path
    )

    await message.answer_document(
        FSInputFile(
            input_path
        ),
        caption="✅ Кружок сохранён как MP4"
    )

    add_history(
        message.from_user.id,
        "Кружок → MP4",
        "video_note",
        "mp4"
    )

    try:
        input_path.unlink()
    except FileNotFoundError:
        pass

    await state.clear()


# =========================================
# СТИКЕР -> PNG
# =========================================

@router.callback_query(
    F.data == "tool_sticker_png"
)
async def sticker_start(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        ExtraStates.waiting_for_sticker
    )

    await callback.message.edit_text(
        "🏷 <b>Стикер → PNG</b>\n\n"
        "Отправь обычный статический стикер.",
        reply_markup=back_to_extra_tools(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.message(
    ExtraStates.waiting_for_sticker,
    F.sticker
)
async def sticker_to_png(
    message: Message,
    state: FSMContext
):

    if (
        message.sticker.is_animated
        or message.sticker.is_video
    ):

        await message.answer(
            "⚠️ Пока поддерживаются "
            "только обычные статические стикеры."
        )

        return

    Path(
        "storage/uploads"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    Path(
        "storage/converted"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    input_path = Path(
        "storage/uploads"
    ) / (
        f"{message.sticker.file_unique_id}.webp"
    )

    output_path = Path(
        "storage/converted"
    ) / (
        f"{message.sticker.file_unique_id}.png"
    )

    telegram_file = await message.bot.get_file(
        message.sticker.file_id
    )

    await message.bot.download_file(
        telegram_file.file_path,
        destination=input_path
    )

    with Image.open(
        input_path
    ) as image:

        image.save(
            output_path,
            "PNG"
        )

    await message.answer_document(
        FSInputFile(
            output_path
        ),
        caption="✅ Стикер → PNG"
    )

    add_history(
        message.from_user.id,
        "Стикер → PNG",
        "webp",
        "png"
    )

    for path in [
        input_path,
        output_path
    ]:

        try:
            path.unlink()
        except FileNotFoundError:
            pass

    await state.clear()
