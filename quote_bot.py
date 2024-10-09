import random
import telebot
from telebot import types
import schedule
import time
from threading import Thread

# Ваш токен от BotFather
TOKEN = 'Ваш токен'
bot = telebot.TeleBot(TOKEN)

# Список нелепых цитат
quotes = [
    "Мы продолжаем то, что мы продолжаем делать. - Джордж Буш",
    "Здесь нет ничего, кроме исторической паранойи. - Генри Киссиндже",
    "Я могу видеть Россию из своего окна. - Сара Пейлин",
    "Это явно был не их день. - Мэр Торонто после снегопада",
    "Думаю, что интернет — это как много труб. - Джордж Буш",
]

# Хранение времени отправки цитат для каждого пользователя
user_schedule = {}

# Функция для отправки случайной цитаты
def send_quote(chat_id):
    quote = random.choice(quotes)
    bot.send_message(chat_id, quote)

# Команда для получения цитаты
@bot.message_handler(commands=['quote'])
def handle_quote(message):
    send_quote(message.chat.id)

# Функция для установки времени
@bot.message_handler(commands=['set_time'])
def set_time(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add("09:00", "12:00", "15:00", "18:00")
    bot.send_message(message.chat.id, "Выберите время для получения цитат:", reply_markup=keyboard)

# Обработка выбора времени
@bot.message_handler(func=lambda message: message.text in ["09:00", "12:00", "15:00", "18:00"])
def handle_time_selection(message):
    user_schedule[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"Цитаты будут отправляться в {message.text} каждый день.")
    schedule_daily_quotes(message.chat.id, message.text)

# Ежедневная отправка цитат
def daily_quotes(chat_id):
    send_quote(chat_id)

# Запуск планировщика для ежедневной отправки
def schedule_daily_quotes(chat_id, time_str):
    # Если уже есть запланированное время для данного пользователя, убираем его
    if chat_id in user_schedule:
        schedule.clear(chat_id)

    # Запланировать отправку цитаты в выбранное время
    schedule.every().day.at(time_str).do(daily_quotes, chat_id).tag(chat_id)

# Запуск планировщика в отдельном потоке
def schedule_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)

t = Thread(target=schedule_thread)
t.start()

# Функция для отображения меню команд при запуске
@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('/quote', '/set_time')
    bot.send_message(message.chat.id, "Привет! Я бот, который отправляет цитаты. Вот доступные команды:", reply_markup=keyboard)

# Запуск бота
bot.polling(none_stop=True)
