import json
import requests
from config import *
class ExchangeException(Exception):
    pass


class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ExchangeException(
                f'Одинаковые валюты не переводяться {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ExchangeException(f'Не смог обработать валюту {quote} . Введите команду /values или 3 параметра.'
                                    f'\n Например: рубль евро 1 ')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ExchangeException(f'Не смог обработать валюту {base} . Введите команду /values или 3 параметра.'
                                    f'\n Например: рубль евро 1 ')


        try:
            if int (amount) > 0:
                amount = int(amount)
            else:
                raise ExchangeException (f'Количество не может быть отрицательным: {amount}. '
                                    f'\nВведите 3 параметра.'
                                    f'\n Например: рубль евро 1 ')
        except ValueError:
            raise ExchangeException(f'Не смог обработать валюту {amount} . Введите команду /values или 3 параметра.'
                                    f'\n Например: рубль евро 1 ')


        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return round(float (total_base * amount), 2)