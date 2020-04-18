import json
import os.path
from telethon import events, functions
from telethon.tl.types import ChannelParticipantsAdmins

from .client import client
from .config import channel_id, chat_id, do_forward_messages, banlist_path

banlist = set(json.load(open(banlist_path, 'r'))) if os.path.isfile(banlist_path) else set()

@client.on(events.NewMessage)
async def handler(event):
	if event.reply_to_msg_id and event.message.message == '!ban':
		# От случайных людей и для прозрачности в целом
		if event.chat_id != chat_id:
			# Отвечаем только если писали в личку боту
			# Иначе просто молчим
			if event.chat_id > 0:
				await client.reply("Сорри, бот принимает сообщения только из конфы")
			return False

		# Проверка на админа
		# Просто удаляем сообщение в случае неудачи
		admin_users = await client.get_participants(chat_id, filter=ChannelParticipantsAdmins)
		admins = {u.id for u in admin_users}
		if not event.from_id in admins: 
			await client.delete_messages(event.chat_id, event.message)
			return False
	
		# Удаляем оба сообщения,
		# Добавляем в игнор юзера
		message = await client.get_messages(event.chat_id, ids=event.reply_to_msg_id)	
		await client.delete_messages(event.chat_id, [event.message, message] )

		banlist.add(message.from_id)
		json.dump(list(banlist), open(banlist_path, 'w'))

	if event.reply_to_msg_id and event.message.message == '!unban':
		# От случайных людей и для прозрачности в целом
		if event.chat_id != chat_id:
			await client.reply("Сорри, бот принимает сообщения только из конфы")
			return False

		# Проверка на админа
		# Просто удаляем сообщение в случае неудачи
		admin_users = await client.get_participants(chat_id, filter=ChannelParticipantsAdmins)
		admins = {u.id for u in admin_users}
		if not event.from_id in admins: 
			await client.delete_messages(event.chat_id, event.message)
			return False
	
		# Удаляем сообщение админа,
		# Убираем юзера из игнора
		message = await client.get_messages(event.chat_id, ids=event.reply_to_msg_id)	
		await client.delete_messages(event.chat_id, [event.message] )

		banlist.remove(message.from_id)
		json.dump(list(banlist), open(banlist_path, 'w'))	