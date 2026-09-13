import logging

from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    LabeledPrice
)
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import main_menu

from keyboards.converter_menu import (
    video_menu,
    video_format_menu,
    audio_menu,
    document_menu,
    image_menu,
    compress_menu,
    torture_menu,
    back_menu
)

from states.converter_states import ConverterStates


router = Router()


# ==================================================
# ГЛАВНОЕ МЕНЮ
# ==================================================

@router.callback_query(F.data == "main_menu")
async def open_main_menu(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    logging.info(
        f"Главное меню | user_id={callback.from_user.id}"
    )

    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>\n\n"
        "Выбери нужный инструмент 👇",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# СКАЧИВАНИЕ
# ==================================================

@router.callback_query(F.data == "download")
async def download_button(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "📥 <b>Скачать медиа</b>\n\n"
        "Отправь ссылку на видео или аудио.\n\n"
        "Можно попробовать:\n"
        "• YouTube\n"
        "• TikTok\n"
        "• Instagram\n"
        "• SoundCloud\n"
        "• VK\n\n"
        "Бот автоматически попробует определить сервис.",
        reply_markup=back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# ВИДЕО
# ==================================================

@router.callback_query(F.data == "video_tools")
async def open_video_tools(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "🎬 <b>Инструменты для видео</b>\n\n"
        "Выбери действие:",
        reply_markup=video_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# КОНВЕРТАЦИЯ ВИДЕО
# ==================================================

@router.callback_query(F.data == "video_convert")
async def video_convert(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "🔄 <b>Конвертация видео</b>\n\n"
        "Выбери формат:",
        reply_markup=video_format_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("convert_format_")
)
async def select_video_format(
    callback: CallbackQuery,
    state: FSMContext
):
    output_format = callback.data.replace(
        "convert_format_",
        ""
    )

    allowed_formats = [
        "mp4",
        "mov",
        "avi",
        "wmv",
        "webm"
    ]

    if output_format not in allowed_formats:
        await callback.answer(
            "❌ Неизвестный формат",
            show_alert=True
        )
        return

    await state.clear()

    await state.update_data(
        video_output_format=output_format
    )

    await state.set_state(
        ConverterStates.waiting_for_video_convert
    )

    await callback.message.edit_text(
        f"🎬 <b>Конвертация в "
        f"{output_format.upper()}</b>\n\n"
        f"Отправь видеофайл.\n\n"
        f"Результат будет: "
        f"<code>.{output_format}</code>",
        reply_markup=back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# ВИДЕО -> MP3
# ==================================================

@router.callback_query(F.data == "video_to_mp3")
async def video_to_mp3(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await state.set_state(
        ConverterStates.waiting_for_video_mp3
    )

    await callback.message.edit_text(
        "🎵 <b>Видео → MP3</b>\n\n"
        "Отправь видеофайл.",
        reply_markup=back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# СЖАТИЕ ВИДЕО
# ==================================================

@router.callback_query(F.data == "compress_video")
async def compress_video(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await state.set_state(
        ConverterStates.waiting_for_video_compress
    )

    await callback.message.edit_text(
        "🎬 <b>Сжатие видео</b>\n\n"
        "Отправь видеофайл.",
        reply_markup=back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# ОБРЕЗКА ВИДЕО
# ==================================================

@router.callback_query(F.data == "trim_video")
async def trim_video(
    callback: CallbackQuery
):
    await callback.message.edit_text(
        "✂️ <b>Обрезка видео</b>\n\n"
        "Эта функция пока ещё не реализована.",
        reply_markup=back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# АУДИО
# ==================================================

@router.callback_query(F.data == "audio_tools")
async def open_audio_tools(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "🎵 <b>Инструменты для аудио</b>\n\n"
        "Выбери формат:",
        reply_markup=audio_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# ВЫБОР ФОРМАТА АУДИО
# ==================================================

@router.callback_query(
    F.data.startswith("audio_format_")
)
async def select_audio_format(
    callback: CallbackQuery,
    state: FSMContext
):
    output_format = callback.data.replace(
        "audio_format_",
        ""
    )

    allowed_formats = [
        "mp3",
        "wav",
        "flac",
        "aac",
        "m4a",
        "m4r",
        "ogg"
    ]

    if output_format not in allowed_formats:
        await callback.answer(
            "❌ Неизвестный формат",
            show_alert=True
        )
        return

    await state.clear()

    await state.update_data(
        audio_output_format=output_format
    )

    await state.set_state(
        ConverterStates.waiting_for_audio_convert
    )

    logging.info(
        f"Аудио формат {output_format} | "
        f"user_id={callback.from_user.id}"
    )

    await callback.message.edit_text(
        f"🎵 <b>Конвертация аудио "
        f"в {output_format.upper()}</b>\n\n"
        f"Отправь аудиофайл.\n\n"
        f"Результат будет: "
        f"<code>.{output_format}</code>",
        reply_markup=back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# ДОКУМЕНТЫ
# ==================================================

@router.callback_query(F.data == "document_tools")
async def open_document_tools(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "📄 <b>Документы</b>\n\n"
        "Выбери действие:",
        reply_markup=document_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(F.data == "pdf_to_word")
async def pdf_to_word(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await state.set_state(
        ConverterStates.waiting_for_pdf
    )

    await callback.message.edit_text(
        "📄 <b>PDF → Word</b>\n\n"
        "Отправь PDF-файл.",
        reply_markup=back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(F.data == "images_to_pdf")
async def images_to_pdf(
    callback: CallbackQuery
):
    await callback.message.edit_text(
        "🖼 <b>Фото → PDF</b>\n\n"
        "Эта функция пока ещё не реализована.",
        reply_markup=back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# ИЗОБРАЖЕНИЯ
# ==================================================

@router.callback_query(F.data == "image_tools")
async def open_image_tools(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "🖼 <b>Изображения</b>\n\n"
        "Выбери действие:",
        reply_markup=image_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(F.data == "jpg_to_png")
async def jpg_to_png(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await state.set_state(
        ConverterStates.waiting_for_jpg
    )

    await callback.message.edit_text(
        "🖼 <b>JPG → PNG</b>\n\n"
        "Отправь JPG/JPEG изображение.",
        reply_markup=back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(F.data == "png_to_jpg")
async def png_to_jpg(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await state.set_state(
        ConverterStates.waiting_for_png
    )

    await callback.message.edit_text(
        "🖼 <b>PNG → JPG</b>\n\n"
        "Отправь PNG-изображение.",
        reply_markup=back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# СЖАТИЕ
# ==================================================

@router.callback_query(F.data == "compress_tools")
async def open_compress_tools(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "🗜 <b>Сжатие файлов</b>\n\n"
        "Выбери действие:",
        reply_markup=compress_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(F.data == "compress_image")
async def compress_image(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await state.set_state(
        ConverterStates.waiting_for_image_compress
    )

    await callback.message.edit_text(
        "🖼 <b>Сжатие изображения</b>\n\n"
        "Отправь изображение.",
        reply_markup=back_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# ПЫТКИ / ГАЛЕРЕЯ
# ==================================================

@router.callback_query(F.data == "torture_menu")
async def open_torture_menu(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "🩸 <b>Пытки</b>\n\n"
        "Выбери предмет для просмотра:",
        reply_markup=torture_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# ПОДДЕРЖАТЬ ПРОЕКТ
# ==================================================

@router.callback_query(F.data == "support_project")
async def support_project(
    callback: CallbackQuery
):
    await callback.message.answer_invoice(
        title="❤️ Поддержать проект",
        description=(
            "Если тебе нравится бот, "
            "можешь поддержать его развитие ❤️"
        ),

        payload="support_project",

        # Telegram Stars
        currency="XTR",

        prices=[
            LabeledPrice(
                label="Поддержка проекта",
                amount=50
            )
        ]
    )

    logging.info(
        f"Открыт платёж поддержки | "
        f"user_id={callback.from_user.id}"
    )

    await callback.answer()
