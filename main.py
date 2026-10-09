from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, Defaults, CallbackQueryHandler
import os
from dotenv import load_dotenv
from functools import wraps
import json
from wakeonlan import wake
from telegram.constants import ParseMode

load_dotenv()

raw_allowed = os.getenv("userID", "[]")
try:
    allowedUser = set(json.loads(raw_allowed))
except json.JSONDecodeError:
    allowedUser = {
        int(uid.strip())
        for uid in raw_allowed.replace("[", "").replace("]", "").split(",")
        if uid.strip().isdigit()
    }  # from Google AI Studio Gemini
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#restrict-access-to-a-handler-decorator from https://stackoverflow.com/a/62530345
def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in allowedUser:
            print(f"Unauthorized access denied for {user_id}.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

async def onStart(application: Application) -> None:
    for id in allowedUser:
        try:
            chat = await application.bot.get_chat(id)
            user_name = chat.first_name or "Master"

            await application.bot.send_message(
                chat_id=id,
                text=f"✨ *B*lack*b*ox *B*ot at your service ✨",
                # parse_mode=ParseMode.MARKDOWN,
            )
            # print(f"Startup message sent to {id} ({user_name})")
            print(f"Startup message sent to {user_name}")
        except Exception as e:
            print(
                f"Unable to send startup message to {id}: {e}\n"
                "The user may have blocked the bot or never pressed /start"
            )

@restricted
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}, *B*lack*b*ox *B*ot at your service ✨")

@restricted
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Pong!')

@restricted  # /wake
async def wol(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # send_magic_packet(os.getenv("WoLmac"), ip_address=os.getenv("WoLIP"), port=9) # Deprecated
    wake(os.getenv("WoLmac"), host=os.getenv("WoLIP"), port=9, interface=os.getenv("WoLIP"))
    await update.message.reply_text(f'Magic package sent!')

@restricted
async def restartBot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"The bot is restarting...")
    exit()

# Gemini from Google AI Studio generated start
@restricted
async def server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "Please provide an argument: `/server shutdown` or `/server reboot`",
            parse_mode="Markdown",
        )
        return
    action = context.args[0].lower()

    if action == "shutdown":
        text = (
            "⚠️ **WARNING: The server is about to POWER OFF.**\n"
            "You will NOT be able to access any functions of this bot, including the `/wake` command, "
            "until the server is booted manually.\n\n"
            "Are you sure you want to proceed?"
        )
        callback_action = "server_shutdown"
    elif action in ["reboot", "restart"]:
        text = (
            "⚠️ **WARNING: The server is about to RESTART/REBOOT.**\n"
            "The bot will be temporarily unavailable until the system finishes rebooting.\n\n"
            "Are you sure you want to proceed?"
        )
        callback_action = "server_reboot"
    else:
        await update.message.reply_text(
            "Invalid argument. Please use `shutdown` or `reboot`.",
            parse_mode="Markdown",
        )
        return

    keyboard = [
        [
            InlineKeyboardButton("Cancel", callback_data="cancel_server_action"),
            InlineKeyboardButton("Confirm", callback_data=f"confirm_{callback_action}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text, reply_markup=reply_markup, parse_mode="Markdown"
    )


@restricted
async def server_button_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    # Processing button click
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "cancel_server_action":
        await query.edit_message_text("Operation canceled.")
        return

    if data == "confirm_server_shutdown":
        await query.edit_message_text("Shutting down the server...")
        os.system("sudo shutdown now")

    elif data == "confirm_server_reboot":
        await query.edit_message_text("Rebooting the server...")
        os.system("sudo reboot")

@restricted
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Available commands:\n"
        "/hello - Greet the bot.\n"
        "/ping - Check if the bot is online.\n"
        "/wake - Wake the computer/device using Wake-on-LAN.\n"
        "/restartBot - Restart the bot.\n"
        "/server <functions> - Server management functions.\n"
        "        shutdown - Shutdown the server.\n"
        "        reboot - Reboot the server.\n"
        "        restart - Alias for reboot.\n"
        "        Aliases: /svr, /srv\n"
    )
    await update.message.reply_text(help_text)
# Gemini from Google AI Studio generated end

# app = ApplicationBuilder().token(os.getenv("botToken")).defaults(Defaults(parse_mode=ParseMode.MARKDOWN_V2)).post_init(onStart).build()
app = ApplicationBuilder().token(os.getenv("botToken")).defaults(Defaults(parse_mode=ParseMode.MARKDOWN)).post_init(onStart).build()

# shutdown / reboot confirmation buttons handler. Generated with Gemini from Google AI Studio.
app.add_handler(
    CallbackQueryHandler(
        server_button_callback, pattern=r"^(confirm_server_|cancel_server_action)"
    )
)
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("wake", wol))
app.add_handler(CommandHandler("restartBot", restartBot))
app.add_handler(CommandHandler("server", server))
app.add_handler(CommandHandler("svr", server))
app.add_handler(CommandHandler("srv", server))
app.add_handler(CommandHandler("help", help))
app.run_polling()
