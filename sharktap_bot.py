from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace with your BotFather token
TOKEN = "7615369637:AAGgWix8r3pE0ntiQyaLNnnW15P-Qa5h_eI"

# Game details
GAME_SHORT_NAME = "sharktap123"  # Use the final short name from BotFather
GAME_URL = "https://beatbid.store"  # Your actual game URL

# Send game when /start or /play is typed
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_game(chat_id=chat_id, game_short_name=GAME_SHORT_NAME)

# Handle the "Play" button click and provide the game URL
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await context.bot.answer_callback_query(callback_query_id=query.id, url=GAME_URL)

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    # Commands to start/play the game
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", start))

    # Callback for game play button
    app.add_handler(CallbackQueryHandler(handle_callback_query))

    print("🎮 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()



# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Application, CommandHandler

# # Replace this with your BotFather token
# TOKEN = "7615369637:AAGgWix8r3pE0ntiQyaLNnnW15P-Qa5h_eI"

# GAME_SHORT_NAME = "sharktap"  # your game short name registered with BotFather

# async def start(update, context):
#     chat_id = update.effective_chat.id
#     # Use send_game to send the game message
#     await context.bot.send_game(chat_id=chat_id, game_short_name=GAME_SHORT_NAME)

# if __name__ == "__main__":
#     app = Application.builder().token(TOKEN).build()
#     app.add_handler(CommandHandler("start", start))
#     print("Bot is running... Press Ctrl+C to stop.")
#     app.run_polling()





#old
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Application, CommandHandler

# # Replace this with your BotFather token
# TOKEN = "7615369637:AAGgWix8r3pE0ntiQyaLNnnW15P-Qa5h_eI"

# async def start(update, context):
#     keyboard = [
#         [InlineKeyboardButton("Play SharkTap 🦈", web_app={"url": "https://beatbid.store/"})]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("Tap to start the game!", reply_markup=reply_markup)

# if __name__ == "__main__":
#     app = Application.builder().token(TOKEN).build()
#     app.add_handler(CommandHandler("start", start))
#     print("Bot is running... Press Ctrl+C to stop.")
#     app.run_polling()
