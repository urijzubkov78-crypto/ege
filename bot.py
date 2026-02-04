import json
import os
import random
from pathlib import Path

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

DATA_PATH = Path(__file__).parent / "data" / "cards.json"
VOWEL_OPTIONS = ["а", "е", "ё", "и", "о", "у", "ы", "э", "ю", "я"]
VOWEL_SET = set(VOWEL_OPTIONS)


def load_cards() -> list[dict[str, str]]:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        cards = json.load(handle)
    validate_cards(cards)
    return cards


def validate_cards(cards: list[dict[str, str]]) -> None:
    for idx, card in enumerate(cards):
        gapped = card.get("gapped", "")
        answer = card.get("answer", "")
        original = card.get("original", "")
        if gapped.count("...") != 1:
            raise ValueError(f"Card {idx} has invalid gap: {gapped}")
        if answer not in VOWEL_SET:
            raise ValueError(f"Card {idx} has invalid answer: {answer}")
        if gapped.replace("...", answer, 1) != original:
            raise ValueError(
                f"Card {idx} mismatch: {gapped} + {answer} != {original}"
            )


def format_card(card: dict[str, str]) -> str:
    return (
        f"<b>Слово:</b> {card['gapped']}\n"
        "<b>Задание:</b> выбери нужную гласную."
    )


def build_vowel_keyboard() -> InlineKeyboardMarkup:
    rows = [VOWEL_OPTIONS[:5], VOWEL_OPTIONS[5:]]
    keyboard = [
        [InlineKeyboardButton(vowel, callback_data=vowel) for vowel in row]
        for row in rows
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Привет! Я показываю карточки со словами с непроверяемыми "
        "безударными гласными в корне.\n\n"
        "Команды:\n"
        "/card — случайная карточка\n"
        "/next — следующая карточка\n"
        "/help — справка\n"
        "/stats — статистика"
    )
    await update.effective_message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "Используйте /card или /next, чтобы получить новую карточку. "
        "Нажмите на кнопку с гласной, чтобы проверить ответ. "
        "Команда /stats покажет статистику."
    )


async def send_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cards = context.application.bot_data.setdefault("cards", load_cards())
    if not cards:
        await update.effective_message.reply_text("Нет карточек для отображения.")
        return
    order = context.user_data.get("order")
    position = context.user_data.get("position", 0)

    if not order or position >= len(order):
        order = list(range(len(cards)))
        random.shuffle(order)
        position = 0

    index = order[position]
    context.user_data["order"] = order
    context.user_data["position"] = position + 1
    card = cards[index]
    context.user_data["current_card"] = card
    await update.effective_message.reply_text(
        format_card(card),
        parse_mode=ParseMode.HTML,
        reply_markup=build_vowel_keyboard(),
    )


async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer()
    card = context.user_data.get("current_card")
    if not card:
        await query.message.reply_text("Сначала запросите карточку через /card.")
        return

    selected = query.data
    correct = card["answer"]
    stats = context.user_data.setdefault(
        "stats", {"total": 0, "correct": 0, "incorrect": 0}
    )
    stats["total"] += 1
    if selected == correct:
        stats["correct"] += 1
        response = f"✅ Верно! Слово: <b>{card['original']}</b>."
    else:
        stats["incorrect"] += 1
        response = (
            "❌ Неверно. "
            f"Правильный вариант: <b>{card['original']}</b> "
            f"(гласная «{correct}»)."
        )
    await query.message.reply_text(response, parse_mode=ParseMode.HTML)


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    stats = context.user_data.get("stats", {"total": 0, "correct": 0, "incorrect": 0})
    message = (
        "<b>Статистика</b>\n"
        f"Всего ответов: {stats['total']}\n"
        f"Верных: {stats['correct']}\n"
        f"Неверных: {stats['incorrect']}"
    )
    await update.effective_message.reply_text(message, parse_mode=ParseMode.HTML)


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("card", send_card))
    application.add_handler(CommandHandler("next", send_card))
    application.add_handler(CommandHandler("stats", show_stats))
    application.add_handler(CallbackQueryHandler(check_answer))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
