import asyncio
import logging
import shutil

from pathlib import Path

from aiogram import (
    Router,
    F
)

from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile
)

from aiogram.fsm.context import (
    FSMContext
)

from services.youtube_service import (
    get_media_info,
    download_youtube,
    download_mp3
)

from states.downloader_states import (
    DownloaderStates
)

from keyboards.download_media_menu import (
    download_media_menu
)

from keyboards.download_quality_menu import (
    download_quality_menu
)

from database.db import (
    add_history
)


router = Router()


# ==================================================
# ФОРМАТИРОВАНИЕ ВРЕМЕНИ
# ==================================================

def format_duration(
    seconds
):

    if not seconds:

        return "Неизвестно"

    seconds = int(
        seconds
    )

    hours = (
        seconds // 3600
    )

    minutes = (
        (seconds % 3600)
        // 60
    )

    seconds = (
        seconds % 60
    )

    if hours:

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    return (
        f"{minutes:02d}:"
        f"{seconds:02d}"
    )


# ==================================================
# ТЕКСТ ПРЕДПРОСМОТРА
# ==================================================

def build_preview_text(
    info
):

    max_height = info.get(
        "max_height"
    )

    if max_height:

        quality_text = (
            f"{max_height}p"
        )

    else:

        quality_text = (
            "Неизвестно"
        )

    duration = format_duration(
        info.get(
            "duration"
        )
    )

    title = info.get(
        "title",
        "Без названия"
    )

    uploader = info.get(
        "uploader",
        "Неизвестно"
    )

    # Telegram ограничивает длину,
    # поэтому очень длинный title режем.
    if len(title) > 120:

        title = (
            title[:117]
            + "..."
        )

    return (
        "◈ <b>ПРЕДПРОСМОТР</b>\n\n"

        "━━━━━━━━━━━━━━━━━━\n"

        f"🎬 <b>{title}</b>\n\n"

        f"👤 Автор: "
        f"<b>{uploader}</b>\n"

        f"⏱ Длительность: "
        f"<b>{duration}</b>\n"

        f"📺 Максимум: "
        f"<b>{quality_text}</b>\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "◈ Что скачать?"
    )


# ==================================================
# ПОЛУЧИЛИ ССЫЛКУ
# ==================================================

@router.message(
    F.text.startswith(
        (
            "http://",
            "https://"
        )
    )
)
async def receive_url(
    message: Message,
    state: FSMContext
):

    url = message.text.strip()

    status = await message.answer(
        "◈ <b>АНАЛИЗ ССЫЛКИ</b>\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🔍 Получаю информацию...\n"
        "━━━━━━━━━━━━━━━━━━",
        parse_mode="HTML"
    )

    try:

        info = await asyncio.to_thread(
            get_media_info,
            url
        )

    except Exception:

        logging.exception(
            "Ошибка получения информации "
            f"| user_id={message.from_user.id}"
        )

        await status.edit_text(
            "◈ <b>ОШИБКА</b>\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "❌ Не удалось получить информацию\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "Проверь ссылку и попробуй снова.",
            parse_mode="HTML"
        )

        return

    await state.clear()

    await state.update_data(
        download_url=url,
        download_info=info
    )

    await state.set_state(
        DownloaderStates.waiting_for_type
    )

    await status.edit_text(
        build_preview_text(
            info
        ),
        reply_markup=download_media_menu(),
        parse_mode="HTML"
    )


# ==================================================
# НАЗАД К ПРЕДПРОСМОТРУ
# ==================================================

