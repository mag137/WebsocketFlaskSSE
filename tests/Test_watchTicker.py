import ccxt.pro as ccxtpro
import asyncio
import get_Triangle
import logging
# logging.basicConfig(level=logging.DEBUG)
print('CCXT version:', ccxtpro.__version__)
async def main():

    print('Тест, показывающий биржи с возможностью широковещательного просмотра цен ask и bid по всем инструментам одним запросом')
    for exchange_id in ccxtpro.exchanges:
        exchange = getattr(ccxtpro, exchange_id)()
        if exchange.has['watchOrderBook']:
            print(exchange.id, 'watchOrderBook', exchange.has['watchOrderBook'])
    print('_____________________________________________________________________')
    print('Тест на fetch_tickers')
    for exchange_id in ccxtpro.exchanges:
        exchange = getattr(ccxtpro, exchange_id)()
        if exchange.has['fetchTickers']:
            print(exchange.id, 'fetchTickers', exchange.has['fetchTickers'])
    print('_____________________________________________________________________')
    print('Тест на watchTickers')
    for exchange_id in ccxtpro.exchanges:
        exchange = getattr(ccxtpro, exchange_id)()
        if exchange.has['watchTickers']:
            print(exchange.id, 'watchTickers', exchange.has['watchTickers'])

    async def fetch_Bids_Asks(target_exchange, pair):
        while True:
            try:
                bids_asks = await target_exchange.watchTicker(pair)
                # print(bids_asks)
                now = target_exchange.milliseconds()
                # print(bids_asks['symbol'], bids_asks['asks'][0][0], bids_asks['bids'][0][0], target_exchange.iso8601(now))
                # print(target_exchange.iso8601(now), target_exchange.id, pair, bids_asks['asks'][0], bids_asks['bids'][0])
                # print(bids_asks['symbol'])
                if bids_asks['symbol'] == 'BTC/USDT':
                    print(bids_asks['ask'], bids_asks['bid'],target_exchange.iso8601(now))
                if bids_asks['symbol'] == 'RUNE/USDT':
                    print(bids_asks['ask'], bids_asks['bid'],target_exchange.iso8601(now))

                # #     print(target_exchange.iso8601(now), target_exchange.id, pair, bids_asks['asks'][0],
                #           bids_asks['bids'][0])

            except Exception as e:
                print(str(e))
                # Раскомментируйте, чтобы прервать все циклы в случае ошибки в любом из них
                # raise e
                break
    pairs = ['ZEN/USDT', 'RUNE/USDT', 'AAVE/USDT', 'SNX/USDT', 'BTC/USDT']
    # Создайте список задач для выполнения запросов асинхронно
    loops = [fetch_Bids_Asks(target_exchange, pair) for pair in pair_list[:]]
    # Запустите все задачи асинхронно
    print(len(loops))
    await asyncio.gather(*loops)
    await target_exchange.close()


target_exchange = ccxtpro.binance()
# Задайте новые пары для тикеров
pairs = ['DCR/BTC', 'AKRO/USDT', 'KUB/USDT', 'JUV/USDT', 'ETHW/USDD']
triangle_dict, get_tri_only_pair = get_Triangle.get_triangle(target_exchange.id, True, True)
pair_list = list(get_tri_only_pair)
# Запустите основную функцию
asyncio.run(main())
