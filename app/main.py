from fastapi import FastAPI, Request
import asyncio

from utilities.logger import log
from utilities.bot import TelegramBot

app = FastAPI()
bot = TelegramBot()

@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    msg = data["message"]

    if bot.active:
        await bot.send_message(bot.chat_id, msg)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.initialize())

