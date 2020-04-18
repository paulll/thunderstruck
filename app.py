import logging
import src.alert_handler
import src.repost_handler
import src.ban_hammer

from src.client import client

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
client.run_until_disconnected()