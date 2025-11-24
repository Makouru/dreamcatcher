from telegram import ForceReply, Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os

from utilities.logger import log

class TelegramBot():

    def __init__(self):
        self.chat_id : int
        self.telegram_bot_token : str
        self.bot : Bot
        self.active : bool = False

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if self.active:
            await update.message.reply_text("the monitoring is already started!")
            return
        self.chat_id = update.effective_chat.id
        await update.message.reply_text("the monitoring has been started!")
        self.active = True

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.active:
            await update.message.reply_text("the monitoring is already stopped!")
            return
        await update.message.reply_text("the monitoring has been stopped!")
        self.active = False

    async def send_message(self, chat_id: int, text: str):
        await self.bot.send_message(chat_id=chat_id, text=text)

    async def initialize(self):

        self.telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.bot = Bot(token=self.telegram_bot_token)

        application = Application.builder().token(self.telegram_bot_token).build()

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("stop", self.stop))

        await application.initialize()
        await application.start()
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)

