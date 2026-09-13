import os
import asyncio
import logging

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from states.converter_states import ConverterStates


router = Router()


MAX_TELEGRAM_DOWNLOAD = 20 * 1024 * 1024


async def download_audio(
    message: Message,
    file_id: str,
    unique_id: str,
    extension: str
):
    os.makedirs(
        "storage/uploads",
        exist_ok=True
    )

    path = (
        f"storage/uploads/"
        f"{unique_id}.{extension}"
    )

    telegram_file = await message.bot.get_file(
        file_id
    )

    await message.bot.download_file(
        telegram_file.file_path,
        destination=path
    )

    return path


@router.message(
    ConverterStates.waiting_for_audio_convert,
    F.audio
)
async def convert_audio_message(
    message: Message,
    state: FSMContext
):

    file_size = message.audio.file_size or 0

    if file_size > MAX_TELEGRAM_DOWNLOAD:

        size_mb = file_size / 1024 / 1024

        await message.answer(
            f"❌ Файл слишком большой.\n\n"
            f"📦 Размер: {size_mb:.1f} MB\n"
            f"⚠️ Максимум сейчас: 20 MB.\n\n"
            f"Отправь другой аудиофайл."
        )

        return

    filename = (
        message.audio.file_name
        or "audio.mp3"
    )

    extension = os.path.splitext(
        filename
    )[1].lower().replace(".", "")

    if not extension:
        extension = "mp3"

    await process_audio(
        message=message,
        state=state,
        file_id=message.audio.file_id,
        unique_id=message.audio.file_unique_id,
        input_extension=extension
    )


@router.message(
    ConverterStates.waiting_for_audio_convert,
    F.document
)
async def convert_audio_document(
    message: Message,
    state: FSMContext
):

    filename = (
        message.document.file_name
        or ""
    )

    extension = os.path.splitext(
        filename
    )[1].lower().replace(".", "")

    mime = (
        message.document.mime_type
        or ""
    )

    audio_extensions = [
        "mp3",
        "wav",
        "flac",
        "aac",
        "m4a",
        "m4r",
        "ogg",
        "opus",
        "wma"
    ]

    is_audio = (
        mime.startswith("audio/")
        or extension in audio_extensions
    )

    if not is_audio:

        await message.answer(
            "❌ Это не аудиофайл.\n\n"
            "Поддерживаются:\n"
            "MP3, WAV, FLAC, AAC, M4A, "
            "M4R, OGG, OPUS, WMA"
        )

        return

    file_size = (
        message.document.file_size
        or 0
    )

    if file_size > MAX_TELEGRAM_DOWNLOAD:

        size_mb = (
            file_size
            / 1024
            / 1024
        )

        await message.answer(
            f"❌ Файл слишком большой.\n\n"
            f"📦 Размер: {size_mb:.1f} MB\n"
            f"⚠️ Максимум сейчас: 20 MB."
        )

        return

    if not extension:
        extension = "mp3"

    await process_audio(
        message=message,
        state=state,
        file_id=message.document.file_id,
        unique_id=message.document.file_unique_id,
        input_extension=extension
    )


async def process_audio(
    message: Message,
    state: FSMContext,
    file_id: str,
    unique_id: str,
    input_extension: str
):

    status = await message.answer(
        "📥 Загружаю аудио..."
    )

    input_path = None
    output_path = None

    try:

        data = await state.get_data()

        output_format = data.get(
            "audio_output_format"
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
            raise ValueError(
                "Формат аудио не выбран"
            )

        os.makedirs(
            "storage/converted",
            exist_ok=True
        )

        input_path = await download_audio(
            message,
            file_id,
            unique_id,
            input_extension
        )

        old_size = (
            os.path.getsize(input_path)
            / 1024
            / 1024
        )

        output_path = (
            f"storage/converted/"
            f"{unique_id}.{output_format}"
        )

        await status.edit_text(
            f"🔄 Конвертирую аудио...\n\n"
            f"🎵 {input_extension.upper()} "
            f"→ {output_format.upper()}\n"
            f"📦 Размер: {old_size:.2f} MB"
        )

        command = create_ffmpeg_command(
            input_path,
            output_path,
            output_format
        )

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE
        )

        _, stderr = await process.communicate()

        if process.returncode != 0:

            logging.error(
                stderr.decode(
                    errors="ignore"
                )
            )

            raise RuntimeError(
                "FFmpeg завершился с ошибкой"
            )

        new_size = (
            os.path.getsize(output_path)
            / 1024
            / 1024
        )

        await status.edit_text(
            f"📤 Отправляю "
            f"{output_format.upper()}..."
        )

        result = FSInputFile(
            output_path
        )

        await message.answer_audio(
            audio=result,
            caption=(
                f"✅ Конвертация завершена\n\n"
                f"🎵 {input_extension.upper()} "
                f"→ {output_format.upper()}\n"
                f"📦 Было: {old_size:.2f} MB\n"
                f"📦 Стало: {new_size:.2f} MB"
            )
        )

        await status.delete()

        await state.clear()

    except Exception:

        logging.exception(
            "Ошибка конвертации аудио"
        )

        await status.edit_text(
            "❌ Не удалось конвертировать аудио."
        )

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


def create_ffmpeg_command(
    input_path: str,
    output_path: str,
    output_format: str
):

    base = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-vn"
    ]

    if output_format == "mp3":
        return base + [
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            output_path
        ]

    if output_format == "wav":
        return base + [
            "-c:a",
            "pcm_s16le",
            output_path
        ]

    if output_format == "flac":
        return base + [
            "-c:a",
            "flac",
            output_path
        ]

    if output_format == "aac":
        return base + [
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            output_path
        ]

    if output_format == "m4a":
        return base + [
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            output_path
        ]

    if output_format == "m4r":
        return base + [
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-f",
            "ipod",
            output_path
        ]

    if output_format == "ogg":
        return base + [
            "-c:a",
            "libvorbis",
            "-q:a",
            "5",
            output_path
        ]

    raise ValueError(
        "Неподдерживаемый аудиоформат"
    )
