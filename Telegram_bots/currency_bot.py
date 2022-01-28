from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def on_start(update, context):
	chat = update.effective_chat
	context.bot.send_message(chat_id=chat.id, text="Привет, я Валютный бот")


def on_message(update, context):
	chat = update.effective_chat
	text = update.message.text
	try:
		number = float(text)
		rate = 77.44
		dol = number * rate
		message = "$%.2f = %.2f $" % (number, dol)
		context.bot.send_message(chat_id=chat.id, text=message)
	except:
		context.bot.send_message(chat_id=chat.id, text="Напишите число для перевода")

token = "Place_for_your_token"

updater = Updater(token, use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(MessageHandler(Filters.all, on_message))

updater.start_polling()
updater.idle()
