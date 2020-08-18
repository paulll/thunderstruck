"""
Для хранения данных между перезапусками

* Загружаем сохраненное состояние в начале
* Сохраняем состояние каждую секунду
"""

import json
import asyncio
import os

from .client import client
from .config import state_path

invite_graph = []
to_delete = set()

if os.path.isfile(state_path):
    state = json.load(open(state_path, "r"))
    invite_graph = state["invite_graph"] if "invite_graph" in state else []
    to_delete = set(state["to_delete"]) if "to_delete" in state else set()

# Перезаписываем файл только если изменилось состояние
async def save():
    old_serialized = ""
    while True:
        await asyncio.sleep(1)
        serialized = json.dumps(
            {"invite_graph": invite_graph, "to_delete": list(to_delete)}
        )
        if old_serialized != serialized:
            old_serialized = serialized
            with open(state_path, "w") as file:
                file.write(serialized)


client.loop.create_task(save())
