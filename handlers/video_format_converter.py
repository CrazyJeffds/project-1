import os
import asyncio
import logging

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from states.converter_states import ConverterStates


router = Router()


MAX_TELEGRAM_DOWNLOAD = 20 * 1024 * 1024


async def download_video(
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


# =========================================
# ЕСЛИ ВИДЕО ОТПРАВЛЕНО КАК VIDEO
# =========================================

@router.message(
    ConverterStates.waiting_for_video_convert,
    F.video
)
async def convert_video_message(
    message: Message,
    state: FSMContext
):

    file_size = message.video.file_size or 0

    if file_size > MAX_TELEGRAM_DOWNLOAD:

        size_mb = file_size / 1024 / 1024

        await message.answer(
            f"❌ Файл слишком большой.\n\n"
            f"📦 Размер: {size_mb:.1f} MB\n"
            f"⚠️ Максимум сейчас: 20 MB.\n\n"
            f"🔄 Отправь другое видео меньше 20 MB."
        )

        # ВАЖНО:
        # state.clear() тут НЕ делаем.
        # Бот продолжает ждать видео.

        return

    await process_conversion(
        message=message,
        state=state,
        file_id=message.video.file_id,
        unique_id=message.video.file_unique_id,
        input_extension="mp4"
    )


# =========================================
# ЕСЛИ ВИДЕО ОТПРАВЛЕНО КАК DOCUMENT
# =========================================

@router.message(
    ConverterStates.waiting_for_video_convert,
    F.document
)
async def convert_video_document(
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

    mime = message.document.mime_type or ""

    video_extensions = [
        "mp4",
        "mov",
        "avi",
        "wmv",
        "webm",
        "mkv",
        "m4v"
    ]

    is_video = (
        mime.startswith("video/")
        or extension in video_extensions
    )

    if not is_video:

        await message.answer(
            "❌ Это не видеофайл.\n\n"
            "Поддерживаются:\n"
            "MP4, MOV, AVI, WMV, WEBM, MKV, M4V\n\n"
            "Отправь видеофайл."
        )

        # Состояние тоже сохраняем.
        return

    file_size = message.document.file_size or 0

    if file_size > MAX_TELEGRAM_DOWNLOAD:

        size_mb = file_size / 1024 / 1024

        await message.answer(
            f"❌ Файл слишком большой.\n\n"
            f"📦 Размер: {size_mb:.1f} MB\n"
            f"⚠️ Максимум сейчас: 20 MB.\n\n"
            f"🔄 Отправь другое видео меньше 20 MB."
        )

        # НЕ очищаем состояние
        return

    if not extension:
        extension = "mp4"

    await process_conversion(
        message=message,
        state=state,
        file_id=message.document.file_id,
        unique_id=message.document.file_unique_id,
        input_extension=extension
    )


# =========================================
# КОНВЕРТАЦИЯ
# =========================================

async def process_conversion(
    message: Message,
    state: FSMContext,
    file_id: str,
    unique_id: str,
    input_extension: str
):

    status = await message.answer(
        "📥 Загружаю видео..."
    )

    input_path = None
    output_path = None

    try:

        data = await state.get_data()

        output_format = data.get(
            "video_output_format"
        )

        allowed_formats = [
            "mp4",
            "mov",
            "avi",
            "wmv",
            "webm"
        ]

        if output_format not in allowed_formats:

            raise ValueError(
                "Формат конвертации не выбран"
            )

        os.makedirs(
            "storage/converted",
            exist_ok=True
        )

        input_path = await download_video(
            message,
            file_id,
            unique_id,
            input_extension
        )

        original_size = (
            os.path.getsize(input_path)
            / 1024
            / 1024
        )

        output_path = (
            f"storage/converted/"
            f"{unique_id}.{output_format}"
        )

        await status.edit_text(
            f"🔄 Конвертирую видео...\n\n"
            f"🎬 {input_extension.upper()} "
            f"→ {output_format.upper()}\n"
            f"📦 Размер: {original_size:.2f} MB"
        )

        command = create_ffmpeg_command(
            input_path,
            output_path,
            output_format
        )

        logging.info(
            f"Конвертация видео | "
            f"user_id={message.from_user.id} | "
            f"{input_extension} -> {output_format}"
        )

        process = await asyncio.create_subprocess_exec(
            *command,
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
                "Конвертированный файл не найден"
            )

        result_size = (
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

        caption = (
            f"✅ Конвертация завершена\n\n"
            f"🎬 {input_extension.upper()} "
            f"→ {output_format.upper()}\n"
            f"📦 Было: {original_size:.2f} MB\n"
            f"📦 Стало: {result_size:.2f} MB"
        )

        if output_format in [
            "mp4",
            "mov",
            "webm"
        ]:

            try:

                await message.answer_video(
                    video=result,
                    caption=caption
                )

            except Exception:

                result = FSInputFile(
                    output_path
                )

                await message.answer_document(
                    document=result,
                    caption=caption
                )

        else:

            await message.answer_document(
                document=result,
                caption=caption
            )

        await status.delete()

        logging.info(
            f"Видео сконвертировано | "
            f"user_id={message.from_user.id} | "
            f"{input_extension} -> "
            f"{output_format} | "
            f"{original_size:.2f} MB -> "
            f"{result_size:.2f} MB"
        )

        # Только после УСПЕШНОЙ конвертации
        # выходим из состояния.
        await state.clear()

    except Exception:

        logging.exception(
            "Ошибка конвертации видео"
        )

        try:

            await status.edit_text(
                "❌ Не удалось конвертировать видео.\n\n"
                "Можешь отправить другой файл."
            )

        except Exception:
            pass

        # Тут тоже специально НЕ state.clear()
        # чтобы можно было сразу попробовать другой файл.

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


# =========================================
# КОМАНДЫ FFMPEG
# =========================================

def create_ffmpeg_command(
    input_path: str,
    output_path: str,
    output_format: str
):

    base = [
        "ffmpeg",
        "-y",
        "-i",
        input_path
    ]

    if output_format == "mp4":

        return base + [
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "23",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            output_path
        ]

    if output_format == "mov":

        return base + [
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "23",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            output_path
        ]

    if output_format == "avi":

        return base + [
            "-c:v",
            "mpeg4",
            "-q:v",
            "5",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            output_path
        ]

    if output_format == "wmv":

        return base + [
            "-c:v",
            "wmv2",
            "-b:v",
            "2500k",
            "-c:a",
            "wmav2",
            "-b:a",
            "192k",
            output_path
        ]

    if output_format == "webm":

        return base + [
            "-c:v",
            "libvpx-vp9",
            "-crf",
            "32",
            "-b:v",
            "0",
            "-c:a",
            "libopus",
            "-b:a",
            "128k",
            output_path
        ]

    raise ValueError(
        "Неподдерживаемый формат"
    )
