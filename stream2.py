import ccxt.pro
import time
import threading
from flask import Flask, render_template, Response
import asyncio
# import GetPrice

DataList = ["Нет связи с биржей"]

print('Server started...')
app = Flask(__name__)
active_threads = threading.enumerate()
# Глобальные переменные для хранения времени в разных форматах
current_time = ""
current_unix_time = 0
count = 0




# Функция watch_order_book является асинхронной и используется для отслеживания стакана ордеров на бирже.
async def watch_order_book(exchange = ccxt.pro.binance(), symbol = 'BTC/USDT'):
    # Бесконечный цикл
    while True:
        try:
            global DataList
            # Подписка
            # вызывает метод watch_order_book у объекта exchange, который отслеживает стакан ордеров для заданного symbol
            # ожидает появления новых данных от биржи, без блокировки.
            orderbook = await exchange.watch_order_book(symbol)
            # получает текущую дату и время с использованием метода iso8601 и milliseconds объекта exchange.
            datetime = exchange.iso8601(exchange.milliseconds())
            DataList = (datetime, orderbook['nonce'], symbol, orderbook['asks'][0], orderbook['bids'][0])
            print(DataList)
            # print("event")
        except Exception as e:
            print(type(e).__name__, str(e))
            break

def run_async_function():
    # Создаем новый цикл asyncio для потока
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Запускаем асинхронную функцию
    loop.run_until_complete(watch_order_book())
    # Завершаем асинхронную функцию
    loop.close()


# Функция, которая будет выполняться в первом потоке и обновлять current_time
def update_current_time():
    global current_time
    while True:
        current_time = time.strftime("%H:%M:%S")
        time.sleep(1)


# Функция, которая будет выполняться во втором потоке и обновлять current_unix_time
def update_current_unix_time():
    global current_unix_time
    while True:
        global count
        count += 1
        current_unix_time = int(time.time())
        time.sleep(1)

# Запускаем потоки
thread_time = threading.Thread(target=update_current_time)
thread_unix_time = threading.Thread(target=update_current_unix_time)
thread_price = threading.Thread(target=run_async_function)



thread_time.start()
thread_unix_time.start()
thread_price.start()

for thread in active_threads:
    print(f"Thread Name: {thread.name}, Thread ID: {thread.ident}, Thread is Daemon: {thread.daemon}")

@app.route('/stream')
def home():
    def generate():
        while True:
            yield f"data: current_time: {current_time}\n\n"
            yield f"data: current_unix_time: {current_unix_time}\n\n"
            yield f"data: BTC: {DataList}\n\n"
            time.sleep(0.1)

    return Response(generate(), content_type='text/event-stream')


@app.route('/') # главная страница, маршрут,
def index(): # Этот маршрут возвращает HTML-шаблон index.html при запросе к корневому пути ('/').
    return render_template('index.html')




if __name__ == '__main__':

    app.run(debug=True)
