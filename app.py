import telebot
from config import TOKEN, keys
from extensions import ExchangeException, Exchange


bot = telebot.TeleBot(TOKEN)

#Обрабатываем команду start:

@bot.message_handler(commands=['start'])
def start(message):
    text =  f'{message.from_user.first_name}, Приветствую Вас! Я,Бот-Конвертер валют.\n Меню:  \n- Список доступных валют: /values ; \
    \n- Вывести конвертацию валюты через команду: <имя валюты> <в какую валюту перевести> <количество переводимой валюты> (Например : рубль евро 1) ;\n \
- Напомнить, что я могу:/help .'
    bot.send_message(message.chat.id, text)

#Обрабатываеи команду help:
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Начать конвертацию - введите команду боту через пробел в следующем формате:' \
           ' \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты> ;' \
           '\n Например : рубль евро 1 ' \
           '\nСписок всех доступных валют - введите команду:\n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ExchangeException('Введите команду или 3 параметра. Например : рубль евро 1')

        quote, base, amount = values
        total_base = Exchange.get_price(quote, base, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()