import telebot

# Создаем экземпляр
bot = telebot.TeleBot('place_for_your_token')

# Функция обрабатывающая /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь')

# Получение пользовательских сообщений
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)

# Запуск бота
bot.polling(none_stop=True, interval = 0)
