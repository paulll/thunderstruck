from telethon import TelegramClient, events, sync, connection
from .secrets import api_id, api_hash, bot_token

client = TelegramClient(
	'alertbot', 
	api_id, 
	api_hash,
	connection=connection.ConnectionTcpMTProxyRandomizedIntermediate
)

client.start(bot_token=bot_token)