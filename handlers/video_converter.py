import os
import asyncio
import logging

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from states.converter_states import ConverterStates


router = Router()


async def download_video_file(
    message: Message,
    file_id: str,
    unique_id: str,
    extension: str = "mp4"
):
    os.makedirs(
        "storage/uploads",
        exist_ok=True
    )

    input_path = (
        f"storage/uploads/"
        f"{unique_id}.{extension}"
    )

    telegram_file = await message.bot.get_file(
        file_id
    )

    await message.bot.download_file(
        telegram_file.file_path,
        destination=input_path
    )

    return input_path


# =========================================
# ВИДЕО -> MP3
# Если Telegram отправил как VIDEO
# =========================================

@router.message(
    ConverterStates.waiting_for_video_mp3,
    F.video
)
async def video_to_mp3_video(
    message: Message,
    state: FSMContext
):

    await convert_video_to_mp3(
        message=message,
        state=state,
        file_id=message.video.file_id,
        unique_id=message.video.file_unique_id
    )


# =========================================
# ВИДЕО -> MP3
# Если Telegram отправил как DOCUMENT
# =========================================

@router.message(
    ConverterStates.waiting_for_video_mp3,
    F.document
)
async def video_to_mp3_document(
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
        or filename.endswith(".avi")
    )

    if not is_video:

        await message.answer(
            "❌ Это не видеофайл.\n\n"
            "Отправь MP4, MOV, MKV, WEBM или AVI."
        )

        return

    await convert_video_to_mp3(
        message=message,
        state=state,
        file_id=message.document.file_id,
        unique_id=message.document.file_unique_id
    )


# =========================================
# ОСНОВНАЯ КОНВЕРТАЦИЯ
# =========================================

async def convert_video_to_mp3(
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
            "storage/converted",
            exist_ok=True
        )

        input_path = await download_video_file(
            message,
            file_id,
            unique_id
        )

        input_size = (
            os.path.getsize(input_path)
            / 1024
            / 1024
        )

        await status.edit_text(
            "🎵 Извлекаю аудио...\n\n"
            f"📦 Видео: {input_size:.2f} MB"
        )

        output_path = (
            f"storage/converted/"
            f"{unique_id}.mp3"
        )

        process = await asyncio.create_subprocess_exec(

            "ffmpeg",

            "-y",

            "-i",
            input_path,

            "-vn",

            "-c:a",
            "libmp3lame",

            "-b:a",
            "192k",

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
                "MP3-файл не создан"
            )

        mp3_size = (
            os.path.getsize(output_path)
            / 1024
            / 1024
        )

        logging.info(
            f"Видео → MP3 | "
            f"user_id={message.from_user.id} | "
            f"{input_size:.2f} MB -> "
            f"{mp3_size:.2f} MB"
        )

        await status.edit_text(
            "📤 Отправляю MP3..."
        )

        audio = FSInputFile(
            output_path
        )

        await message.answer_audio(
            audio=audio,
            caption=(
                "✅ Видео → MP3 готово\n\n"
                f"🎵 Размер MP3: "
                f"{mp3_size:.2f} MB"
            )
        )

        await status.delete()

        await state.clear()

    except Exception:

        logging.exception(
            "Ошибка Видео -> MP3"
        )

        await status.edit_text(
            "❌ Не удалось преобразовать видео в MP3."
        )

        await state.clear()

    finally:

        if (
            input_path
            and os.path.exists(input_path)
        ):
            try:
                os.remove(input_path)
            except Exception:
                pass

        if (
            output_path
            and os.path.exists(output_path)
        ):
            try:
                os.remove(output_path)
            except Exception:
                pass
