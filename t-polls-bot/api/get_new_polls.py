import requests
import asyncio
from aiogram import Bot
import logging
import config


async def get_new_polls(bot: Bot):
    await asyncio.sleep(10)
    while True:
        logging.info("Getting new polls...")
        try:
            new_polls = requests.get(config.API + "/api/user/notifications")
            print(new_polls.json())
            for notification in new_polls.json():
                for n in notification["notifications"]:
                    await bot.send_message(notification["id"], f"В мини-приложении доступен новый опрос: {n}")
        except requests.exceptions.RequestException:
            logging.error("Getting new polls failed.")
        await asyncio.sleep(config.NOTIFICATION_INTERVAL)
