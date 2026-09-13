# project-1
The work was done using ChatGPT—specifically, a Telegram bot for file conversion—and took over eight hours to complete.
# ⚡ Telegram Media Tool Bot

<p align="center">
  <b>Многофункциональный Telegram-бот для скачивания, конвертации и обработки медиафайлов</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram" alt="aiogram">
  <img src="https://img.shields.io/badge/FFmpeg-enabled-black?style=for-the-badge&logo=ffmpeg" alt="FFmpeg">
  <img src="https://img.shields.io/badge/yt--dlp-enabled-red?style=for-the-badge" alt="yt-dlp">
</p>

---

## 🧩 О проекте

**Telegram Media Tool Bot** — универсальный Telegram-бот для работы с медиа и файлами прямо внутри Telegram.

Бот умеет:

- 📥 скачивать видео и аудио по ссылкам;
- 🎬 конвертировать видео в разные форматы;
- 🎵 конвертировать аудио;
- 🖼 работать с изображениями;
- 🗜 сжимать видео и изображения;
- 🔳 создавать QR-коды;
- 🎤 преобразовывать голосовые сообщения в MP3;
- ⭕ сохранять видеокружки в MP4;
- 🏷 конвертировать статические стикеры в PNG;
- 🕘 хранить историю операций;
- ⚙️ сохранять пользовательские настройки;
- ⭐ принимать поддержку через Telegram Stars.

---

## 🌑 Интерфейс

Бот оформлен в едином тёмном / cyber-style интерфейсе.

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
```

---

## 🚀 Возможности

### 📥 Скачивание медиа

- предпросмотр ссылки перед скачиванием;
- отображение названия ролика;
- отображение автора;
- отображение длительности;
- определение максимального качества;
- выбор между видео и MP3;
- выбор качества: 360p / 480p / 720p / 1080p / авто;
- отображение прогресса скачивания;
- автоматическая очистка временных файлов.

### 🎬 Видео

- видео → MP3;
- MP4;
- MOV;
- AVI;
- WMV;
- WEBM;
- сжатие видео.

### 🎵 Аудио

Поддерживаемые форматы:

- MP3;
- WAV;
- FLAC;
- AAC;
- M4A;
- M4R;
- OGG.

Поддерживаемый битрейт MP3:

- 128 kbps;
- 192 kbps;
- 256 kbps;
- 320 kbps.

### 🖼 Изображения

- JPG → PNG;
- PNG → JPG;
- сжатие изображений;
- статический Telegram-стикер → PNG.

### 🧰 Дополнительные инструменты

- генератор QR-кодов;
- информация о файле;
- голосовое сообщение → MP3;
- Telegram-видеокружок → MP4;
- история операций;
- пользовательские настройки.

---

## 🛠 Используемые технологии

| Технология | Назначение |
|---|---|
| **Python 3** | основной язык проекта |
| **aiogram 3** | Telegram Bot API |
| **yt-dlp** | скачивание медиа |
| **FFmpeg** | обработка видео и аудио |
| **Pillow** | обработка изображений |
| **SQLite** | настройки и история |
| **qrcode** | создание QR-кодов |
| **python-dotenv** | переменные окружения |

---

# 🚀 Установка и запуск

## 1. 📥 Клонировать репозиторий

```bash
git clone https://github.com/CrazyJeffds/project-1.git
```

---

## 2. 📂 Перейти в папку проекта

```bash
cd project-1
```

---

## 3. 🐍 Создать виртуальное окружение

```bash
python3 -m venv venv
```

---

## 4. ⚡ Активировать виртуальное окружение

### Linux / Kali Linux

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

---

## 5. 📦 Установить зависимости

```bash
pip install -r requirements.txt
```

---

## 6. 🎬 Установить FFmpeg

### Kali Linux / Debian / Ubuntu

```bash
sudo apt update
sudo apt install ffmpeg
```

Проверить установку:

```bash
ffmpeg -version
```

---

## 7. 🔐 Создать файл `.env`

```bash
nano .env
```

Добавить внутрь:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

Токен Telegram-бота можно получить через `@BotFather`.

> ⚠️ Никогда не публикуй настоящий `BOT_TOKEN` в GitHub.

---

## 8. ▶️ Запустить бота

```bash
python bot.py
```

При успешном запуске:

```text
Запуск бота...
Бот запущен и ожидает сообщения
```

---

## 📁 Структура проекта

```text
telegram_converter_bot/
├── bot.py
├── config.py
├── requirements.txt
├── handlers/
├── keyboards/
├── services/
├── states/
├── database/
├── storage/
├── utils/
└── assets/
```

---

## 🗄 База данных

Проект использует **SQLite**.

Файл базы создаётся автоматически:

```text
database/bot.db
```

В базе хранятся настройки пользователей и история операций.

---

## ⭐ Telegram Stars

В боте реализована добровольная поддержка проекта через Telegram Stars.

Доступные суммы:

```text
⭐ 25
⭐ 50
⭐ 100
⭐ 250
⭐ 500
```

---

## 🔒 Безопасность

В репозиторий не должны попадать:

```text
.env
BOT_TOKEN
database/bot.db
venv/
storage/downloads/
storage/uploads/
storage/converted/
```

---

## 🧪 Статус проекта

Проект рабочий и продолжает развиваться.

Планируемые функции:

- ✂️ обрезка видео;
- ✂️ обрезка аудио;
- 🎞 GIF ↔ MP4;
- 📄 несколько изображений → PDF;
- 📦 ZIP нескольких файлов;
- 📐 изменение размера изображений;
- 🧹 удаление метаданных;
- 📊 админ-панель и статистика;
- 🚦 очередь задач.

---

## 🔄 Обновление проекта

После изменений:

```bash
git add .
git commit -m "Описание изменений"
git push
```

---

## 👤 Автор

GitHub: **CrazyJeffds**

---

## ⭐ Поддержка проекта

Если проект оказался полезным — поставь ⭐ репозиторию.



