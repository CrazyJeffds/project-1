from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.db import (
    get_settings,
    set_video_quality,
    set_audio_bitrate
)

from keyboards.settings_menu import (
    settings_menu,
    video_quality_menu,
    audio_bitrate_menu
)


router = Router()


# =========================================
# ОТКРЫТЬ НАСТРОЙКИ
# =========================================

@router.callback_query(F.data == "settings_menu")
async def open_settings(callback: CallbackQuery):

    settings = get_settings(
        callback.from_user.id
    )

    await callback.message.edit_text(
        "⚙️ <b>Настройки</b>\n\n"
        "Здесь можно настроить качество "
        "видео и аудио.",
        reply_markup=settings_menu(
            settings["video_quality"],
            settings["audio_bitrate"]
        ),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================
# МЕНЮ КАЧЕСТВА ВИДЕО
# =========================================

@router.callback_query(
    F.data == "settings_video_quality"
)
async def open_video_quality(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "🎬 <b>Качество видео</b>\n\n"
        "Выбери максимальное качество:",
        reply_markup=video_quality_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================
# ВЫБОР КАЧЕСТВА ВИДЕО
# =========================================

@router.callback_query(
    F.data.startswith("vq_")
)
async def select_video_quality(
    callback: CallbackQuery
):

    quality = callback.data.replace(
        "vq_",
        ""
    )

    allowed = [
        "360",
        "480",
        "720",
        "1080"
    ]

    if quality not in allowed:

        await callback.answer(
            "❌ Неверное качество",
            show_alert=True
        )

        return

    set_video_quality(
        callback.from_user.id,
        quality
    )

    settings = get_settings(
        callback.from_user.id
    )

    await callback.message.edit_text(
        "✅ <b>Настройка сохранена</b>\n\n"
        f"🎬 Качество видео: "
        f"<b>{quality}p</b>",
        reply_markup=settings_menu(
            settings["video_quality"],
            settings["audio_bitrate"]
        ),
        parse_mode="HTML"
    )

    await callback.answer(
        f"Установлено {quality}p"
    )


# =========================================
# МЕНЮ БИТРЕЙТА
# =========================================

@router.callback_query(
    F.data == "settings_audio_bitrate"
)
async def open_audio_bitrate(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "🎵 <b>Качество MP3</b>\n\n"
        "Выбери битрейт:",
        reply_markup=audio_bitrate_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================
# ВЫБОР БИТРЕЙТА
# =========================================

@router.callback_query(
    F.data.startswith("ab_")
)
async def select_audio_bitrate(
    callback: CallbackQuery
):

    bitrate = callback.data.replace(
        "ab_",
        ""
    )

    allowed = [
        "128",
        "192",
        "256",
        "320"
    ]

    if bitrate not in allowed:

        await callback.answer(
            "❌ Неверный битрейт",
            show_alert=True
        )

        return

    set_audio_bitrate(
        callback.from_user.id,
        bitrate
    )

    settings = get_settings(
        callback.from_user.id
    )

    await callback.message.edit_text(
        "✅ <b>Настройка сохранена</b>\n\n"
        f"🎵 MP3: "
        f"<b>{bitrate} kbps</b>",
        reply_markup=settings_menu(
            settings["video_quality"],
            settings["audio_bitrate"]
        ),
        parse_mode="HTML"
    )

    await callback.answer(
        f"Установлено {bitrate} kbps"
    )
