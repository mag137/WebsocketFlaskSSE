import ccxt.pro as ccxtpro
import asyncio

print('Тест показывающий биржи с возможностью широковещательного просмотра цен ask и bid по всем инструментам одним запросом')
for exchange_id in ccxtpro.exchanges:
    exchange = getattr(ccxtpro, exchange_id)()
    if exchange.has['fetchBidsAsks']:
        print(exchange.id, 'fetchBidsAsks', exchange.has['fetchBidsAsks'])
