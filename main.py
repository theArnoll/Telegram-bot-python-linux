from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, Defaults
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
    wake(os.getenv("WoLmac"), host=os.getenv("WoLIP"), port=9)
    await update.message.reply_text(f'Magic package sent\\!')

@restricted
async def restartBot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"The bot is restarting\\.\\.\\.")
    exit()

app = ApplicationBuilder().token(os.getenv("botToken")).defaults(Defaults(parse_mode=ParseMode.MARKDOWN_V2)).post_init(onStart).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("wake", wol))
app.add_handler(CommandHandler("restartBot", restartBot))
# app.add_handler(CommandHandler(filters.TEXT & (~filters.COMMAND), hello))
app.run_polling()