@router.callback_query(
    F.data == "download_back_preview"
)
async def back_to_preview(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    info = data.get(
        "download_info"
    )

    if not info:

        await callback.answer(
            "Ссылка потеряна. "
            "Отправь её заново.",
            show_alert=True
        )

        await state.clear()

        return

    await state.set_state(
        DownloaderStates.waiting_for_type
    )

    await callback.message.edit_text(
        build_preview_text(
            info
        ),
        reply_markup=download_media_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# ВЫБРАЛИ ВИДЕО
# ==================================================

@router.callback_query(
    DownloaderStates.waiting_for_type,
    F.data == "download_type_video"
)
async def choose_video(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        DownloaderStates.waiting_for_quality
    )

    await callback.message.edit_text(
        "◈ <b>КАЧЕСТВО ВИДЕО</b>\n\n"

        "━━━━━━━━━━━━━━━━━━\n"

        "📱 360p — экономно\n"
        "📱 480p — стандарт\n"
        "💻 720p — HD\n"
        "🖥 1080p — Full HD\n"
        "⚡ АВТО — лучшее доступное\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "◈ Выбери качество:",

        reply_markup=download_quality_menu(),

        parse_mode="HTML"
    )

    await callback.answer()


# ==================================================
# ВЫБРАЛИ MP3
# ==================================================

@router.callback_query(
    DownloaderStates.waiting_for_type,
    F.data == "download_type_mp3"
)
async def choose_mp3(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    url = data.get(
        "download_url"
    )

    if not url:

        await callback.answer(
            "Ссылка потеряна",
            show_alert=True
        )

        await state.clear()

        return

    user_id = (
        callback.from_user.id
    )

    await callback.answer()

    await state.clear()

    await callback.message.edit_text(
        "◈ <b>MP3</b>\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🎵 Подготавливаю аудио...\n"
        "━━━━━━━━━━━━━━━━━━",
        parse_mode="HTML"
    )

    await download_media(
        message=callback.message,
        url=url,
        user_id=user_id,
        media_type="mp3",
        quality_text="MP3"
    )


# ==================================================
# ВЫБОР КАЧЕСТВА
# ==================================================

@router.callback_query(
    DownloaderStates.waiting_for_quality,
    F.data.startswith(
        "download_quality_"
    )
)
async def choose_quality(
    callback: CallbackQuery,
    state: FSMContext
):

    quality = callback.data.replace(
        "download_quality_",
        ""
    )

    allowed = {
        "360",
        "480",
        "720",
        "1080",
        "auto"
    }

    if quality not in allowed:

        await callback.answer(
            "Неверное качество",
            show_alert=True
        )

        return

    data = await state.get_data()

    url = data.get(
        "download_url"
    )

    if not url:

        await callback.answer(
            "Ссылка потеряна",
            show_alert=True
        )

        await state.clear()

        return

    if quality == "auto":

        quality_text = "АВТО"

    else:

        quality_text = (
            f"{quality}p"
        )

    user_id = (
        callback.from_user.id
    )

    await callback.answer()

    await state.clear()

    await callback.message.edit_text(
        "◈ <b>ПОДГОТОВКА</b>\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🎬 Качество: "
        f"<b>{quality_text}</b>\n"
        "⚡ Статус: "
        "<b>подготовка...</b>\n"
        "━━━━━━━━━━━━━━━━━━",
        parse_mode="HTML"
    )

    await download_media(
        message=callback.message,
        url=url,
        user_id=user_id,
        media_type="video",
        quality=quality,
        quality_text=quality_text
    )


# ==================================================
# СКАЧИВАНИЕ
# ==================================================

async def download_media(
    message,
    url,
    user_id,
    media_type,
    quality=None,
    quality_text=""
):

    logging.info(
        f"Скачивание | "
        f"user_id={user_id} | "
        f"type={media_type} | "
        f"quality={quality_text} | "
        f"url={url}"
    )

    status_message = await message.answer(
        "◈ <b>СКАЧИВАНИЕ</b>\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🎯 Формат: "
        f"<b>{quality_text}</b>\n"
        "📊 Прогресс: "
        "<b>0%</b>\n"
        "━━━━━━━━━━━━━━━━━━",
        parse_mode="HTML"
    )

    loop = (
        asyncio.get_running_loop()
    )

    last_percent = {
        "value": -10
    }

    # ==========================================
    # ПРОГРЕСС
    # ==========================================

    def progress_callback(
        percent
    ):

        if (
            percent != 100
            and
            percent
            < last_percent["value"] + 10
        ):

            return

        last_percent[
            "value"
        ] = percent

        async def update():

            try:

                await status_message.edit_text(
                    "◈ <b>СКАЧИВАНИЕ</b>\n\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"🎯 Формат: "
                    f"<b>{quality_text}</b>\n"
                    f"📊 Прогресс: "
                    f"<b>{percent}%</b>\n"
                    "⚡ Статус: "
                    "<b>загрузка</b>\n"
                    "━━━━━━━━━━━━━━━━━━",
                    parse_mode="HTML"
                )

            except Exception:
                pass

        asyncio.run_coroutine_threadsafe(
            update(),
            loop
        )

    file_path = None

    try:

        # ======================================
        # ВИДЕО
        # ======================================

        if media_type == "video":

            file_path = (
                await asyncio.to_thread(
                    download_youtube,
                    url,
                    progress_callback,
                    user_id,
                    quality
                )
            )

        # ======================================
        # MP3
        # ======================================

        else:

            file_path = (
                await asyncio.to_thread(
                    download_mp3,
                    url,
                    progress_callback,
                    user_id
                )
            )

        path = Path(
            file_path
        )

        if not path.exists():

            raise FileNotFoundError(
                "Итоговый файл отсутствует"
            )

        file_size_mb = (
            path.stat().st_size
            / 1024
            / 1024
        )

        extension = (
            path.suffix
            .lower()
            .replace(".", "")
        )

        await status_message.edit_text(
            "◈ <b>ГОТОВО</b>\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🎯 Формат: "
            f"<b>{quality_text}</b>\n"
            f"📦 Размер: "
            f"<b>{file_size_mb:.2f} MB</b>\n"
            "📤 Статус: "
            "<b>отправка</b>\n"
            "━━━━━━━━━━━━━━━━━━",
            parse_mode="HTML"
        )

        # ======================================
        # ОТПРАВКА MP3
        # ======================================

        if media_type == "mp3":

            await message.answer_audio(
                FSInputFile(
                    path
                ),
                caption=(
                    "◈ <b>ФАЙЛ ГОТОВ</b>\n\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "🎵 Формат: "
                    "<b>MP3</b>\n"
                    f"📦 Размер: "
                    f"<b>{file_size_mb:.2f} MB</b>\n"
                    "⚡ Статус: "
                    "<b>успешно</b>\n"
                    "━━━━━━━━━━━━━━━━━━"
                ),
                parse_mode="HTML"
            )

        # ======================================
        # ОТПРАВКА ВИДЕО
        # ======================================

        else:

            try:

                await message.answer_video(
                    FSInputFile(
                        path
                    ),
                    caption=(
                        "◈ <b>ФАЙЛ ГОТОВ</b>\n\n"
                        "━━━━━━━━━━━━━━━━━━\n"
                        f"🎬 Качество: "
                        f"<b>{quality_text}</b>\n"
                        f"📦 Размер: "
                        f"<b>{file_size_mb:.2f} MB</b>\n"
                        "⚡ Статус: "
                        "<b>успешно</b>\n"
                        "━━━━━━━━━━━━━━━━━━"
                    ),
                    parse_mode="HTML"
                )

            except Exception:

                await message.answer_document(
                    FSInputFile(
                        path
                    ),
                    caption="✅ Файл готов"
                )

        # ======================================
        # ИСТОРИЯ
        # ======================================

        try:

            add_history(
                user_id,
                (
                    "Скачивание MP3"
                    if media_type == "mp3"
                    else "Скачивание видео"
                ),
                extension,
                extension,
                file_size_mb,
                file_size_mb
            )

        except Exception:

            logging.exception(
                "Ошибка записи истории"
            )

        try:

            await status_message.delete()

        except Exception:
            pass

    except Exception:

        logging.exception(
            f"Ошибка скачивания | "
            f"user_id={user_id}"
        )

        try:

            await status_message.edit_text(
                "◈ <b>ОШИБКА</b>\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "❌ Не удалось скачать файл\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "Попробуй другую ссылку "
                "или другое качество.",
                parse_mode="HTML"
            )

        except Exception:
            pass

    finally:

        if file_path:

            try:

                path = Path(
                    file_path
                )

                parent = (
                    path.parent
                )

                if (
                    parent.exists()
                    and
                    parent.parent.name
                    == "downloads"
                ):

                    shutil.rmtree(
                        parent,
                        ignore_errors=True
                    )

                elif path.exists():

                    path.unlink()

            except Exception:

                logging.exception(
                    "Ошибка очистки "
                    "временных файлов"
                )
