from aiogram.fsm.state import (
    State,
    StatesGroup
)


class ExtraStates(StatesGroup):

    waiting_for_qr_text = State()

    waiting_for_file_info = State()

    waiting_for_voice = State()

    waiting_for_video_note = State()

    waiting_for_sticker = State()
