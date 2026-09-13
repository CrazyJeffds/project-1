# project-1
The work was done using ChatGPT—specifically, a Telegram bot for file conversion—and took over eight hours to complete.

Технологии

Проект использует:

Python 3
aiogram 3
yt-dlp
FFmpeg
Pillow
SQLite
qrcode
python-dotenv


git clone https://github.com/CrazyJeffds/project-1.git 

cd project-1

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt


nano .env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

python bot.py

# Telegram Media Tool Bot

Многофункциональный Telegram-бот для скачивания, конвертации и обработки медиафайлов.

Бот умеет работать с видео, аудио, изображениями, документами и ссылками на медиа.

---

## Возможности

### Скачивание медиа

- скачивание видео по ссылке
- выбор качества перед скачиванием:
  - 360p
  - 480p
  - 720p
  - 1080p
  - авто
- предпросмотр информации о ролике
- скачивание только аудио в MP3
- поддержка `yt-dlp`

---

### Видео

- видео → MP3
- конвертация видео:
  - MP4
  - MOV
  - AVI
  - WMV
  - WEBM
- сжатие видео

---

### Аудио

Поддерживается конвертация в:

- MP3
- WAV
- FLAC
- AAC
- M4A
- M4R
- OGG

Также можно выбрать битрейт MP3:

- 128 kbps
- 192 kbps
- 256 kbps
- 320 kbps

---

### Изображения

- JPG → PNG
- PNG → JPG
- сжатие изображений
- статический Telegram-стикер → PNG

---

### Дополнительные инструменты

- создание QR-кода
- информация о файле
- голосовое сообщение → MP3
- Telegram-кружок → MP4
- история операций
- пользовательские настройки

---

### Игры и дополнительные разделы

- мини-игра «Угадай число»
- галерея
- поддержка проекта через Telegram Stars

---

## Интерфейс

Бот оформлен в едином cyber/dark стиле.

Пример главного меню:

```text
◈ NEON TOOLS

━━━━━━━━━━━━━━━━━━
⚡ МЕДИА И ФАЙЛОВЫЕ ИНСТРУМЕНТЫ
━━━━━━━━━━━━━━━━━━

📥 СКАЧАТЬ

🎬 ВИДЕО        🎵 АУДИО
🖼 ИЗОБРАЖЕНИЯ  📄 ДОКУМЕНТЫ
🧰 ИНСТРУМЕНТЫ 🗜 СЖАТИЕ
⚙️ НАСТРОЙКИ   🕘 ИСТОРИЯ
🎮 ИГРЫ         🩸 ГАЛЕРЕЯ
❤️ ПОДДЕРЖАТЬ ПРОЕКТ





