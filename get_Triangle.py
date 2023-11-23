import ccxt as ccxt
import time


def get_triangle(exchange, spot=True, log=True):  # Функция получения всех инструментов, доступных на целевой бирже
    triangle_dict = {}  # Основной словарь для собираемых треугольников
    get_all_pair_data_list = []
    get_all_symbols = set()
    get_all_pairs = set()
    get_tri_only_pair = set()
    _exchange = getattr(ccxt, str(exchange))()  # Динамическое создание экземпляра биржи

    markets = _exchange.load_markets()  # Загрузка доступных рынков
    current_unix_time = time.time()
    col = 0
    pairB_F_count = 0
    pairC_F_count = 0
    pairB_T_count = 0
    pairC_T_count = 0
    direct_b = True
    direct_c = False

    for pair in markets:
        market = markets[pair]
        '''get_all_pair_data_list - список всех данных пар рынка: id, symbol, baseId, quoteId'''
        '''Добавим условие - только спотовый рынок'''
        if market['active']:
            if spot and market['type'] != 'spot':
                continue
            get_all_pair_data_list.append([market['id'], market['symbol'], market['base'], market['quote'], market['precision'], market['limits']])
            '''Получим все неповторяющиеся символы с биржи'''
            get_all_symbols.add(market['base'])
            get_all_symbols.add(market['quote'])
            '''Получим все неповторяющиеся пары с биржи'''
            get_all_pairs.add(market['symbol'])

    duration_get_market_by_time = round((time.time() - current_unix_time)*1000, 2)
    current_unix_time = time.time()
    pair_b = ''
    pair_c = ''
    pair_a = ''
    for pair_a_data in get_all_pair_data_list: # Цикл по всем доступным парам. Берем любую доступную пару и ищем треугольник
        direct_a = True
        for symbolC in get_all_symbols: # К пробной паре прикручиваем символ из доступных
            """Пробуем добавить к паре символ С"""
            if symbolC in pair_a_data:  # Если символ совпадает с символом пары, то пропускаем итерацию
                continue
            if symbolC not in pair_a_data:  # Если такого символа в паре нет, значит будет третьим
                pair_a = pair_a_data[1]
                '''Ищем вычисленные пары на рынке. Составляем пары a/b b/c c/a'''
                """Ищем не инверсную пару B, если пара В прямая и идет через котируемый символ..."""
                if (pair_a_data[3] + '/' + symbolC) in get_all_pairs:
                    if (pair_a_data[2] + '/' + symbolC) in get_all_pairs:
                        pair_b = (pair_a_data[3] + '/' + symbolC)
                        pair_c = (pair_a_data[2] + '/' + symbolC)
                        tri_name = pair_a_data[1] + '/' + symbolC
                        pair_dict = {
                            'PairA': pair_a,
                            'dirA': direct_a,
                            'PairB': pair_b,
                            'dirB': direct_b,
                            'PairC': pair_c,
                            'dirC': direct_c
                        }
                        triangle_dict[tri_name] = pair_dict
                        pairB_T_count += 1
                    '''Если пара В прямая, то пара С Должна быть инверсной через базовый символ'''
                '''Если пара В прямая и идет через базовый символ'''
                if (symbolC + '/' + pair_a_data[2]) in get_all_pairs:
                    if (symbolC + '/' + pair_a_data[3]) in get_all_pairs:
                        pair_b = (symbolC + '/' + pair_a_data[2])
                        pair_c = (symbolC + '/' + pair_a_data[3])
                        tri_name = pair_a_data[1] + '/' + symbolC
                        pair_dict = {
                            'PairA': pair_a,
                            'dirA': direct_a,
                            'PairB': pair_b,
                            'dirB': direct_b,
                            'PairC': pair_c,
                            'dirC': direct_c
                        }
                        triangle_dict[tri_name] = pair_dict
                        pairB_T_count += 1
                    '''И если пара В прямая, то пара С Должна быть инверсная, через котируемый символ'''
                else:  # Если такой пары нет - пропускаем
                    continue

                get_tri_only_pair.update([pair_a, pair_b, pair_c])


    duration_constructor_by_time = round((time.time() - current_unix_time)*1000, 2)
    if log:
        print('Биржа:', exchange)
        print('Пары в треугольниках', get_tri_only_pair)
        print("Всего", len(get_all_pair_data_list), 'активных пар,состоящих из', len(get_all_symbols),
              'неповторяющихся символов. Затрачено времени:', duration_get_market_by_time, 'мс')
        print('Количество пар в треугольниках', len(get_tri_only_pair))
        print('Конструктор треугольников: количество:', len(triangle_dict),
              ". Затрачено времени:", duration_constructor_by_time, "мс")
        print('пара B True', pairB_T_count, 'False', pairB_F_count)
        print('пара C True', pairC_T_count, 'False', pairC_F_count)

    return triangle_dict, get_tri_only_pair


if __name__ == '__main__':
    get_triangle('poloniex', log=True)
