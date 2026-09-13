from aiogram.fsm.state import State, StatesGroup


class ConverterStates(StatesGroup):

    # Изображения
    waiting_for_image_compress = State()
    waiting_for_jpg = State()
    waiting_for_png = State()

    # Видео
    waiting_for_video_mp3 = State()
    waiting_for_video_compress = State()
    waiting_for_video_convert = State()

    # Аудио
    waiting_for_audio_convert = State()

    # Документы
    waiting_for_pdf = State()
