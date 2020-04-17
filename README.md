# Thunderstruck

Телеграм-бот, который просто пересылает помеченные сообщения в из конфы в канал. 

## Суть


### В целом

Есть конфа-флудилка, есть канал в телеграме.      
В конфе мы пишем что угодно, в канале только важная информация.      
Если кто-то отвечает на чье-то или своё сообщение текстом `!`, то то сообщение автоматически пересылается в канал, а сообщение `!` - удаляется.

![Как писать](https://habrastorage.org/webt/w0/cz/tc/w0cztcmu7hfgsqhvlclb46ppogg.png)
_Писать как-то так. Сообщение с восклицательным знаком будет сразу удалено, чтобы не засорять чат_

Таким образом, можно явно отметить сообщение как важное и оповестить всех нуждающихся.    

### Модерам

Чтобы бот игнорировал сообщения `!` от заданного человека, написать в ответ на любое его сообщение `!ban`
Отменить - аналогично, ответить на любое сообщение заданного человека текстом `!unban`.
Так как бот удаляет сообщения с `!`, посмотреть отправителя можно в истории действий чата. 
_Совсем не обязательно что автор сообщения - это тот же человек, что писал_ `!`


## Прогерам и любопытным

```
git clone https://git.paulll.cc/paulll/thunderstruck.git && cd thunderstruck 
python3 -m pip install -r requirements.txt
nano src/secrets.py # указать токен и прочее
python3 app.py
```

Настройки в файле `src/config.py`