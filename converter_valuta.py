import requests
from datetime import datetime

def get_rates():

    # Получает актуальные курсы валют с сайта ЦБ РФ.
    # Возвращает словарь {код_валюты: курс_к_рублю}.

    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    data = requests.get(url).json()
    rates = {"RUB": 1.0}
    for code, info in data["Valute"].items():
        rates[code] = info["Value"] / info["Nominal"]
    return rates


def convert_currency(amount, from_currency, to_currency):

    # Конвертирует сумму из одной валюты в другую.

    rates = get_rates()
    if from_currency not in rates or to_currency not in rates:
        return None
    amount_in_rub = amount * rates[from_currency]
    converted = amount_in_rub / rates[to_currency]
    return converted

def log_history(message):
    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f'{message}\n')

if __name__ == "__main__":
    amount = float(input("Введите сумму: "))
    from_currency = input("Введите исходную валюту (USD, EUR, RUB, ...): ").upper()
    to_currency = input("Введите целевую валюту (USD, EUR, RUB, ...): ").upper()

    result = convert_currency(amount, from_currency, to_currency)
    if result:
        print(f"{amount} {from_currency} = {result:.2f} {to_currency}")
        log_history(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {amount} {from_currency} → {result:.2f} {to_currency}")
    else:
        print("Ошибка: валюта не найдена.")
