import time
import threading
from flask import Flask, render_template, Response
import ccxt.pro
from asyncio import run, gather



app = Flask(__name__)
active_threads = threading.enumerate()
# Глобальные переменные для хранения времени в разных форматах
current_time = ""
current_unix_time = 0
count = 0


async def watch_order_book(exchange, symbol):
    while True:
        try:
            orderbook = await exchange.watch_order_book(symbol)
            datetime = exchange.iso8601(exchange.milliseconds())
            print(datetime, orderbook['nonce'], symbol, orderbook['asks'][0], orderbook['bids'][0])
        except Exception as e:
            print(type(e).__name__, str(e))
            break


async def reload_markets(exchange, delay):
    while True:
        try:
            await exchange.sleep(delay)
            markets = await exchange.load_markets(True)
            datetime = exchange.iso8601(exchange.milliseconds())
            print(datetime, 'Markets reloaded')
        except Exception as e:
            print(type(e).__name__, str(e))
            break
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

thread_time.start()
thread_unix_time.start()

for thread in active_threads:
    print(f"Thread Name: {thread.name}, Thread ID: {thread.ident}, Thread is Daemon: {thread.daemon}")

@app.route('/stream')
def home():
    def generate():
        while True:
            yield f"data: current_time: {current_time}\n\n"
            yield f"data: current_unix_time: {current_unix_time}\n\n"
            time.sleep(1)

    return Response(generate(), content_type='text/event-stream')


@app.route('/') # главная страница, маршрут,
def index(): # Этот маршрут возвращает HTML-шаблон index.html при запросе к корневому пути ('/').
    return render_template('index.html')




if __name__ == '__main__':

    app.run(debug=True)
