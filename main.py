from utils import *
from config import *

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function start's the intial conversation, 
    which leads to auth or exit
    """
    # Init user specific data when starting a new conversation 
    context.user_data["action"]: str = None
    context.user_data["user"]: User = None

    # Keyboard layout
    keyboard: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text = CONTENT["log_in"], callback_data = "auth")],
        [InlineKeyboardButton(text = CONTENT["log_out"], callback_data = "exit")],
    ]

    # Send the message
    await update.message.reply_text(text = CONTENT["greet"], reply_markup = InlineKeyboardMarkup(keyboard))




async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function end's the entire conversation
    """
    # Uninit user specific data when ending a conversation 
    context.user_data["action"]: str = None
    context.user_data["user"]: User = None

    # Check whether function call comes from callback handler or command handler
    if update.callback_query is not None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(CONTENT["goodbye"])
        return None
    
    await update.message.reply_text(CONTENT["goodbye"])
        



async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Auth start
    """
    context.user_data["action"]: str = "auth"

    # Check whether function call comes from callback handler or command handler
    if update.callback_query is not None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(CONTENT["auth"])
        return None
    
    await update.message.reply_text(CONTENT["auth"])




async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function return's a pretty menu for user interaction
    """
    context.user_data["action"] = None
    # If user is not logged in
    if context.user_data.get("user") == None:
        text: str = CONTENT["menu_unauth"]
        keyboard: list[list[InlineKeyboardButton]] = [
            [InlineKeyboardButton(text = CONTENT["log_in"], callback_data = "auth")],
            [InlineKeyboardButton(text = CONTENT["log_out"], callback_data = "exit")],
        ]
    else:
        # Menu layout for staff
        if context.user_data["user"].is_staff:
            text: str = CONTENT["menu_staff"].format(context.user_data["user"].username)
            keyboard: list[list[InlineKeyboardButton]] = [
                [InlineKeyboardButton(text = CONTENT["fresh_orders"], callback_data = "freshOrders"),],
                [InlineKeyboardButton(text = CONTENT["user_orders"], callback_data = "userOrders"), InlineKeyboardButton(text = CONTENT["all_orders"], callback_data = "allOrders" ),],
                [InlineKeyboardButton(text = CONTENT["log_out"], callback_data = "exit"),],
            ]
        # If layout for customer
        else:
            text: str = CONTENT["menu_customer"].format(context.user_data["user"].username)
            keyboard: list[list[InlineKeyboardButton]] = [
                [InlineKeyboardButton(text = CONTENT["personal_orders"], callback_data = "personalOrders"),],
                [InlineKeyboardButton(text = CONTENT["log_out"], callback_data = "exit"),],
            ]

    # Return menu
    # Check whether function call comes from callback handler or command handler       
    if update.callback_query is not None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text = text, parse_mode = "HTML")
        await update.callback_query.edit_message_reply_markup(reply_markup = InlineKeyboardMarkup(keyboard))
        return None   
     
    await update.message.reply_text(text = text, reply_markup = InlineKeyboardMarkup(keyboard), parse_mode = "HTML")




async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function cancels the current action
    """
    match context.user_data["action"]:
        case "input_username":
            await update.message.reply_text(CONTENT["cancel_input_username"])
            return await menu(context, update)
        case "auth":
            await update.message.reply_text(CONTENT["cancel_auth"])
            return await start(context, update)




async def handleCallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function handles all of the callback events (button presses)
    """
    # This is imperative, but idk why
    await update.callback_query.answer()

    keyboard = [[InlineKeyboardButton(text = CONTENT["menu_back"], callback_data = "menu")]]

    # Handle callback
    match update.callback_query.data:
        case "freshOrders":
            orders: str = getOrders(filter = {"fresh": True})
            text: str = f"{CONTENT['fresh_orders']}:\n{orders}"

        case "userOrders":
            context.user_data["action"]: str = "input_username"
            text: str = CONTENT["input_username"]
        
        case "allOrders":
            orders: str = getOrders(filter = {})
            text: str = f"{CONTENT['all_orders']}:\n{orders}"

        case "personalOrders":
            orders: str = getOrders(filter = {"user_id": context.user_data["user"].id})
            text: str = f"{CONTENT['personal_orders']}:\n{orders}"

        case "auth":
            if context.user_data.get("auth") == None:
                return await auth(update, context)
            await update.callback_query.edit_message_text(CONTENT["logged_in"])
            return None
        
        case "menu":
            return await menu(update, context)

        case "exit":
            return await stop(update, context)
    
    # Edit the message depending on callback
    await update.callback_query.edit_message_text(text = text, parse_mode = "HTML")
    await update.callback_query.edit_message_reply_markup(reply_markup = InlineKeyboardMarkup(keyboard))




async def handleMessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function handles user input and 
    depending on the action it'll do different stuff.
    """
    
    # What user typed 
    user_input: str = update.message.text.strip()

    # Which action is currently active
    match context.user_data.get("action"):

        # Getting orders for specific user
        case "input_username":
            orders: str = getOrders(filter = {"user_id": user_input})
            text: str = CONTENT["input_invalid_username"]
            keyboard = [[InlineKeyboardButton(text = CONTENT["menu_back"], callback_data = "menu")]]
            if orders:
                context.user_data["action"]: str = None
                text: str = f"{CONTENT['user_orders']} с id {user_input}:\n{orders}"

            await update.message.reply_text(text = text, parse_mode = "HTML", reply_markup = InlineKeyboardMarkup(keyboard))

        # Auth handling
        case "auth":
            credentials: list[str] = user_input.split("\n")
            user: User = getUser(credentials[0], credentials[1]) if (len(credentials) == 2) else None
            if not user:
                await context.bot.edit_message_text(text = CONTENT["invalid_auth"], message_id = update.message.id - 1, chat_id = update.message.chat_id)
                return await auth(update, context)
            
            context.user_data["user"]: User = user
            return await menu(update, context)
        



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"(!) WARNING  (!): Update {update} caused error {context.error}")



def main() -> None:
    # Create application
    app = Application.builder().token(TOKENS["TOKEN"]).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CommandHandler("exit", stop))

    # Callback and message handlers
    app.add_handler(CallbackQueryHandler(handleCallback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND , handleMessage))

    # Error warnings
    app.add_error_handler(error)

    # Start the bot
    app.run_polling(allowed_updates = Update.ALL_TYPES)




if __name__ == "__main__":
    main()