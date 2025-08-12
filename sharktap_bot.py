from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler

# Replace this with your BotFather token
TOKEN = "7615369637:AAGgWix8r3pE0ntiQyaLNnnW15P-Qa5h_eI"

GAME_SHORT_NAME = "sharktap"  # your game short name registered with BotFather

async def start(update, context):
    chat_id = update.effective_chat.id
    # Use send_game to send the game message
    await context.bot.send_game(chat_id=chat_id, game_short_name=GAME_SHORT_NAME)

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()





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
