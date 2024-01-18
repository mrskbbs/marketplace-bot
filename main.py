from typing import Final
from .utils import *

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Fetches token and bot's name
t = fetchToken()
TOKEN: Final = t[0]
NAME: Final = t[1]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello my nigga!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a help comand")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")

def handle_responce(message: str) -> str:
    match message:
        case "Hello":
            return "WAZZUP!!!"
        case "test":
            return "sdfsdfssdf"
        case _:
            return "No responce"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == "group":
        if NAME in text:
            responce: str = handle_responce(text.replace(NAME, "").strip())
        else: 
            return
    else:
        responce: str = handle_responce(text)

    await update.message.reply_text(responce)
         
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"(!) WARNING: Update {update} caused error {context.error} (!)")

def main() -> None:
    print(f"BOT: {NAME} | {TOKEN} is running...")

    # Create application
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Error handling
    app.add_error_handler(error)

    
    print("Polling...")
    app.run_polling(poll_interval=5)

if __name__ == "__main__":
    main()