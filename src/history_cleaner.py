"""
Удаляет старые сообщения, ttl зависит от содержимого:
объявления живут дольше, а опасные удаляются почти сразу.

Как работает:
* При запуске читает список сохраненных сообщений
* !save с ответом на сообщение -> сохранить
* При запуске проверяем все старые сообщения
* При поступлении нового сообщения ставим таймер
"""
import re
import asyncio
import time

from datetime import datetime, timezone
from telethon import events, functions
from .client import client
from .config import channel_id, chat_id, do_forward_messages
from .ban_hammer import banlist
from .persistent import to_delete

second = 1
minute = 60 * second
hour = 60 * minute
day = 24 * hour


def get_message_ttl(text):
    text_lowercase = text.lower()

    # /команды
    if text.startswith('/'):
        return minute

    # Объявления
    sell_buy_signatures = {
        "#объявление",
        "объявление",
        "куплю",
        "продам",
        "отдам",
        "продаю",
        "покупаю",
    }
    if any(
        re.search(r"\b{}\b".format(signature), text_lowercase)
        for signature in sell_buy_signatures
    ):
        return 4 * day

    # Потенциально опасные сообщения
    danger_signatures = {
        "бес",
        "алпач",
        "алпацкий",
        "бессонов",
        "офицер",
        "деж",
        "дежурный",
        "ответственный",
        "опер",
        "оперативный",
        "опердеж",
        "корпоративный",
        "майор",
        "полкан",
        "полковник",
        "майор",
        "майорчик",
        "капитан",
        "прапор",
        "прапорщик",
        "лейтеха",
        "лейтёха",
        "лейт",
        "лейтенант",
		"офик",
		"воппер",
		"кэп",
		"кэпчик",
		"ген",
		"генерал"
    }
    if any(
        re.search(r"\b{}\b".format(signature), text_lowercase)
        for signature in danger_signatures
    ):
        return 15 * minute

    # По-умолчанию
    return 2 * hour


async def deletion_task(m):
    to_delete.add(m.id)
    ttl = get_message_ttl(m.message)
    time_passed = (datetime.now(timezone.utc) - m.date).total_seconds()
    actual_ttl = ttl - time_passed if time_passed < ttl else 0
    print("deleting", m.id, "in", actual_ttl, "seconds")
    await asyncio.sleep(actual_ttl)
    if m.id in to_delete:
        await m.delete()
        to_delete.remove(m.id)


async def remove_older_messages():
    async for m in client.iter_messages(chat_id, ids=list(to_delete)):
        if m is not None:
            asyncio.create_task(deletion_task(m))


@client.on(events.NewMessage)
async def handler(event):
    print(event)
    if event.chat_id not in { chat_id, channel_id }:
        return
    if event.reply_to_msg_id and event.message.message == "!save":
        to_delete.remove(event.reply_to_msg_id)
        await event.message.delete()
        return
    client.loop.create_task(deletion_task(event.message))


client.loop.create_task(remove_older_messages())
