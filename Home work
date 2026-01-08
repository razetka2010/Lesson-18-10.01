import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from config import TOKEN

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

longpoll = VkLongPoll(vk_session)
print("Игровой бот запущен!")

game_state = {}

def send(uid, text="", attachment=None):
    vk.messages.send(
        user_id=uid,
        message=text,
        attachment=attachment or "",
        random_id=random.randint(0, 2**64)
    )

def start_number_game(uid):
    secret = random.randint(1, 10)
    game_state[uid] = {"mode": "number", "secret": secret}
    send(uid, "Я загадал число от 1 до 10!")

def start_city_game(uid):
    cities = {
        "великие луки": "photo-234450844_456239027",
        "невель": "photo-234450844_456239028",
        "усвяты": "photo-234450844_456239030",
        "псков": "photo-234450844_456239029",
        "велиж": "photo-234450844_456239026"
    }
    city, photo_id = random.choice(list(cities.items()))
    game_state[uid] = {"mode": "city_photo", "city": city}  # Исправлено: "city" вместо "сity"
    send(uid, text="Угадай город по фотографии:", attachment=photo_id)

def start_truth_game(uid):
    facts = [
        ("У пингвинов есть колени.", "правда"),
        ("Жирафы не умеют спать.", "ложь"),
        ("Python назван в честь змеи.", "ложь"),
    ]
    text, correct = random.choice(facts)
    game_state[uid] = {"mode": "quiz", "correct": correct.lower()}
    send(uid, f"Правда или ложь?\n{text}")

def start_yesno_game(uid):
    words = ["да", "нет"]
    secret = random.choice(words)
    game_state[uid] = {"mode": "yesno", "secret": secret}
    send(uid, 'Я думаю о слове. Это "да" или "нет"?')

def process_game(uid, text):
    if uid not in game_state:
        return

    mode = game_state[uid]["mode"]
    user_answer = text.strip().lower()

    if mode == "number":
        if not user_answer.isdigit():
            send(uid, "Введи число от 1 до 10")
            return

        guess = int(user_answer)
        secret = game_state[uid]["secret"]

        if guess == secret:
            send(uid, "Верно! Ты угадал число!")
        else:
            send(uid, f"Неверно! Я загадал {secret}. Попробуй ещё раз!")

        game_state.pop(uid)
        return

    elif mode == "city_photo":
        correct = game_state[uid]["city"]

        if user_answer == correct:
            send(uid, "Правильно! Молодец!")
        else:
            send(uid, f"Неверно! Это был: {correct.capitalize()}")

        game_state.pop(uid)
        return

    elif mode == "quiz":
        correct = game_state[uid]["correct"]

        if user_answer == correct:
            send(uid, "Верно! Отлично!")
        else:
            send(uid, f"Неправильно! Правильный ответ: {correct.capitalize()}")

        game_state.pop(uid)
        return

    elif mode == "yesno":
        secret = game_state[uid]["secret"]

        if user_answer in ["да", "нет"]:
            if user_answer == secret:
                send(uid, f'Верно! Я задумал "{secret}".')
            else:
                send(uid, f'Неверно! Я задумал "{secret}".')
        else:
            send(uid, 'Нужно ответить "да" или "нет". Попробуй ещё раз.')
            return

        game_state.pop(uid)
        return

commands = {
    "игры": "menu",
    "1": start_number_game,
    "2": start_city_game,
    "3": start_truth_game,
    "4": start_yesno_game
}

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        uid = event.user_id
        text = (event.text or "").strip().lower()

        if uid in game_state:
            process_game(uid, text)
            continue

        if text == "игры":
            send(uid,
                 "Выбери игру:\n"
                 "1 - Угадай число\n"
                 "2 - Угадай город по фотографии\n"
                 "3 - Правда или ложь\n"
                 "4 - Да или Нет")
            continue
            
        if text in commands and callable(commands[text]):
            commands[text](uid)
            continue
        send(uid, "Я тебя не понял. Напиши 'игры', чтобы увидеть список игр")
