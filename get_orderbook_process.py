import asyncio
import get_Triangle

from multiprocessing import Process

async def symbol_orderbook_loop(exchange, symbol, input_delta_calc_data_queue, connection_attempts=0):
    import asyncio
    print('Starting the', exchange.id, 'symbol loop with', symbol)
    connection_attempts += 1
    while True:
        try:
            orderbook = await exchange.watch_order_book(symbol)
            ask = orderbook['asks'][0]
            bid = orderbook['bids'][0]
            # print(ask)
            if connection_attempts > 2:
                print(exchange.iso8601(now), exchange.id, symbol, ask, bid)
            '''Создадим кортеж с данными для очереди'''
            data_to_calc_delta_process = (symbol, ask, bid)
            input_delta_calc_data_queue.put(data_to_calc_delta_process)
            while not input_delta_calc_data_queue.empty():
                item = input_delta_calc_data_queue.get()
                print(item)

        except asyncio.CancelledError:
            print(f"CancelledError in symbol_orderbook_loop for {symbol}, Задача отменена")

        except Exception as e:
            print(f"Exception Error watch_order_book {e}, for {symbol}")
            connection_attempts += 1
            await handler(connection_attempts)
            if connection_attempts > 3:
                connection_attempts = 0
            await symbol_orderbook_loop(exchange, symbol, input_delta_calc_data_queue, connection_attempts)


async def handler(attempts):
    if attempts > 3:
        pause = 10
        print(f"Too many connection attempts for {symbol}, pause {pause}...")
    else:
        pause = 1
        print(f"Error watch_order_book for {symbol}, pause {pause}, reconnect, attempt {attempts}")
    await asyncio.sleep(pause)


