"""
Удаляет сервисные сообщения (о вступлении в чат, все такое).
Сохряняет граф приглашений
"""
import asyncio
import time

from telethon import events, functions, types
from .client import client
from .config import channel_id, chat_id, do_forward_messages
from .ban_hammer import banlist
from .persistent import invite_graph


async def deletion_task(m):
    if m.action:
        print(m.action, m)
        if isinstance(m.action, types.MessageActionChatAddUser):
            for user_id in m.action.users:
                print("{} -> {}".format(m.from_id, user_id))
                invite_graph.append([time.time(), m.from_id, user_id])
        await m.delete()


@client.on(events.ChatAction)
async def handler(event):
    await deletion_task(event.action_message)
