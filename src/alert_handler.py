from telethon import events, functions
from .client import client
from .config import channel_id, chat_id, do_forward_messages
from .ban_hammer import banlist

messages_already_forwarded = set()

@client.on(events.NewMessage)
async def handler(event):
	if event.reply_to_msg_id and event.message.message == '!':
		# От случайных людей и для прозрачности в целом
		if event.chat_id != chat_id:
			await client.reply("Сорри, бот принимает сообщения только из конфы")
			return False

		# Удаление повторных и забаненных
		if event.reply_to_msg_id in messages_already_forwarded or event.message.from_id in banlist:
			await client.delete_messages(event.chat_id, event.message)
			return False
		messages_already_forwarded.add(event.reply_to_msg_id)
		
		# Пересылка или копирование сообщения
		# Пересылка, в теории, быстрее, так как не требует загрузки исходного сообщения
		# Хотя, telethon, возможно, под капотом кэширует последние сообщения
		if do_forward_messages:
			await client.forward_messages(channel_id, event.reply_to_msg_id, event.chat_id)
		else:
			result = await client(functions.messages.GetMessagesRequest(id=[event.reply_to_msg_id]))
			messsage = result.messages[0]
			await client.send_message(channel_id, messsage)
		await client.delete_messages(event.chat_id, event.message)
