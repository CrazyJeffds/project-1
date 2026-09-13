import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = Path("database/bot.db")


def get_connection():
    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_PATH
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # =========================================
    # ПОЛЬЗОВАТЕЛИ
    # =========================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    # =========================================
    # НАСТРОЙКИ
    # =========================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER PRIMARY KEY,

            video_quality TEXT
            NOT NULL
            DEFAULT '720',

            audio_bitrate TEXT
            NOT NULL
            DEFAULT '192',

            language TEXT
            NOT NULL
            DEFAULT 'ru',

            FOREIGN KEY(user_id)
            REFERENCES users(user_id)
        )
        """
    )

    # =========================================
    # ИСТОРИЯ
    # =========================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            action TEXT NOT NULL,

            source_format TEXT,

            target_format TEXT,

            size_before REAL,

            size_after REAL,

            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


# =========================================
# ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ
# =========================================

def ensure_user(
    user_id,
    username=None,
    first_name=None
):

    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.now().isoformat(
        timespec="seconds"
    )

    cursor.execute(
        """
        INSERT INTO users (
            user_id,
            username,
            first_name,
            created_at
        )
        VALUES (?, ?, ?, ?)

        ON CONFLICT(user_id)
        DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name
        """,
        (
            user_id,
            username,
            first_name,
            created_at
        )
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO settings (
            user_id
        )
        VALUES (?)
        """,
        (
            user_id,
        )
    )

    conn.commit()
    conn.close()


# =========================================
# ПОЛУЧИТЬ НАСТРОЙКИ
# =========================================

def get_settings(user_id):

    ensure_user(
        user_id
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            video_quality,
            audio_bitrate,
            language

        FROM settings

        WHERE user_id = ?
        """,
        (
            user_id,
        )
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:

        return {
            "video_quality": "720",
            "audio_bitrate": "192",
            "language": "ru"
        }

    return dict(
        row
    )


# =========================================
# ИЗМЕНИТЬ КАЧЕСТВО ВИДЕО
# =========================================

def set_video_quality(
    user_id,
    quality
):

    ensure_user(
        user_id
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE settings

        SET video_quality = ?

        WHERE user_id = ?
        """,
        (
            quality,
            user_id
        )
    )

    conn.commit()
    conn.close()


# =========================================
# ИЗМЕНИТЬ БИТРЕЙТ АУДИО
# =========================================

def set_audio_bitrate(
    user_id,
    bitrate
):

    ensure_user(
        user_id
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE settings

        SET audio_bitrate = ?

        WHERE user_id = ?
        """,
        (
            bitrate,
            user_id
        )
    )

    conn.commit()
    conn.close()


# =========================================
# ДОБАВИТЬ В ИСТОРИЮ
# =========================================

def add_history(
    user_id,
    action,
    source_format=None,
    target_format=None,
    size_before=None,
    size_after=None
):

    ensure_user(
        user_id
    )

    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.now().isoformat(
        timespec="seconds"
    )

    cursor.execute(
        """
        INSERT INTO history (
            user_id,
            action,
            source_format,
            target_format,
            size_before,
            size_after,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            action,
            source_format,
            target_format,
            size_before,
            size_after,
            created_at
        )
    )

    conn.commit()
    conn.close()


# =========================================
# ПОЛУЧИТЬ ИСТОРИЮ
# =========================================

def get_history(
    user_id,
    limit=10
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            action,
            source_format,
            target_format,
            size_before,
            size_after,
            created_at

        FROM history

        WHERE user_id = ?

        ORDER BY id DESC

        LIMIT ?
        """,
        (
            user_id,
            limit
        )
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


# =========================================
# СТАТИСТИКА
# =========================================

def get_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        AS count
        FROM users
        """
    )

    users_count = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*)
        AS count
        FROM history
        """
    )

    operations_count = cursor.fetchone()["count"]

    conn.close()

    return {
        "users": users_count,
        "operations": operations_count
    }
