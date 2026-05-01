import telebot
import os
import re
from dotenv import load_dotenv
from telebot import types
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from telebot.states import State,StatesGroup

load_dotenv()

TOKEN = os.getenv('TOKEN')

if TOKEN is None:
    print('Token is not found!')
    exit()

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN)

bot.add_custom_filter(custom_filter=custom_filters.StateFilter(bot))

class RegistrationStates(StatesGroup):
    waiting_for_email = State()


registration_kb = types.ReplyKeyboardMarkup(True)
registration_btn = types.KeyboardButton("Реєстрація🪪")
registration_kb.add(registration_btn)

cancel_kb = types.InlineKeyboardMarkup()
cancel_btn = types.InlineKeyboardButton("Скасувати🚫",callback_data="cancel")
cancel_kb.add(cancel_btn)

remove_kb = types.ReplyKeyboardRemove()

@bot.message_handler(commands=["start"])
def start_handler(message):
     bot.send_message(
         message.chat.id,
        "Привіт!Натисни реєстрація щоб отримувати спам на почту",
        reply_markup=registration_kb)

@bot.message_handler(func=lambda message:message.text.startswith("Реєстрація"))
def registration_start(message):
    temp_msg = bot.send_message(
        message.chat.id,
        "⏲️Оновлюємо інтерфейс...",
        reply_markup = remove_kb
    )
    bot.delete_message(message.chat.id,temp_msg.id)

    bot.set_state(
        message.from_user.id,
        RegistrationStates.waiting_for_email,
        message.chat.id
        )

    bot.send_message(
        message.chat.id,
        "Чудово!Надішли мені свою адресу електронної пошти,куди хочеш отримувати спам",
        reply_markup=cancel_kb)
    

@bot.message_handler(state=RegistrationStates.waiting_for_email)
def process_email(message):
    email = message.text
    email_pattern = r'^[\w\.-]+@[\w.-]+\.\w+$'
    print(f"New email:{email}")


    if re.match(email_pattern,email):
        with open("emails.txt","+a")as f:
            f.write(email)

        bot.send_message(
            message.chat.id,
            "Дякую! Тепер спам буде надходити тобі регулярно")
        bot.delete_state(message.from_user.id,message.chat.id)

    else :
        bot.send_message(
            message.chat.id,
            "Не схожу на адресу електронної пошти!Спробуй ще раз."
        )

@bot.callback_query_handler(lambda call:call.data == "cancel")
def cancel_handler(call):
    bot.send_message(
        call.message.chat.id,
        "Якщо передумаєш - натисни кнопку Реєстрація знову.",
        reply_markup=registration_kb
    )
    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    print("Bot in running...")
    bot.infinity_polling()