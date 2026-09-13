import os
import asyncio
import logging

from PIL import Image

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from states.converter_states import ConverterStates


router = Router()


# ==================================================
# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ
# ==================================================

async def download_telegram_file(
    message: Message,
    file_id: str,
    file_unique_id: str,
    extension: str
):

    os.makedirs("storage/uploads", exist_ok=True)

    path = (
        f"storage/uploads/"
        f"{file_unique_id}.{extension}"
    )

    tg_file = await message.bot.get_file(file_id)

    await message.bot.download_file(
        tg_file.file_path,
        destination=path
    )

    return path


# ==================================================
# СЖАТИЕ ИЗОБРАЖЕНИЯ
# ==================================================

@router.message(
    ConverterStates.waiting_for_image_compress,
    F.photo
)
async def compress_photo(
    message: Message,
    state: FSMContext
):

    photo = message.photo[-1]

    await process_image(
        message=message,
        state=state,
        file_id=photo.file_id,
        unique_id=photo.file_unique_id
    )


@router.message(
    ConverterStates.waiting_for_image_compress,
    F.document
)
async def compress_image_document(
    message: Message,
    state: FSMContext
):

    mime = message.document.mime_type or ""

    if not mime.startswith("image/"):

        await message.answer(
            "❌ Это не изображение."
        )

        return

    await process_image(
        message=message,
        state=state,
        file_id=message.document.file_id,
        unique_id=message.document.file_unique_id
    )


async def process_image(
    message: Message,
    state: FSMContext,
    file_id: str,
    unique_id: str
):

    status = await message.answer(
        "🗜 Сжимаю изображение..."
    )

    input_path = None
    output_path = None

    try:

        os.makedirs(
            "storage/converted",
            exist_ok=True
        )

        input_path = await download_telegram_file(
            message,
            file_id,
            unique_id,
            "jpg"
        )

        output_path = (
            f"storage/converted/"
            f"{unique_id}_compressed.jpg"
        )

        old_size = (
            os.path.getsize(input_path)
            / 1024
            / 1024
        )

        with Image.open(input_path) as img:

            img = img.convert("RGB")

            # Если изображение очень большое —
            # уменьшаем максимальный размер
            img.thumbnail(
                (1920, 1920)
            )

            img.save(
                output_path,
                "JPEG",
                quality=60,
                optimize=True
            )

        new_size = (
            os.path.getsize(output_path)
            / 1024
            / 1024
        )

        logging.info(
            f"Сжатие изображения | "
            f"{old_size:.2f} MB -> "
            f"{new_size:.2f} MB"
        )

        result = FSInputFile(
            output_path
        )

        await message.answer_document(
            document=result,
            caption=(
                "✅ Изображение сжато\n\n"
                f"📦 Было: {old_size:.2f} MB\n"
                f"📉 Стало: {new_size:.2f} MB"
            )
        )

        await status.delete()

        await state.clear()

    except Exception:

        logging.exception(
            "Ошибка сжатия изображения"
        )

        await status.edit_text(
            "❌ Не удалось сжать изображение."
        )

        await state.clear()

    finally:

        if input_path and os.path.exists(input_path):
            os.remove(input_path)

        if output_path and os.path.exists(output_path):
            os.remove(output_path)


# ==================================================
# СЖАТИЕ ВИДЕО
# ==================================================

@router.message(
    ConverterStates.waiting_for_video_compress,
    F.video
)
async def compress_video(
    message: Message,
    state: FSMContext
):

    await process_video(
        message=message,
        state=state,
        file_id=message.video.file_id,
        unique_id=message.video.file_unique_id
    )


# MP4 часто отправляется через Telegram
# именно как документ
@router.message(
    ConverterStates.waiting_for_video_compress,
    F.document
)
async def compress_video_document(
    message: Message,
    state: FSMContext
):

    mime = message.document.mime_type or ""

    filename = (
        message.document.file_name
        or ""
    ).lower()

    is_video = (
        mime.startswith("video/")
        or filename.endswith(".mp4")
        or filename.endswith(".mov")
        or filename.endswith(".mkv")
        or filename.endswith(".webm")
    )

    if not is_video:

        await message.answer(
            "❌ Это не видеофайл.\n\n"
            "Отправь MP4, MOV, MKV или WEBM."
        )

        return

    await process_video(
        message=message,
        state=state,
        file_id=message.document.file_id,
        unique_id=message.document.file_unique_id
    )


async def process_video(
    message: Message,
    state: FSMContext,
    file_id: str,
    unique_id: str
):

    status = await message.answer(
        "📥 Загружаю видео..."
    )

    input_path = None
    output_path = None

    try:

        os.makedirs(
            "storage/uploads",
            exist_ok=True
        )

        os.makedirs(
            "storage/converted",
            exist_ok=True
        )

        input_path = await download_telegram_file(
            message,
            file_id,
            unique_id,
            "mp4"
        )

        old_size = (
            os.path.getsize(input_path)
            / 1024
            / 1024
        )

        await status.edit_text(
            f"🗜 Сжимаю видео...\n\n"
            f"📦 Исходный размер: "
            f"{old_size:.2f} MB"
        )

        output_path = (
            f"storage/converted/"
            f"{unique_id}_compressed.mp4"
        )

        # ffmpeg:
        # CRF выше = меньше файл / хуже качество
        # 28 — нормальный компромисс
        process = await asyncio.create_subprocess_exec(

            "ffmpeg",

            "-y",

            "-i",
            input_path,

            "-c:v",
            "libx264",

            "-preset",
            "medium",

            "-crf",
            "28",

            "-c:a",
            "aac",

            "-b:a",
            "96k",

            "-movflags",
            "+faststart",

            output_path,

            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE
        )

        _, stderr = await process.communicate()

        if process.returncode != 0:

            error_text = stderr.decode(
                errors="ignore"
            )

            logging.error(
                f"FFmpeg error:\n{error_text}"
            )

            raise RuntimeError(
                "FFmpeg завершился с ошибкой"
            )

        if not os.path.exists(output_path):

            raise FileNotFoundError(
                "Сжатое видео не найдено"
            )

        new_size = (
            os.path.getsize(output_path)
            / 1024
            / 1024
        )

        percent_saved = 0

        if old_size > 0:

            percent_saved = (
                (old_size - new_size)
                / old_size
                * 100
            )

        logging.info(
            f"Видео сжато | "
            f"{old_size:.2f} MB -> "
            f"{new_size:.2f} MB"
        )

        await status.edit_text(
            "📤 Отправляю сжатое видео..."
        )

        result = FSInputFile(
            output_path
        )

        await message.answer_video(
            video=result,
            caption=(
                "✅ Видео сжато\n\n"
                f"📦 Было: "
                f"{old_size:.2f} MB\n"
                f"📉 Стало: "
                f"{new_size:.2f} MB\n"
                f"💾 Экономия: "
                f"{percent_saved:.1f}%"
            )
        )

        await status.delete()

        await state.clear()

    except Exception:

        logging.exception(
            "Ошибка сжатия видео"
        )

        await status.edit_text(
            "❌ Не удалось сжать видео."
        )

        await state.clear()

    finally:

        if input_path and os.path.exists(input_path):

            try:
                os.remove(input_path)
            except Exception:
                pass

        if output_path and os.path.exists(output_path):

            try:
                os.remove(output_path)
            except Exception:
                pass
