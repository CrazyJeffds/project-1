import os
import uuid

from pathlib import Path

import yt_dlp

from database.db import get_settings


DOWNLOAD_ROOT = Path(
    "storage/downloads"
)


# ==================================================
# СОЗДАТЬ УНИКАЛЬНУЮ ПАПКУ
# ==================================================

def create_download_dir():

    DOWNLOAD_ROOT.mkdir(
        parents=True,
        exist_ok=True
    )

    download_id = uuid.uuid4().hex

    download_dir = (
        DOWNLOAD_ROOT
        / download_id
    )

    download_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return download_dir


# ==================================================
# ИНФОРМАЦИЯ О ССЫЛКЕ БЕЗ СКАЧИВАНИЯ
# ==================================================

def get_media_info(url):

    ydl_opts = {

        "quiet": True,

        "no_warnings": True,

        # Если ссылка содержит playlist,
        # качаем/смотрим только конкретное видео.
        "noplaylist": True,

        "skip_download": True
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

    # ==========================================
    # МАКСИМАЛЬНОЕ ДОСТУПНОЕ РАЗРЕШЕНИЕ
    # ==========================================

    heights = []

    for item in info.get(
        "formats",
        []
    ):

        height = item.get(
            "height"
        )

        if height:

            heights.append(
                height
            )

    max_height = None

    if heights:

        max_height = max(
            heights
        )

    return {

        "title": (
            info.get("title")
            or "Без названия"
        ),

        "uploader": (
            info.get("uploader")
            or info.get("channel")
            or "Неизвестно"
        ),

        "duration": (
            info.get("duration")
            or 0
        ),

        "max_height": max_height,

        "thumbnail": info.get(
            "thumbnail"
        ),

        "id": info.get(
            "id"
        ),

        "webpage_url": (
            info.get("webpage_url")
            or url
        )
    }


# ==================================================
# ПРОГРЕСС
# ==================================================

def create_progress_hook(
    progress_callback
):

    def progress_hook(data):

        if progress_callback is None:
            return

        status = data.get(
            "status"
        )

        if status == "downloading":

            downloaded = data.get(
                "downloaded_bytes",
                0
            )

            total = (
                data.get("total_bytes")
                or
                data.get(
                    "total_bytes_estimate"
                )
            )

            if total:

                percent = int(
                    downloaded
                    / total
                    * 100
                )

                try:

                    progress_callback(
                        percent
                    )

                except Exception:
                    pass

        elif status == "finished":

            try:

                progress_callback(
                    100
                )

            except Exception:
                pass

    return progress_hook


# ==================================================
# НАЙТИ ГОТОВЫЙ ФАЙЛ
# ==================================================

def find_result_file(
    download_dir,
    preferred_extensions=None
):

    if preferred_extensions is None:

        preferred_extensions = []

    files = []

    for file in download_dir.iterdir():

        if not file.is_file():
            continue

        if file.name.endswith(
            ".part"
        ):
            continue

        if file.name.endswith(
            ".ytdl"
        ):
            continue

        files.append(
            file
        )

    # Сначала ищем нужное расширение
    for extension in preferred_extensions:

        for file in files:

            if (
                file.suffix.lower()
                == f".{extension.lower()}"
            ):

                return str(
                    file
                )

    if files:

        # Обычно итоговый медиафайл
        # будет самым большим.
        files.sort(
            key=lambda item: (
                item.stat().st_size
            ),
            reverse=True
        )

        return str(
            files[0]
        )

    raise FileNotFoundError(
        "Итоговый файл не найден"
    )


# ==================================================
# СКАЧАТЬ ВИДЕО
# ==================================================

def download_youtube(
    url,
    progress_callback=None,
    user_id=None,
    quality=None
):

    download_dir = (
        create_download_dir()
    )

    # ==========================================
    # КАЧЕСТВО
    # ==========================================

    if quality is None:

        quality = "720"

        if user_id is not None:

            try:

                settings = get_settings(
                    user_id
                )

                quality = settings.get(
                    "video_quality",
                    "720"
                )

            except Exception:

                quality = "720"

    progress_hook = (
        create_progress_hook(
            progress_callback
        )
    )

    # ==========================================
    # АВТО
    # ==========================================

    if quality == "auto":

        format_string = (
            "bv*+ba/b"
        )

    else:

        format_string = (
            f"bv*[height<={quality}]"
            f"+ba/"
            f"b[height<={quality}]/"
            f"b"
        )

    ydl_opts = {

        "format": format_string,

        "merge_output_format": "mp4",

        "outtmpl": str(
            download_dir
            / "%(id)s.%(ext)s"
        ),

        "noplaylist": True,

        "restrictfilenames": True,

        "continuedl": False,

        "overwrites": True,

        "progress_hooks": [
            progress_hook
        ]
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        ydl.extract_info(
            url,
            download=True
        )

    return find_result_file(
        download_dir,
        preferred_extensions=[
            "mp4",
            "webm",
            "mkv"
        ]
    )


# ==================================================
# СКАЧАТЬ MP3
# ==================================================

def download_mp3(
    url,
    progress_callback=None,
    user_id=None
):

    download_dir = (
        create_download_dir()
    )

    # ==========================================
    # БИТРЕЙТ
    # ==========================================

    bitrate = "192"

    if user_id is not None:

        try:

            settings = get_settings(
                user_id
            )

            bitrate = settings.get(
                "audio_bitrate",
                "192"
            )

        except Exception:

            bitrate = "192"

    progress_hook = (
        create_progress_hook(
            progress_callback
        )
    )

    ydl_opts = {

        "format": "bestaudio/best",

        "outtmpl": str(
            download_dir
            / "%(id)s.%(ext)s"
        ),

        "noplaylist": True,

        "restrictfilenames": True,

        "continuedl": False,

        "overwrites": True,

        "progress_hooks": [
            progress_hook
        ],

        "postprocessors": [
            {
                "key": (
                    "FFmpegExtractAudio"
                ),

                "preferredcodec": (
                    "mp3"
                ),

                "preferredquality": (
                    bitrate
                )
            }
        ]
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        ydl.extract_info(
            url,
            download=True
        )

    return find_result_file(
        download_dir,
        preferred_extensions=[
            "mp3"
        ]
    )
