import asyncio
import ccxt.pro as ccxtpro
import time
async def main(loop):
    exchange = ccxtpro.poloniex({'enableRateLimit': True, 'asyncio_loop': loop, "type": "future", 'newUpdates': False})
    tickers = ['DCR/BTC', 'AKRO/USDT', 'KUB/USDT', 'JUV/USDT', 'ETHW/USDD']

    for t in tickers:
        await exchange.watch_order_book(t)

    while True:
        for t in tickers:
            if t in exchange.orderbooks:

                print(f"---- {t}")
                print(exchange.orderbooks[t]['bids'][0])
                print(exchange.orderbooks[t]['asks'][0])
                print(exchange.iso8601(exchange.milliseconds()))

            await exchange.sleep(0.01)

loop = asyncio.new_event_loop()
loop.run_until_complete(main(loop))