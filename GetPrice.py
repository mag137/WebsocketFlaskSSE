from asyncio import run, gather

import ccxt.pro
import asyncio





DataList = []

# Функция watch_order_book является асинхронной и используется для отслеживания стакана ордеров на бирже.
async def watch_order_book(exchange = ccxt.pro.binance(), symbol = 'BTC/USDT'):
    # Бесконечный цикл
    while True:
        try:
            global DataList
            # Подписка
            # вызывает метод watch_order_book у объекта exchange,
            # который отслеживает стакан ордеров для заданного symbol
            # Оператор await ожидает завершения этой операции, прежде чем перейти к следующей строке кода.
            orderbook = await exchange.watch_order_book(symbol)
            # получает текущую дату и время с использованием метода iso8601 и milliseconds объекта exchange.
            datetime = exchange.iso8601(exchange.milliseconds())
            DataList = (datetime, orderbook['nonce'], symbol, orderbook['asks'][0], orderbook['bids'][0])
            print(DataList)
            await asyncio.sleep(1)
            # print("event")
        except Exception as e:
            print(type(e).__name__, str(e))
            break


# Функция reload_markets также является асинхронной и используется
# для периодической перезагрузки списка доступных рынков на бирже.
async def reload_markets(exchange, delay):#Передаем название биржи и задержку
    while True: #Бесконечный цикл
        try:
            await exchange.sleep(delay)# Задержка - приостанавливает выполнение на указанное время
            # Оператор await ожидает завершения этой операции, прежде чем перейти к следующей строке кода.
            markets = await exchange.load_markets(True)# загружает список доступных рынков.
            # TRUE - загружает все рынки
            # Оператор await ожидает завершения этой операции, прежде чем перейти к следующей строке кода.
            datetime = exchange.iso8601(exchange.milliseconds())
            # получает текущую дату и время с использованием метода iso8601 и milliseconds объекта exchange.
            # print(datetime, 'Markets reloaded')
            await asyncio.sleep(1)
        except Exception as e:
            print(type(e).__name__, str(e))
            break


async def main():
    # создает экземпляр объекта exchange класса ccxt.pro.binance()
    exchange = ccxt.pro.binance()
    # вызывает метод load_markets у объекта exchange, чтобы загрузить список доступных рынков на бирже.
    await exchange.load_markets()
    # exchange.verbose = True
    # определяет символ (торговую пару) для отслеживания стакана ордеров
    symbol = 'BTC/USDT'
    # определяет задержку (в миллисекундах) между перезагрузками списка доступных рынков.
    # В данном случае используется 60000 миллисекунд, что равно одной минуте.
    delay = 60000  # every minute = 60 seconds = 60000 milliseconds
    # создает список loops, содержащий две асинхронные функции: watch_order_book и reload_markets.
    # Эти функции будут выполняться параллельно.
    #print(delay)
    loops = [watch_order_book(exchange, symbol)]#, reload_markets(exchange, delay)]
    # вызывает функцию gather для выполнения асинхронных функций из списка loops.
    # Это позволяет выполнять эти функции параллельно.
    #print(loops)
    await gather(*loops)

    # вызывает метод close у объекта exchange, чтобы закрыть соединение с биржей и освободить ресурсы.

    await exchange.close()

if __name__ == '__main__':
    asyncio.run(main())
print("GetPrice stopped because it is running in another application...")