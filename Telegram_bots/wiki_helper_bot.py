import telebot, wikipedia, re

bot = telebot.TeleBot('Place_for_your_token')

wikipedia.set_lang("ru")

def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первые полторы тысячи слов
        wikitext=ny.content[:1500]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Убираем все после последней точки
        wikimas = wikimas[:-1]
        # Переменная для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков равно
        for x in wikimas:
            if not('==' in x):
                # Если в строке осталось больше трёх символов, то добавляем её
                if(len((x.strip()))>3):
                    wikitext2=wikitext2+x+'.'
            else:
                break
        # При помощи регулярных выражений избавляемя от разметки
        wikitext2=re.sub('\([^()]*\)', '',wikitext2)
        wikitext2=re.sub('\([^()]*\)', '',wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем строку
        return wikitext2
    # Обрабатываем исключения, которые могли быть вызваны работой модуля Вики
    except Exception as e:
        return 'В энциклопедии нет информации об этом'

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте любое слово, и я найду его значение в Вики')

# Получение сообщений от пользователя
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, getwiki(message.text))

# Запуск бота
bot.polling(none_stop=True, interval=0)
