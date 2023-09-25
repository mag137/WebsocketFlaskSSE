class CryptoQuote:
    def __init__(self, timestamp, trade_id, symbol, ask_data, bid_data):
        self.timestamp = timestamp  # Время последней котировки
        self.trade_id = trade_id  # Идентификатор сделки
        self.symbol = symbol  # Торговая пара
        self.ask_price = ask_data[0]  # Цена аска
        self.ask_volume = ask_data[1]  # Объем аска
        self.bid_price = bid_data[0]  # Цена бида
        self.bid_volume = bid_data[1]  # Объем бида

    def display_info(self):
        print(f"Время последней котировки: {self.timestamp}")
        print(f"Идентификатор сделки: {self.trade_id}")
        print(f"Торговая пара: {self.symbol}")
        print(f"Цена аска: {self.ask_price}")
        print(f"Объем аска: {self.ask_volume}")
        print(f"Цена бида: {self.bid_price}")
        print(f"Объем бида: {self.bid_volume}")

# Пример данных от бинанса
binance_data = ('2023-09-25T19:31:06.084Z', 39018832512, 'BTC/USDT', [26277.12, 5.51757], [26277.11, 9.10171])

# Создаем объект класса CryptoQuote, используя данные от бинанса
quote = CryptoQuote(binance_data[0], binance_data[1], binance_data[2], binance_data[3], binance_data[4])

# Выводим информацию о котировке
quote.display_info()
