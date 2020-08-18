from telethon import events
from .client import client
from .config import chat_id, do_remove_reposts


@client.on(events.NewMessage)
async def handler(event):
    if event.message.from_id is None and do_remove_reposts:
        await client.delete_messages(event.chat_id, event.message)
