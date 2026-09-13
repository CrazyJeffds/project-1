from aiogram.fsm.state import (
    State,
    StatesGroup
)


class DownloaderStates(StatesGroup):

    # Получили ссылку и ждём:
    # Видео или MP3
    waiting_for_type = State()

    # Пользователь выбрал видео
    # и теперь выбирает качество
    waiting_for_quality = State()
