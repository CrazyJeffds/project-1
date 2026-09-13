from aiogram.fsm.state import State, StatesGroup


class ConverterStates(StatesGroup):

    waiting_for_image_compress = State()

    waiting_for_video_mp3 = State()

    waiting_for_pdf = State()

    waiting_for_jpg = State()

    waiting_for_png = State()

    waiting_for_video_compress = State()
