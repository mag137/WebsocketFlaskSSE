


def calc_delta(triangle_dict, get_triangle_in_pair_dict, price_dict, input_delta_calc_data_queue, output_delta_calc_data_queue):
    '''Инициализируем выходные словари'''
    delta_direct = {} # Словарь с дельтами для каждого треугольника
    delta_reverse = {}
    best_delta_dict_direct = {}
    best_delta_dict_reverse = {}
    for i in range(6):  # Инициализируем словари с наилучшими дельтами из всех треугольников
        best_delta_dict_direct[f'{i}'] = 0
        best_delta_dict_reverse[f'{i}'] = 0
    while True:
        try:
            pair, ask, bid = input_delta_calc_data_queue.get() # Получаем пару, по которой изменилась цена из очереди
            price_dict[pair] = {'ask': ask, 'bid': bid, 'volume_ask': None, 'volume_bid': None}

            for tri in get_triangle_in_pair_dict[pair]: # Проходим по всем треугольникам, в которых есть эта пара, чтобы пересчитать дельты
                pair_A = triangle_dict[tri]['pairA']
                pair_B = triangle_dict[tri]['pairB']
                pair_C = triangle_dict[tri]['pairC']

                if price_dict[pair_A]['ask'] is not None \
                        and price_dict[pair_A]['bid'] is not None \
                        and price_dict[pair_B]['ask'] is not None \
                        and price_dict[pair_B]['bid'] is not None \
                        and price_dict[pair_C]['ask'] is not None \
                        and price_dict[pair_C]['bid'] is not None:
                    ask_a = price_dict[pair_A]['ask']
                    ask_b = price_dict[pair_B]['ask']
                    ask_c = price_dict[pair_C]['ask']
                    bid_a = price_dict[pair_A]['bid']
                    bid_b = price_dict[pair_B]['bid']
                    bid_c = price_dict[pair_C]['bid']
                    '''Добавляем в словарь дельт вычисленнее значения'''
                    delta_direct[tri] = bid_a * bid_b / ask_c
                    delta_reverse[tri] = bid_c / (ask_a * ask_b)

                    '''Формируем словарь с 5-ю наибольшими дельтами, записываем 6-м последним значением свежую дельту'''
                    best_delta_dict_direct['6'] = {'Triangle_direct': tri, 'delta': delta_direct[tri]}
                    best_delta_dict_reverse['6'] = {'Triangle_reverse': tri, 'delta': delta_reverse[tri]}

                    for i in range(5, 0, -1):
                        '''Если новая пришедшая дельта больше существующей, то заменяем ее'''
                        if best_delta_dict_direct[f'{i+1}']['delta'] > best_delta_dict_direct[f'{i}']['delta']:
                            '''Меняем местами существующую и новую пришедшую дельту на данной позиции'''
                            best_delta_dict_direct[f'{i}'], best_delta_dict_direct[f'{i+1}'] = best_delta_dict_direct[f'{i+1}'], best_delta_dict_direct[f'{i}']
                        else:
                            break

                    for i in range(5, 0, -1):
                        '''Если новая пришедшая дельта больше существующей, то заменяем ее'''
                        if best_delta_dict_reverse[f'{i+1}']['delta'] > best_delta_dict_reverse[f'{i}']['delta']:
                            '''Меняем местами существующую и новую пришедшую дельту на данной позиции'''
                            best_delta_dict_reverse[f'{i}'], best_delta_dict_reverse[f'{i+1}'] = best_delta_dict_reverse[f'{i+1}'], best_delta_dict_reverse[f'{i}']
                        else:
                            break

                output_delta_calc_data_queue.put((tri, best_delta_dict_direct, best_delta_dict_reverse))
        except Exception as e:
            print(f"Произошла ошибка: {e}")
    return