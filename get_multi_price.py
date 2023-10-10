import ccxt.pro
import asyncio
import get_Triangle
import time

# Глобальный словарь для хранения значений
data_dict = {}
exchange = ccxt.pro.binance()
triangle_dict, get_tri_only_pair = get_Triangle.get_triangle(exchange.id, True, True)


def run_async_function():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_multi_watch_order_book())
    loop.close()


async def start_multi_watch_order_book():
    # Создание списка задач
    tasks = [watch_order_book(exchange, pair) for pair in get_tri_only_pair]
    tasks.append(PrintData())
    # Запуск задач параллельно
    await asyncio.gather(*tasks)
    await exchange.close()

async def watch_order_book(target_exchange=ccxt.pro.binance(), pair='BTC/USDT'):
    # Бесконечный цикл
    while True:
        try:
            global data_dict
            orderbook = await target_exchange.watch_order_book(pair)
            data_list = {
                'symbol': orderbook['symbol'],
                'nonce': orderbook['nonce'],
                'ask': orderbook['asks'][0],
                'bid': orderbook['bids'][0],
                'datetime': orderbook['datetime'],
                'timestamp': orderbook['timestamp']
            }
            data_dict[orderbook['symbol']] = data_list
            # print(data_dict.keys())
        except Exception as e:
            print(type(e).__name__, str(e))
            break


async def PrintData():
    while True:
        a = 'ETH/USDT'
        if a in data_dict:
            print(data_dict[a])
        await asyncio.sleep(0.2)


# Запуск основной асинхронной функции
asyncio.run(start_multi_watch_order_book())
