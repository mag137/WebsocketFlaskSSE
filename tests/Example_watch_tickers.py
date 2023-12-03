

import ccxt.pro as ccxtpro
import asyncio


async def main(loop):
    exchange = ccxtpro.binance({'enableRateLimit': True, 'asyncio_loop': loop, "type": "future", 'newUpdates': False})
    pair = ['DCR/BTC', 'AKRO/USDT', 'KUB/USDT', 'JUV/USDT', 'ETHW/USDD']

    if exchange.has['watchTickers']:
        while True:
            try:
                data = await exchange.watch_tickers()
                # data = await exchange.fetchTickers()
                # data = await exchange.fetchL1OrderBook()
                for key, value in data.items():
                    print("Key:", key)
                    print("ask:", value['ask'])
                    print("bid:", value['bid'])
                    print("Datetime:", value['datetime'])
                    # ... и так далее
                    print("\n")
                # print(exchange.iso8601(exchange.milliseconds()), tickers)
                # print(data)
            except Exception as e:
                print(str(e))
                # raise e  # uncomment to break all loops in case of an error in any one of them
                break
    else:
        print(exchange.id, 'does not support watchTickers')
        # stop the loop on exception or leave it commented to retry
        raise Exception('exchange does not support watchTickers')
    await exchange.close()
exchange_info = ccxtpro.binance()
loop = asyncio.new_event_loop()
loop.run_until_complete(main(loop))