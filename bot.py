import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from database.db import init_db

from handlers.start import router as start_router
from handlers.support import router as support_router
from handlers.payments import router as payments_router
from handlers.callbacks import router as callbacks_router
from handlers.games import router as games_router
from handlers.torture_gallery import router as torture_router
from handlers.settings import router as settings_router
from handlers.history import router as history_router
from handlers.extra_tools import router as extra_tools_router
from handlers.compress import router as compress_router
from handlers.image_converter import router as image_router
from handlers.video_converter import router as video_converter_router
from handlers.video_format_converter import router as video_format_router
from handlers.audio_converter import router as audio_converter_router
from handlers.downloader import router as downloader_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


async def main():

    # Создаём SQLite базу и таблицы
    init_db()

    logging.info("Запуск бота...")

    bot = Bot(
        token=BOT_TOKEN
    )

    dp = Dispatcher()

    # /start
    dp.include_router(
        start_router
    )

    # Поддержка проекта
    dp.include_router(
        support_router
    )

    # Telegram Stars платежи
    dp.include_router(
        payments_router
    )

    # Главное меню и callback-кнопки
    dp.include_router(
        callbacks_router
    )

    # Настройки пользователя
    dp.include_router(
        settings_router
    )

    # История операций
    dp.include_router(
        history_router
    )

    # Дополнительные инструменты
    dp.include_router(
        extra_tools_router
    )

    # Игры
    dp.include_router(
        games_router
    )

    # Галерея
    dp.include_router(
        torture_router
    )

    # Сжатие файлов
    dp.include_router(
        compress_router
    )

    # JPG -> PNG
    # PNG -> JPG
    dp.include_router(
        image_router
    )

    # Видео -> MP3
    dp.include_router(
        video_converter_router
    )

    # Видео -> MP4 / MOV / AVI / WMV / WEBM
    dp.include_router(
        video_format_router
    )

    # Аудио ->
    # MP3 / WAV / FLAC / AAC / M4A / M4R / OGG
    dp.include_router(
        audio_converter_router
    )

    # Скачивание по ссылкам
    dp.include_router(
        downloader_router
    )

    logging.info(
        "Бот запущен и ожидает сообщения"
    )

    try:

        await dp.start_polling(
            bot
        )

    except Exception:

        logging.exception(
            "Критическая ошибка бота"
        )

    finally:

        await bot.session.close()

        logging.info(
            "Бот остановлен"
        )


if __name__ == "__main__":

    try:

        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        logging.info(
            "Бот остановлен пользователем"
        )
