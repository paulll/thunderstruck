"""
Публикует сообщения в канал с важными уведомлениями.

* Если на сообщение ответили знаком "!"
* Если сообщение похоже на важное предупреждение типа "режим в общаге"
"""

import re
import string

from telethon import events, functions
from .client import client
from .config import channel_id, chat_id, do_forward_messages
from .ban_hammer import banlist

messages_already_forwarded = set()


@client.on(events.NewMessage)
async def handler(event):
    if event.reply_to_msg_id and event.message.message == "!":
        # От случайных людей и для прозрачности в целом
        if event.chat_id != chat_id:
            # Отвечаем только если писали в личку боту
            # Иначе просто молчим
            if event.chat_id > 0:
                await client.reply("Сорри, бот принимает сообщения только из конфы")
            return False

        # Удаление повторных и забаненных
        if (
            event.reply_to_msg_id in messages_already_forwarded
            or event.message.from_id in banlist
        ):
            await client.delete_messages(event.chat_id, event.message)
            return False
        messages_already_forwarded.add(event.reply_to_msg_id)

        # Пересылка или копирование сообщения
        # Пересылка, в теории, быстрее, так как не требует загрузки исходного сообщения
        # Хотя, telethon, возможно, под капотом кэширует последние сообщения
        if do_forward_messages:
            await client.forward_messages(
                channel_id, event.reply_to_msg_id, event.chat_id
            )
        else:
            message = await client.get_messages(
                event.chat_id, ids=event.reply_to_msg_id
            )
            await client.send_message(channel_id, message)
        await client.delete_messages(event.chat_id, event.message)

    elif event.chat_id == chat_id and event.message.from_id is not None:
        important_patterns = {
            r"^(воппер|офик|генерал|бес|генералы|офицер|бомж|лейтеха|лейт|капитан|кэп|опер|деж|дежурный|оперативный|беляев|собака|полкан|полковник|подпол|майор|режим) на (\d|четвертом|пятом|шестом|седьмом|восьмом|девятом)",
            r"^(режим|бес) в общаге$"
		}

        text = event.message.message.lower().translate(
            str.maketrans("", "", string.punctuation)
        )
        if any(re.match(x, text) for x in important_patterns):
            messages_already_forwarded.add(event.message.id)
            if do_forward_messages:
                await event.message.forward_to(channel_id)
            else:
                await client.send_message(channel_id, event.message)
