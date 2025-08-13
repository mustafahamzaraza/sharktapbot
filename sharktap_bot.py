from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import asyncio
import os


# === CONFIGURATION ===
TOKEN = "7615369637:AAGgWix8r3pE0ntiQyaLNnnW15P-Qa5h_eI"
WEBHOOK_URL = "https://sharktapbot.onrender.com"  # Your Render app URL
GAME_SHORT_NAME = "sharktap123"
GAME_URL = "https://beatbid.store"

# === FLASK APP ===
app = Flask(__name__)

# === TELEGRAM BOT APP ===
telegram_app = Application.builder().token(TOKEN).build()






# === BOT COMMANDS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send the game when user types /start or /play"""
    chat_id = update.effective_chat.id
    await context.bot.send_game(chat_id=chat_id, game_short_name=GAME_SHORT_NAME)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the Play button click and open the game URL"""
    query = update.callback_query
    await context.bot.answer_callback_query(callback_query_id=query.id, url=GAME_URL)

async def set_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manually set a score for the user (test command)"""
    try:
        score = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Please provide a valid score: /setscore 100")
        return

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    try:
        await context.bot.set_game_score(
            user_id=user_id,
            score=score,
            chat_id=chat_id,
            force=True,
            game_short_name=GAME_SHORT_NAME
        )
        await update.message.reply_text(f"✅ Score of {score} saved for you!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to set score: {e}")

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if webhook is receiving updates"""
    user = update.effective_user
    chat = update.effective_chat
    await update.message.reply_text(
        f"✅ Webhook is working!\n"
        f"👤 User ID: {user.id}\n"
        f"💬 Chat ID: {chat.id}\n"
        f"Username: @{user.username if user.username else 'No username'}"
    )


# === FLASK ROUTES ===
@app.route("/", methods=["GET"])
def home():
    return "SharkTapBot is running!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Receive updates from Telegram and process them asynchronously"""
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.run_coroutine_threadsafe(telegram_app.process_update(update), telegram_app.loop)
    return "ok"

# === SET WEBHOOK ===
def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
    resp = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}")
    if resp.status_code == 200:
        print(f"✅ Webhook set to {webhook_url}")
    else:
        print(f"❌ Failed to set webhook: {resp.text}")

# === MAIN ENTRYPOINT ===
if __name__ == "__main__":
    telegram_app = Application.builder().token(TOKEN).build()

    # Add all handlers here
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("play", start))
    telegram_app.add_handler(CommandHandler("setscore", set_score))
    telegram_app.add_handler(CommandHandler("debug", debug))
    telegram_app.add_handler(CallbackQueryHandler(handle_callback_query))

    # Set webhook for server mode
    set_webhook()

    # Run bot
    if os.environ.get("RUN_LOCAL"):
        telegram_app.run_polling()
    else:
        app.run(host="0.0.0.0", port=5000)








# from flask import Flask, request
# from telegram import Update
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
# import requests

# # === CONFIGURATION ===
# TOKEN = "7615369637:AAGgWix8r3pE0ntiQyaLNnnW15P-Qa5h_eI"
# WEBHOOK_URL = "https://sharktapbot.onrender.com"  # Replace with your actual Render app URL
# GAME_SHORT_NAME = "sharktap123"
# GAME_URL = "https://beatbid.store"

# # === FLASK APP ===
# app = Flask(__name__)

# # === TELEGRAM BOT APP ===
# telegram_app = Application.builder().token(TOKEN).build()

# # /start or /play command
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     await context.bot.send_game(chat_id=chat_id, game_short_name=GAME_SHORT_NAME)

# # Handle the "Play" button click
# async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await context.bot.answer_callback_query(callback_query_id=query.id, url=GAME_URL)

# # /setscore command
# async def set_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         score = int(context.args[0])
#     except (IndexError, ValueError):
#         await update.message.reply_text("Please provide a valid score: /setscore 100")
#         return

#     user_id = update.effective_user.id
#     chat_id = update.effective_chat.id

