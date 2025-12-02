import os
from utilities.logger import log
from telegram import ForceReply, Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

class TelegramBot():

    def __init__(self, database=None):
        self.db = database
        self.chat_id : int
        self.telegram_bot_token : str
        self.bot : Bot
        self.active : bool = False

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if self.active:
            await update.message.reply_text("notifications are already activated.")
            return
        self.chat_id = update.effective_chat.id
        await update.message.reply_text("notifications are now activated.")
        self.active = True

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.active:
            await update.message.reply_text("notifications are already deactivated.")
            return
        await update.message.reply_text("notifications are now deactivated.")
        self.active = False

    async def mute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        replied = update.message.reply_to_message
        if replied:
            ret = await self.db.save_message_to_muted(str(replied.text))
            if ret == -1:
                await update.message.reply_text("this notification is already muted.")
            else:
                await update.message.reply_text("this notification is now muted.")
        else:
            await update.message.reply_text("you need to reply to a notification.")

    async def clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        deleted_count = await self.db.clear_muted_collection()
        if deleted_count == 0:
            await update.message.reply_text("currently there are no notifications muted.")
        elif deleted_count == 1:
            await update.message.reply_text(f"{deleted_count} muted notification has been removed")
        else:
            await update.message.reply_text(f"{deleted_count} muted notifications have been removed")

    async def send_message(self, chat_id: int, text: str):
        await self.bot.send_message(chat_id=chat_id, text=text)

    async def initialize(self):

        self.telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.bot = Bot(token=self.telegram_bot_token)

        application = Application.builder().token(self.telegram_bot_token).build()

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("stop", self.stop))
        application.add_handler(CommandHandler("mute", self.mute))
        application.add_handler(CommandHandler("clear", self.clear))

        await application.initialize()
        await application.start()
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)

