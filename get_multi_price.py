# -*- coding: utf-8 -*-

import ccxt.pro
from asyncio import gather, run
import get_Triangle

async def symbol_loop(exchange, symbol):
    print('Starting the', exchange.id, 'symbol loop with', symbol)
    while True:
        try:
            orderbook = await exchange.watch_order_book(symbol)
            now = exchange.milliseconds()
            print(exchange.iso8601(now), exchange.id, symbol, orderbook['asks'][0], orderbook['bids'][0])
        except Exception as e:
            print(str(e))
            # raise e  # uncomment to break all loops in case of an error in any one of them
            break  # you can break just this one loop if it fails

async def main():

    symbols = ['KDA/USDT', 'KDA/BTC', 'BTC/USDT']
    loops = [symbol_loop(exchange, symbol) for symbol in symbols]
    await gather(*loops)
    await exchange.close()

exchange = ccxt.pro.kucoin({
        "apiKey": "655e1149aa87b00001139c0d",
        "secret": "2d445845-2ceb-4567-8b0b-bccb01926d81",
        # "password": "190180",
    })
triangle_dict, get_tri_only_pair = get_Triangle.get_triangle(exchange.id, True, True)
pair_list = list(get_tri_only_pair)

run(main())