#     try:
#         await context.bot.set_game_score(
#             user_id=user_id,
#             score=score,
#             chat_id=chat_id,
#             force=True,
#             game_short_name=GAME_SHORT_NAME
#         )
#         await update.message.reply_text(f"Score of {score} saved for you!")
#     except Exception as e:
#         await update.message.reply_text(f"Failed to set score: {e}")

# # === REGISTER HANDLERS ===
# telegram_app.add_handler(CommandHandler("start", start))
# telegram_app.add_handler(CommandHandler("play", start))
# telegram_app.add_handler(CommandHandler("setscore", set_score))
# telegram_app.add_handler(CallbackQueryHandler(handle_callback_query))

# # === FLASK ROUTES ===
# @app.route(f"/{TOKEN}", methods=["POST"])
# def webhook():
#     update = Update.de_json(request.get_json(force=True), telegram_app.bot)
#     telegram_app.update_queue.put_nowait(update)
#     return "ok"

# # === SET WEBHOOK ===
# def set_webhook():
#     webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
#     resp = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}")
#     if resp.status_code == 200:
#         print(f"✅ Webhook set to {webhook_url}")
#     else:
#         print(f"❌ Failed to set webhook: {resp.text}")

# # === MAIN ENTRYPOINT ===
# if __name__ == "__main__":
#     set_webhook()
#     app.run(host="0.0.0.0", port=5000)









# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# # Replace with your BotFather token
# TOKEN = "7615369637:AAGgWix8r3pE0ntiQyaLNnnW15P-Qa5h_eI"

# # Game details
# GAME_SHORT_NAME = "sharktap123"  # Use the final short name from BotFather
# GAME_URL = "https://beatbid.store"  # Your actual game URL

# # Send game when /start or /play is typed
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     await context.bot.send_game(chat_id=chat_id, game_short_name=GAME_SHORT_NAME)

# # Handle the "Play" button click and provide the game URL
# async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     # Answer callback by opening the game URL
#     await context.bot.answer_callback_query(callback_query_id=query.id, url=GAME_URL)

# # New command to set score for the user
# # Usage: /setscore <score>
# async def set_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         score = int(context.args[0])  # get score from command argument
#     except (IndexError, ValueError):
#         await update.message.reply_text("Please provide a valid score: /setscore 100")
#         return

#     user_id = update.effective_user.id
#     chat_id = update.effective_chat.id

#     # Call Telegram API to set game score
#     # Using context.bot.set_game_score convenience method
#     try:
#         await context.bot.set_game_score(
#             user_id=user_id,
#             score=score,
#             chat_id=chat_id,
#             force=True,
#             game_short_name=GAME_SHORT_NAME
#         )
#         await update.message.reply_text(f"Score of {score} saved for you!")
#     except Exception as e:
#         await update.message.reply_text(f"Failed to set score: {e}")

# if __name__ == "__main__":
#     app = Application.builder().token(TOKEN).build()

#     # Commands to start/play the game
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("play", start))

#     # Command to set score (test purpose)
#     app.add_handler(CommandHandler("setscore", set_score))

#     # Callback for game play button
#     app.add_handler(CallbackQueryHandler(handle_callback_query))

#     print("🎮 Bot is running... Press Ctrl+C to stop.")
#     app.run_polling()



# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# # Replace with your BotFather token
# TOKEN = "7615369637:AAGgWix8r3pE0ntiQyaLNnnW15P-Qa5h_eI"

# # Game details
# GAME_SHORT_NAME = "sharktap123"  # Use the final short name from BotFather
# GAME_URL = "https://beatbid.store"  # Your actual game URL

# # Send game when /start or /play is typed
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     await context.bot.send_game(chat_id=chat_id, game_short_name=GAME_SHORT_NAME)

# # Handle the "Play" button click and provide the game URL
# async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await context.bot.answer_callback_query(callback_query_id=query.id, url=GAME_URL)

# if __name__ == "__main__":
#     app = Application.builder().token(TOKEN).build()

#     # Commands to start/play the game
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("play", start))

#     # Callback for game play button
#     app.add_handler(CallbackQueryHandler(handle_callback_query))

#     print("🎮 Bot is running... Press Ctrl+C to stop.")
#     app.run_polling()



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
