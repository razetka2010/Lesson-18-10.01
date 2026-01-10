import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import TOKEN
import json
import os

DATA_FILE = "user.json"

def load_json():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

users = load_data()

longpoll = VkLongPoll(vk_session)
print("Бот с памятью запущен!")

def cmd_setname(uid, text):
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return "Напиши так: /setname Имя"
    
    name = parts[1].atrip()
    if not name:
        return "Имя не может быть пустым"
    
    uid = str(uid)
    if uid not in users:
        users[uid] = {}

    users[uid]["name"] = name
    save_data(users)

    return f"Готово! Я запомнил: тебя зовут {name}"

def cmd_whoami(uid, text=None):
    uid = str(uid)
    if uid not in users:
        return "Я тебя не знаю. Напиши: /setname Имя"
    
    name = users[uid].get('name', 'Без имени')
    return f"Ты - {name}"

def handle_command(uid, text):
    cmd = text.split()[0].lower()

    if cmd in commands:
        return commands[cmd](uid, text)
    else:
        return "Неизвестная команда"
    

def send(uid, text=""):
    vk.message.send(
        user_id=uid,
        message=text,
        random_id=0
    )

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        text = (event.text or "").strip().lower().lower()

        if text == '/start':
            vk.messages.send(
                user_id=user_id,
                message="Привет",
                random_id=0
            )
        elif text == '/help':
            vk.messages.send(
                user_id=user_id,
                message="Доступные команды:\nstart,\nhelp\n Бот создан для сохранения имени;\n для просмотра сохранения имени;\n для просмотра справки\n",
                random_id=0
            )
        else:
            vk.messages.send(
                user_id=user_id,
                message="Я ещё не знаю этой команды попробуйте что-то другое! /help",
                random_id=0
            )