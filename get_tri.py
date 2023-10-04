import ccxt.pro as ccxtpro
import ccxt as ccxt
import asyncio

from tornado.httputil import qs_to_qsl

exchange_list = []
g_symbols = ()
g_pair = ()
g_quote = ()
dict_symbols = {}






async def watch_order_book(exchange, symbol ="BTC/USDT"):
    try:
        while True:
            orderbook = await exchange.watch_order_book(symbol)
            #print(exchange.iso8601(exchange.milliseconds()), symbol, orderbook['asks'][0], orderbook['bids'][0])
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print("Программа завершена по запросу пользователя (Ctrl+C).")

def get_exchanges():
    global exchange_list
    methods_and_attributes = dir(ccxt) # получим все методы библиотеки
    for ex in ccxtpro.exchanges: # выведем список всех поддерживаемых бирж
        print(ex)
    print(ccxtpro.exchanges)
    exchange_list = ccxtpro.exchanges[:]
# Создать объект биржи (в данном случае Binance)

def get_markets(obj):
    print(obj.__dir__())
    return obj.__dir__()
exchange = ccxtpro.binance()
symbol="BCH/USDT"
exchange.verbose = False


def get_market_data(ExTarget): # Функция получения всех инструментов, доступных на целевой бирже
    global g_symbols
    global g_pair
    get_allPairId_dict = {}
    get_allPairData_list = []
    get_allSymbolsId_list = []
    get_allSymbolsId_set = set()
    get_Symbols_Base_set = set()
    get_Symbols_Quote_set = set()





    non_unique = []
    singleSymbolId = set()
    twiceSymbolId = set()
    _exchange = getattr(ccxt, ExTarget)() # Динамическое создание экземпляра биржи
    markets = _exchange.load_markets() # Загрузка доступных рынков
    for pair in markets:
        market = markets[pair]
        #print(f"Symbol: {symbol}, Base: {market['base']}, Quote: {market['quote']}")
        '''get_Symbols_Quote_set - множество со всеми котировочными символами во всех парах'''
        get_Symbols_Quote_set.add(market['base'])
        '''get_Symbols_Base_set - множество со всеми базовыми символами во всех парах'''
        get_Symbols_Base_set.add(market['quote'])
        '''get_allSymbolsId_set - множество всех символов, которые используются для определения пары'''
        get_allSymbolsId_set.add(market['baseId'])
        get_allSymbolsId_set.add(market['quoteId'])
        '''get_allSymbolsId_list - список всех символов полученных из каждой пары с повторами'''
        get_allSymbolsId_list.append(market['baseId'])
        get_allSymbolsId_list.append(market['quoteId'])
        '''get_allPairId_dict - словарь всех пар рынка'''
        get_allPairId_dict[market['id']] = {'symbol':     market['symbol'], 'baseId':     market['baseId'], 'quoteId':     market['quoteId']}
        '''get_allPairData_list - список всех данных пар рынка: id, symbol, baseId, quoteId'''
        '''Добавим условие - только спотовый рынок'''
        if market['type'] == 'spot' and market['active'] == True:
            get_allPairData_list.append([market['id'], market['symbol'], market['baseId'], market['quoteId']])
    print(get_allPairData_list, '\n',len(get_allPairData_list))

    с = 0
    for i in range (len(get_allPairData_list)):
        #print(get_allPairData_list[i], len(get_allPairData_list))
        for j in range (i+1, len(get_allPairData_list)):
            intersection = set(get_allPairData_list[i]) & set(get_allPairData_list[j])
            if intersection:
                '''Получаем символы для третьей пары треугольника'''
                trisymbols = list(set(get_allPairData_list[i][2:]) ^ set(get_allPairData_list[j][2:]))
                '''Проверяем наличие искомой пары среди торгуемых пар'''
                for sublist in get_allPairData_list:
                    if len(trisymbols)>0:
                        if (trisymbols[0] == sublist[2] and trisymbols[1] == sublist[3] or trisymbols[0] == sublist[3] and trisymbols[1] == sublist[2]):
                            с += 1
                            print(get_allPairData_list[i][2:], get_allPairData_list[j][2:],"Общие элементы:", intersection,'Искомые:',trisymbols,"пара",sublist, с)


    for x in get_allSymbolsId_set:
        if get_allSymbolsId_list.count(x) == 1:
            '''singleSymbolId - Множество символов встречающихся во всех парах только один раз'''
            singleSymbolId.add(x)
        if get_allSymbolsId_list.count(x) == 2:
            '''twiceSymbolId - Множество символов встречающихся во всех парах два раза'''
            twiceSymbolId.add(x)
    # print('Только одна пара с этими символами по id:', len(singleSymbolId), 'шт.\n', singleSymbolId,'\n')
    # print('Только две пары с этими символами по id:',  len(twiceSymbolId),  'шт.\n', twiceSymbolId,'\n')
    # print("Общее количество в числителях",len(get_Symbols_Quote_set))
    # g_quote     = tuple(sorted(set(get_Symbols_Quote_set) - set (get_Symbols_Base_set)))
    # print("Общее количество неповторяющихся символов", len(g_quote))
    # g_symbols   = tuple(sorted(set(get_allSymbolsId_set)))
    #
    # q_base      = tuple(sorted(get_Symbols_Base_set))

    # print(len(g_quote),'',g_quote)
    # print(len(q_base), '', q_base)



    # print (singleSymbolId)
    for symbol in markets:              # Раскладываем данные рынков
        symbolData = markets[symbol]    # Получаем словари по каждой паре

        if symbolData['id'] in singleSymbolId:
            print (symbolData['id'])
            continue
        dict_symbols[symbolData['id']] = {'symbol': symbolData['symbol'], 'baseId': symbolData['baseId'], 'quoteId': symbolData['quoteId']}
        #print(symbol)
        # print(symbolData['id'])

    # print("ывфыавыы",symbolData)
    #print(dict_symbols)  #
    # print(len(dict_symbols))


    return markets #Возвращаем словарь с ключами-парами и аргументами словарями с данными

datamarket = get_market_data('binance')
# print(g_symbols)

def get_triangles(allsymbols):
    length = len(allsymbols)
    print(
        'всего символов',
        len(allsymbols)
    )
    c = 0
    # print(allsymbols[1] + allsymbols[2])
    for a in range (length):
        for b in range(a+1,length):
            for c in range(b+1, length):
                print(a,b,c)
                if (allsymbols[b] + '/' + allsymbols[a] or allsymbols[a] + '/' + allsymbols[b])\
                and (allsymbols[b] + '/' + allsymbols[c] or allsymbols[c] + '/' + allsymbols[b])\
                and (allsymbols[c] + '/' + allsymbols[a] or allsymbols[a] + '/' + allsymbols[c]) in g_pair:
                    c += 1
                    print(c)
                    # print(allsymbols[b] + '/' + allsymbols[a])
    print(c)
            #     print("орлорлрлр",g_pair)

                # print(a,b,c)
        # for b in pair:
        #     print(b)
    # return triangles # возвращаем словарь свозможными треугольниками
    pass
# get_triangles(g_symbols)
# Запустить асинхронную функцию
asyncio.run(watch_order_book(exchange, symbol))
