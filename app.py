import logging
import src.yoba_handler
import src.alert_handler
import src.repost_handler
import src.ban_hammer
import src.service_message_cleaner
import src.history_cleaner

from src.client import client

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


async def catch_up():
    await client.catch_up()


client.loop.create_task(catch_up())
client.run_until_disconnected()
