import datetime
import math
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

STATE = None
BIRTH_YEAR = 1
BIRTH_MONTH = 2
BIRTH_DAY = 3

# Функция старт
def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(f"Привет {first_name}, рад знакомству!")
    start_getting_birthday_info(update, context)

def start_getting_birthday_info(update, context):
    global STATE
    STATE = BIRTH_YEAR
    update.message.reply_text(
        f"необходимо знать дату твоего рождения, подскажи когда ты родился...")

def received_birth_year(update, context):
    global STATE

    try:
        today = datetime.date.today()
        year = int(update.message.text)

        if year > today.year:
            raise ValueError("недопустимое значение")

        context.user_data['birth_year'] = year
        update.message.reply_text(
            f"хм, теперь нужен месяц (в формате цифр)...")
        STATE = BIRTH_MONTH
    except:
        update.message.reply_text(
            "забавно, но похоже не соответствует правде...")

def received_birth_month(update, context):
    global STATE

    try:
        today = datetime.date.today()
        month = int(update.message.text)

        if month > 12 or month < 1:
            raise ValueError("недопустимое значение")

        context.user_data['birth_month'] = month
        update.message.reply_text(f"Отлично! а теперь, день...")
        STATE = BIRTH_DAY
    except:
        update.message.reply_text(
            "забавно, но похоже не соответствует правде...")

def received_birth_day(update, context):
    global STATE

    try:
        today = datetime.date.today()
        dd = int(update.message.text)
        yyyy = context.user_data['birth_year']
        mm = context.user_data['birth_month']
        birthday = datetime.date(year=yyyy, month=mm, day=dd)

        if today - birthday < datetime.timedelta(days=0):
            raise ValueError("недопустимое значние")

        context.user_data['birthday'] = birthday
        STATE = None
        update.message.reply_text(f'ладно, ты рожден {birthday}')

    except:
        update.message.reply_text(
            "забавно, но похоже не соответствует правде...")

# Обработка Хелпа
def help(update, context):
    update.message.reply_text('запрос на помощ получен')

# Обработка ошибок
def error(update, context):
    update.message.reply_text('Ошибка')

# Обработка текста
def text(update, context):
    global STATE

    if STATE == BIRTH_YEAR:
        return received_birth_year(update, context)

    if STATE == BIRTH_MONTH:
        return received_birth_month(update, context)

    if STATE == BIRTH_DAY:
        return received_birth_day(update, context)

# Функция вызываемая по запросу биоритм
def biorhythm(update, context):
    print("ok")
    user_biorhythm = calculate_biorhythm(
        context.user_data['birthday'])

    update.message.reply_text(f"Физический: {user_biorhythm['phisical']}")
    update.message.reply_text(f"Эмоциональный: {user_biorhythm['emotional']}")
    update.message.reply_text(f"Интелектуальный: {user_biorhythm['intellectual']}")

def calculate_biorhythm(birthdate):
    today = datetime.date.today()
    delta = today - birthdate
    days = delta.days

    phisical = math.sin(2*math.pi*(days/23))
    emotional = math.sin(2*math.pi*(days/28))
    intellectual = math.sin(2*math.pi*(days/33))

    biorhythm = {}
    biorhythm['phisical'] = int(phisical * 10000)/100
    biorhythm['emotional'] = int(emotional * 10000)/100
    biorhythm['intellectual'] = int(intellectual * 10000)/100

    biorhythm['phisical_critical_day'] = (phisical == 0)
    biorhythm['emotional_critical_day'] = (emotional == 0)
    biorhythm['intellectual_critical_day'] = (intellectual == 0)

    return biorhythm

def main():
    TOKEN = "insert here your token and don't share it with anyone!"

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    
    dispatcher.add_handler(CommandHandler("biorhythm", biorhythm))

    dispatcher.add_handler(MessageHandler(Filters.text, text))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
