from telethon import TelegramClient, events, sync, connection
from .secrets import api_id, api_hash, bot_token

client = TelegramClient(
	'alertbot', 
	api_id, 
	api_hash,
	connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
	proxy=('fi.a47.me', 1443, 'dd720945c9394dea5751b1958ac6d2aadd')
)

client.start(bot_token=bot_token)