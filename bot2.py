import telebot
import os
import re
from dotenv import load_dotenv
from telebot import types, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.states import State, StatesGroup

load_dotenv()

TOKEN = os.getenv('TOKEN')

if TOKEN is None:
    print('Token is not found!')
    exit()

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage)

bot.add_custom_filter(custom_filters.StateFilter(bot))


class RegistrationStates(StatesGroup):
    waiting_for_number = State()


# клавіатури
registration_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
registration_btn = types.KeyboardButton("Реєстрація🪪")
registration_kb.add(registration_btn)

cancel_kb = types.InlineKeyboardMarkup()
cancel_btn = types.InlineKeyboardButton("Скасувати🚫", callback_data="cancel")
cancel_kb.add(cancel_btn)

remove_kb = types.ReplyKeyboardRemove()


@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(
        message.chat.id,
        "Привіт! Натисни реєстрацію щоб продовжити",
        reply_markup=registration_kb
    )


@bot.message_handler(func=lambda message: message.text and message.text == "Реєстрація🪪")
def registration_start(message):
    bot.send_message(
        message.chat.id,
        "⏲️ Оновлюємо інтерфейс...",
        reply_markup=remove_kb
    )

    bot.set_state(
        message.from_user.id,
        RegistrationStates.waiting_for_number,
        message.chat.id
    )

    bot.send_message(
        message.chat.id,
        "Введи свій номер телефону на який хочеш спам",
        reply_markup=cancel_kb
    )


@bot.message_handler(state=RegistrationStates.waiting_for_number)
def process_number(message):
    number = message.text
    number_pattern = r'^(\+380\d{9}|0\d{9})$'

    print(f"New number: {number}")

    if re.match(number_pattern, number):
        with open("numbers.txt", "a") as f:
            f.write(number + "\n")

        bot.send_message(
            message.chat.id,
            "Дякую! Номер збережено,тепер спам буде постійно,дякую ,що обрали мій бот)"
        )

        bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(
            message.chat.id,
            "Невірний формат номера! Спробуй ще раз."
        )


@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel_handler(call):
    bot.delete_state(call.from_user.id, call.message.chat.id)

    bot.send_message(
        call.message.chat.id,
        "Скасовано. Натисни реєстрацію знову.",
        reply_markup=registration_kb
    )

    bot.answer_callback_query(call.id)


if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling(skip_pending=True)