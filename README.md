# Telegram-бот для карточек по правописанию гласных в корне

Небольшой Telegram-бот, который показывает карточки со словами с непроверяемыми безударными гласными в корне. В слове пропущена гласная, а внизу появляются кнопки с вариантами.

## Быстрый старт

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Экспортируйте токен бота:
   ```bash
   export TELEGRAM_BOT_TOKEN="<your_token>"
   ```
3. Запустите бота:
   ```bash
   python bot.py
   ```

## Команды

- `/start` — приветствие и подсказка по командам.
- `/card` — показать случайную карточку.
- `/next` — показать следующую карточку.
- `/help` — краткая справка.
- `/stats` — статистика ответов.
- `/menu` — главное меню.

Карточки хранятся в `data/cards.json` и легко расширяются (поля `gapped`, `answer`, `original`).

## Запуск на Linux VPS (systemd)

1. Установите системные зависимости и создайте директорию проекта:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv
   sudo mkdir -p /opt/telegram-spelling-bot
   sudo chown $USER:$USER /opt/telegram-spelling-bot
   ```
2. Скопируйте проект в `/opt/telegram-spelling-bot`, затем создайте виртуальное окружение:
   ```bash
   cd /opt/telegram-spelling-bot
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```
3. Скопируйте `deploy/telegram-spelling-bot.service` в `/etc/systemd/system/` и укажите токен:
   ```bash
   sudo cp deploy/telegram-spelling-bot.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable telegram-spelling-bot
   sudo systemctl start telegram-spelling-bot
   ```
4. Проверка статуса:
   ```bash
   sudo systemctl status telegram-spelling-bot
   ```
