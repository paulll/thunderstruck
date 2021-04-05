from datetime import datetime, timezone
from telethon import events, functions
from .client import client
from .config import chat_id, do_forward_messages
from collections import Counter
import asyncio

second = 1
minute = 60 * second
hour = 60 * minute
day = 24 * hour

threshold = 2

commands = Counter()
commandStatuses = dict()

async def clearStats():
    while True:
        await asyncio.sleep(day)
        for msg in commandStatuses.values():
            await msg.delete()
        commands.clear()
        commandStatuses.clear()

@client.on(events.NewMessage)
async def handler(event):
    if event.chat_id != chat_id:
        return
    text = event.message.message.strip().split('@')[0]
    if text.startswith('/'):
        print('Yoba detected')
        commands.update([text])
        if commands[text] >= threshold:
            print(f"Yoba threshold reached for command {text}")
            if text in commandStatuses:
                if commandStatuses[text]:
                    await commandStatuses[text].edit(text=f"Ура, нас уже {commands[text]} идиотов! Жми {text} и присоединяйся")
            else:
                commandStatuses[text] = None
                commandStatuses[text] = await client.send_message(chat_id, f"Ура, нас уже {commands[text]} идиотов! Жми {text} и присоединяйся")

client.loop.create_task(clearStats())