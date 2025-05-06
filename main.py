import os
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = 8024354255:AAGQ-o2bmrYlrmVF3-Bdh4wk1GrfrIhpmGM  # Задай TOKEN через переменную окружения

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Отправка изображения
    try:
        with open("welcome.jpg", "rb") as photo:
            caption = f"🌟 Добро пожаловать, {user.first_name}!\n\nТы можешь поддержать нас переводом на USDT."
            await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
    except FileNotFoundError:
        await context.bot.send_message(chat_id=chat_id, text="👋 Добро пожаловать! (Изображение не найдено)")

    # Анимация кнопки "Начать"
    loading_frames = ["🌑", "🌓", "🌔", "🌕", "🌝", "🌞", "🚀"]
    msg = await context.bot.send_message(chat_id=chat_id, text="⏳ Подготовка кнопки...")

    for frame in loading_frames:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{frame} Начать", callback_data="start_clicked")]
        ])
        await msg.edit_reply_markup(reply_markup=keyboard)
        await asyncio.sleep(0.4)

    final_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Начать", callback_data="start_clicked")]
    ])
    await msg.edit_text("👇 Готово!", reply_markup=final_keyboard)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    user = query.from_user

    if query.data == "start_clicked":
        await context.bot.send_message(chat_id=chat_id, text="⏳ Подготовка адреса USDT...")
        await asyncio.sleep(2)

        ton_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💵 Узнать адрес USDT", callback_data="get_ton")]
        ])
        await context.bot.send_message(chat_id=chat_id, text="Готово! Нажми кнопку ниже:", reply_markup=ton_keyboard)

    elif query.data == "get_ton":
        ton_address = "EQC1234567890TONaddress..."  # ← ВСТАВЬ СВОЙ TON-АДРЕС
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"💵 Адрес USDT:\n`{ton_address}`",
            parse_mode="Markdown"
        )

# Удаление всех сообщений (кроме команд и кнопок)
async def block_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
    except:
        pass

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, block_messages))
    app.run_polling()
