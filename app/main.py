from fastapi import FastAPI, Request
import os
import asyncio

from utilities.logger import log
from utilities.bot import TelegramBot
from utilities.db import Database

app = FastAPI()
db = Database()
bot = TelegramBot(database=db)

STORE_WEBHOOKS_TO_DATABASE = os.environ.get("STORE_WEBHOOKS_TO_DATABASE")

@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    msg = data["message"]

    if STORE_WEBHOOKS_TO_DATABASE.lower() == 'true':
        await db.save_webhook_payload(data)

    if bot.active:
        if not await db.message_is_muted(msg):
            await bot.send_message(bot.chat_id, msg)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.initialize())
    await db.connect()

