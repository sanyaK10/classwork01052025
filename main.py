import telebot
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

if TOKEN is None:
    print('Token is not found!')
    exit()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    print(type(message))
    bot.reply_to(message, "Привіт, я ECHO-бот! Напиши мені щось і я повторю це.")

@bot.message_handler(commands=["info"])
def send_info(messange):
    first_name = messange.from_user.first_name
    last_name = messange.from_user.last_name
    user_name = messange.from_user.user_name
    chat_id = messange.chat.id
    user_id = messange.from_user.id
    msg_text = messange.text

    print(first_name, last_name, user_name, user_id, msg_text, chat_id)

    reply_msg = f"Привіт, {first_name}\n" \
                f"Твій Телеграм ID: {user_id}\n" \
                f"Твоє повідомлення: {msg_text}\n" \
                
    bot.reply_to(messange, reply_msg)








@bot.message_handler(func=lambda messange: messange.text.startswith("Hello"))
def hello_answer(messange):
    bot.send_message(messange.chat.id, "Привіт")



@bot.message_handler(func = lambda messange: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)



if __name__ == "main":
    print("Bot in running...")
    bot.infinity_polling()