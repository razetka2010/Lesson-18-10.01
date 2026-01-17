import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import TOKEN
import json
import os

DATA_FILE = "users.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

longpoll = VkLongPoll(vk_session)
users = load_data()
print("Бот с памятью запущен!")

def send(uid, text):
    vk.messages.send(
        user_id=uid,
        message=text,
        random_id=0
    )

def cmd_setname(uid, text):
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return "Напиши так: /setname Имя"
    
    name = parts[1].strip()
    if not name:
        return "Имя не может быть пустым."
    
    uid = str(uid)
    if uid not in users:
        users[uid] = {}

    users[uid]["name"] = name
    save_data(users)

    return f"Готово! Я запомнил: тебя зовут {name}"

def cmd_whoami(uid, text=None):
    uid = str(uid)
    if uid not in users:
        return "Я тебя пока не знаю. Напиши: /setname Имя"
    
    name = users[uid].get("name", "Без имени")
    return f"Ты - {name}"

def  cmd_start(uid, text=None):
    return "Привет! Я бот\n Команды:\n /setname [имя] - сохранить имя\n/whoami - посмотреть имя\n/help - справка"

def cmd_help(uid, text=None):
    return "Все команды:\n/start - приветствие и список команд\n/setname [имя] - сохранить имя\n/whoami - посмотреть имя\n/help - это мправка\n"

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        uid = event.user_id
        text = (event.text or "").strip()

        if text == "/start":
            respone = cmd_start(uid)
        elif text == "/help":
            respone = cmd_help(uid)
        elif text.startswith("/setname"):
            respone = cmd_setname(uid, text)
        elif text == "/whoami":
            respone = cmd_whoami(uid)
        else:
            respone = "Не знаю такую команду. Напиши /help"

        send(uid, respone)  