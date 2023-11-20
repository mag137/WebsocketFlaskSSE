import ccxt as ccxt
import asyncio

async def watch_order_book(target_exchange=ccxt.pro.binance(), pair='BTC/USDT', log=False):
    # Бесконечный цикл
    while True:
        try:
            global symbols_data_dict, count
            orderbook = await target_exchange.watch_order_book(pair)
            data_list = {
                'symbol': orderbook['symbol'],
                'nonce': orderbook['nonce'],
                'ask': orderbook['asks'][0],
                'bid': orderbook['bids'][0],
                'datetime': orderbook['datetime'],
                'timestamp': orderbook['timestamp']
            }
            count += 1
            symbols_data_dict[pair] = data_list
            if log:
                print('watch_order_book ответ получен',pair,orderbook['asks'][0],count)
        except Exception as e:
            print(f"{__name__} 'watch_order_book' Исключение: {type(e).__name__}")
            print(f"Сообщение об ошибке: {str(e)}")
            print("Подробная трассировка:")