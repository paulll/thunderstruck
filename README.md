# Thunderstruck

Телеграм-бот, который просто пересылает помеченные сообщения в из конфы в канал. 

## Развертывание

```
git clone https://git.paulll.cc/paulll/thunderstruck.git && cd thunderstruck 
python3 -m pip install -r requirements.txt
nano src/secrets.py # указать токен и прочее
python3 app.py
```

Настройки в файле `src/config.py`