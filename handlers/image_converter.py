import os
import logging

from PIL import Image

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from states.converter_states import ConverterStates
from keyboards.main_menu import main_menu


router = Router()


# ==========================================
# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ
# Скачивает фото или документ из Telegram
# ==========================================

async def download_image(message: Message, extension: str):

    os.makedirs("storage/uploads", exist_ok=True)
    os.makedirs("storage/converted", exist_ok=True)

    # Если пользователь отправил как обычное фото
    if message.photo:

        photo = message.photo[-1]

        file_id = photo.file_id
        unique_id = photo.file_unique_id

    # Если отправил как файл
    elif message.document:

        file_id = message.document.file_id
        unique_id = message.document.file_unique_id

    else:
        raise ValueError("Изображение не найдено")

    telegram_file = await message.bot.get_file(file_id)

    input_path = (
        f"storage/uploads/"
        f"{unique_id}.{extension}"
    )

    await message.bot.download_file(
        telegram_file.file_path,
        destination=input_path
    )

    return input_path, unique_id


# ==========================================
# PNG -> JPG
# ==========================================

@router.message(
    ConverterStates.waiting_for_png,
    F.document
)
async def png_to_jpg_document(
    message: Message,
    state: FSMContext
):

    status = await message.answer(
        "🔄 Конвертирую PNG → JPG..."
    )

    input_path = None
    output_path = None

    try:

        mime = message.document.mime_type

        if mime != "image/png":

            await status.edit_text(
                "❌ Это не PNG-файл.\n\n"
                "Отправь изображение формата .png"
            )

            return

        input_path, unique_id = await download_image(
            message,
            "png"
        )

        output_path = (
            f"storage/converted/"
            f"{unique_id}.jpg"
        )

        with Image.open(input_path) as image:

            # JPG не поддерживает прозрачность
            if image.mode in ("RGBA", "LA"):

                background = Image.new(
                    "RGB",
                    image.size,
                    "white"
                )

                alpha = image.getchannel("A")

                background.paste(
                    image,
                    mask=alpha
                )

                image = background

            else:

                image = image.convert("RGB")

            image.save(
                output_path,
                "JPEG",
                quality=95
            )

        result = FSInputFile(output_path)

        await message.answer_document(
            document=result,
            caption="✅ PNG → JPG готово"
        )

        await status.delete()

        logging.info(
            f"PNG → JPG | "
            f"user_id={message.from_user.id}"
        )

        await state.clear()

    except Exception:

        logging.exception(
            "Ошибка PNG -> JPG"
        )

        await status.edit_text(
            "❌ Ошибка при конвертации PNG → JPG."
        )

        await state.clear()

    finally:

        if input_path and os.path.exists(input_path):
            os.remove(input_path)

        if output_path and os.path.exists(output_path):
            os.remove(output_path)


# ==========================================
# Если PNG отправили как обычную фотографию
# ==========================================

@router.message(
    ConverterStates.waiting_for_png,
    F.photo
)
async def png_as_photo(
    message: Message
):

    await message.answer(
        "⚠️ PNG лучше отправлять как <b>Файл</b>, "
        "а не как фотографию.\n\n"
        "📎 Нажми скрепку → Файл → выбери PNG.\n\n"
        "Telegram может автоматически превратить "
        "обычное фото в JPEG.",
        parse_mode="HTML"
    )


# ==========================================
# JPG -> PNG
# ==========================================

@router.message(
    ConverterStates.waiting_for_jpg,
    F.photo
)
async def jpg_photo_to_png(
    message: Message,
    state: FSMContext
):

    await convert_jpg_to_png(
        message,
        state
    )


@router.message(
    ConverterStates.waiting_for_jpg,
    F.document
)
async def jpg_document_to_png(
    message: Message,
    state: FSMContext
):

    mime = message.document.mime_type

    if mime not in [
        "image/jpeg",
        "image/jpg"
    ]:

        await message.answer(
            "❌ Отправь JPG/JPEG изображение."
        )

        return

    await convert_jpg_to_png(
        message,
        state
    )


async def convert_jpg_to_png(
    message: Message,
    state: FSMContext
):

    status = await message.answer(
        "🔄 Конвертирую JPG → PNG..."
    )

    input_path = None
    output_path = None

    try:

        input_path, unique_id = await download_image(
            message,
            "jpg"
        )

        output_path = (
            f"storage/converted/"
            f"{unique_id}.png"
        )

        with Image.open(input_path) as image:

            image.save(
                output_path,
                "PNG",
                optimize=True
            )

        result = FSInputFile(output_path)

        await message.answer_document(
            document=result,
            caption="✅ JPG → PNG готово"
        )

        await status.delete()

        logging.info(
            f"JPG → PNG | "
            f"user_id={message.from_user.id}"
        )

        await state.clear()

    except Exception:

        logging.exception(
            "Ошибка JPG -> PNG"
        )

        await status.edit_text(
            "❌ Ошибка при конвертации JPG → PNG."
        )

        await state.clear()

    finally:

        if input_path and os.path.exists(input_path):
            os.remove(input_path)

        if output_path and os.path.exists(output_path):
            os.remove(output_path)


# ==========================================
# СЖАТИЕ ИЗОБРАЖЕНИЯ
# ==========================================

@router.message(
    ConverterStates.waiting_for_image_compress,
    F.photo
)
async def compress_photo(
    message: Message,
    state: FSMContext
):

    await compress_image(
        message,
        state
    )


@router.message(
    ConverterStates.waiting_for_image_compress,
    F.document
)
async def compress_document(
    message: Message,
    state: FSMContext
):

    mime = message.document.mime_type or ""

    if not mime.startswith("image/"):

        await message.answer(
            "❌ Это не изображение."
        )

        return

    await compress_image(
        message,
        state
    )


async def compress_image(
    message: Message,
    state: FSMContext
):

    status = await message.answer(
        "🗜 Сжимаю изображение..."
    )

    input_path = None
    output_path = None

    try:

        input_path, unique_id = await download_image(
            message,
            "jpg"
        )

        output_path = (
            f"storage/converted/"
            f"{unique_id}_compressed.jpg"
        )

        original_size = (
            os.path.getsize(input_path)
            / 1024
            / 1024
        )

        with Image.open(input_path) as image:

            image = image.convert("RGB")

            image.save(
                output_path,
                "JPEG",
                quality=60,
                optimize=True
            )

        compressed_size = (
            os.path.getsize(output_path)
            / 1024
            / 1024
        )

        result = FSInputFile(output_path)

        await message.answer_document(
            document=result,
            caption=(
                "✅ Изображение сжато\n\n"
                f"📦 Было: {original_size:.2f} MB\n"
                f"📉 Стало: {compressed_size:.2f} MB"
            )
        )

        await status.delete()

        logging.info(
            f"Сжатие изображения | "
            f"user_id={message.from_user.id} | "
            f"{original_size:.2f} MB -> "
            f"{compressed_size:.2f} MB"
        )

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
