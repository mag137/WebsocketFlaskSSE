import ccxt as ccxt
import time
import os
from pprint import pprint

file_path = __file__
file_name = os.path.basename(file_path)
print("Имя текущего файла:", file_name)

"""Основная функция получения всех инструментов, доступных на целевой бирже"""
'''Для заполнения словарей статическими данными'''


def get_triangle(exchange, spot=True, log=True, max_retries=3, retry_delay=1):
    for _ in range(max_retries):
        try:

            triangle_dict = {}    # Основной словарь для собираемых треугольников
            get_triangle_in_pair_dict = {}  # Словарь наличия пары в треугольниках
            get_all_pair_data_list = []    # Список содержащий свойства одной пары рынка
            get_all_symbols_set = set()  # Множество содержащее все доступные символы
            get_all_pairs_set = set()  # Множество содержащее все доступные пары
            get_tri_only_pair_set = set()  # Множество содержащее пары только треугольников
            _exchange = getattr(ccxt, str(exchange))()  # Динамическое создание экземпляра биржи
            markets = _exchange.load_markets()  # Загрузка доступных рынков
            count = 0
            c4 = 0
            for pair in markets:
                market = markets[pair]
                '''get_all_pair_data_list - список всех данных пар рынка: id, symbol, baseId, quoteId'''
                '''Добавим условие - только спотовый рынок'''
                if market['active']:
                    if spot and market['type'] != 'spot':
                        continue
                    '''Получение всех свойств одной пары рынка'''
                    get_all_pair_data_list.append([market['id'],
                                                   market['symbol'],
                                                   market['base'],
                                                   market['quote'],
                                                   market['precision'],
                                                   market['limits']])
                    '''Получим все неповторяющиеся символы с биржи'''
                    get_all_symbols_set.add(market['base'])
                    get_all_symbols_set.add(market['quote'])
                    '''Получим все неповторяющиеся пары с биржи'''
                    get_all_pairs_set.add(market['symbol'])
            """Цикл по всем доступным парам. Берем любую доступную пару и ищем треугольник"""
            for pair_a_data in get_all_pair_data_list:
                """К пробной паре прикручиваем символ из доступных"""
                for symbolC in get_all_symbols_set:
                    """Пробуем добавить к паре символ С"""
                    """Если символ совпадает с символом пары, то пропускаем итерацию"""
                    if symbolC in pair_a_data:
                        continue
                    pair_a = pair_a_data[1]
                    if (pair_a_data[3] + '/' + symbolC) in get_all_pairs_set:
                        if (pair_a_data[2] + '/' + symbolC) in get_all_pairs_set:
                            pair_b = (pair_a_data[3] + '/' + symbolC)
                            pair_c = (pair_a_data[2] + '/' + symbolC)
                            tri_assemble = pair_a_data[1] + '/' + symbolC
                            count += 1
                            pair_dict = {
                                'PairA': pair_a,
                                'PairB': pair_b,
                                'PairC': pair_c,
                                'Number': count
                            }
                            tri_name = str(count) + "-" + tri_assemble.replace("/", "-")
                            # tri_name = tri_assemble.replace("/", "-")
                            triangle_dict[tri_name] = pair_dict
                            if pair_a in get_triangle_in_pair_dict:
                                get_triangle_in_pair_dict[pair_a].append(tri_name)
                            else:
                                c4 += 1
                                # print(pair_a, "- Новая пара", c4)
                                get_triangle_in_pair_dict[pair_a] = [tri_name]
                                get_tri_only_pair_set.add(pair_a)

                            if pair_b in get_triangle_in_pair_dict:
                                get_triangle_in_pair_dict[pair_b].append(tri_name)
                            else:
                                c4 += 1
                                # print(pair_b, "- Новая пара", c4)
                                get_triangle_in_pair_dict[pair_b] = [tri_name]
                                get_tri_only_pair_set.add(pair_b)

                            if pair_c in get_triangle_in_pair_dict:
                                get_triangle_in_pair_dict[pair_c].append(tri_name)
                            else:
                                c4 += 1
                                # print(pair_c, "- Новая пара", c4)
                                get_triangle_in_pair_dict[pair_c] = [tri_name]
                                get_tri_only_pair_set.add(pair_c)
                    else:  # Если такой пары нет - пропускаем
                        continue

            current_unix_time = time.time()
            duration_constructor_by_time = round((time.time() - current_unix_time)*1000, 2)
            get_tri_only_pair_list = list(get_tri_only_pair_set)
            if log:
                print('Биржа:', exchange)
                for key, value in triangle_dict.items():
                    print(key.ljust(35), value, sep='\t')

                print("Всего", len(get_all_pair_data_list), 'активных пар,состоящих из', len(get_all_symbols_set),
                      'неповторяющихся символов.')
                print('Количество пар в треугольниках', len(get_tri_only_pair_set))
                print('Конструктор треугольников: количество:', len(triangle_dict),
                      ". Затрачено времени:", duration_constructor_by_time, "мс")

            '''Проверка на одинаковые треугольники в словаре triangle_dict'''
            c1: int = 0
            for trikey in triangle_dict:
                for trikey2 in triangle_dict:
                    if trikey == trikey2:
                        continue
                    parsed_stroke = trikey.split('-')
                    sym_a = parsed_stroke[1]
                    sym_b = parsed_stroke[2]
                    sym_c = parsed_stroke[3]
                    parsed_stroke2 = trikey2.split('-')  # список типа:['1699', 'USTC/FDUSD', 'FDUSD/USDT', 'USTC/USDT']
                    if sym_a in parsed_stroke2 and sym_b in parsed_stroke2 and sym_c in parsed_stroke2:
                        print('есть одинаковые')
                        num1 = int(triangle_dict[trikey]['Number'])
                        num2 = int(triangle_dict[trikey2]['Number'])
                        c1 += 1
                        print(f'{c1}одинаковые {trikey} {num1} и {trikey2} {num2}')
                        # print('одинаковые', parsed_stroke2, c1, num1, num2)
            print(f'Обнаружено {c1} одинаковых треугольников.')
            '''Возвращаем словарь triangle_dict вида 1699-USTC-FDUSD-USDT 
            {'PairA': 'USTC/FDUSD', 'PairB': 'FDUSD/USDT', 'PairC': 'USTC/USDT', 'Number': 1699}'''
            '''И возвращаем список пар get_tri_only_pair_list участвующих в треугольниках '''
            '''И возвращаем словарь get_triangle_in_pair_dict в каких треугольниках присутствует ключевая пара
            {'MANTA/BNB': [ '1577-MANTA-BNB-USDT',
                            '1578-MANTA-BNB-FDUSD',
                            '1579-MANTA-BNB-TRY',
                            '1580-MANTA-BNB-BTC']}
            '''
            # pprint(get_triangle_in_pair_dict, indent=4, sort_dicts=False)
            print('Всего пар в словаре get_triangle_in_pair_dict:', len(get_triangle_in_pair_dict))
            return triangle_dict, get_tri_only_pair_list, get_triangle_in_pair_dict

        except ccxt.NetworkError as e:
            print(f"Ошибка сети: {e}")
            print(f"Повторная попытка через {retry_delay} секунд.")
            time.sleep(retry_delay)
            retry_delay *= 2
    print(f"Превышено максимальное количество попыток ({max_retries}). Завершение выполнения функции.")
    return None, None


if __name__ == '__main__':
    get_triangle('binance', log=True)
