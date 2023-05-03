import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext

API_KEY = ""
user_id = ""

def curr_image(update: telegram.Update, context : CallbackContext):
    chat_id = update.message.chat_id
    with open("./images/tesla_plaid.png","rb") as img:
        context.bot.send_photo(chat_id=chat_id,photo=img)

def main():
    updater = Updater(API_KEY,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("current_image",curr_image))
    updater.start_polling()
    updater.idle()

def send_alert_telegram():
    bot = telegram.Bot(API_KEY)
    bot.send_message(chat_id=user_id,text="Helmet Rules violated!")
    with open("./images/camera_feed.jpg","rb") as img:
        bot.send_photo(chat_id=user_id,photo=img)

if __name__ == "__main__":
    send_alert_telegram()
    main()