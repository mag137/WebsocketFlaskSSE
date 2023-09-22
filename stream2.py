import time
import threading
from flask import Flask, render_template, Response

app = Flask(__name__)

# Глобальные переменные для хранения времени в разных форматах
current_time = ""
current_unix_time = 0

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
        current_unix_time = int(time.time())
        time.sleep(1)

# Запускаем потоки
thread_time = threading.Thread(target=update_current_time)
thread_unix_time = threading.Thread(target=update_current_unix_time)

thread_time.start()
thread_unix_time.start()

@app.route('/stream')
def home():
    def generate():
        while True:
            yield f"data: {current_time}\ndata_unix: {current_unix_time}\n\n"
            time.sleep(1)

    return Response(generate(), content_type='text/event-stream')

@app.route('/') # главная страница, маршрут,
def index(): # Этот маршрут возвращает HTML-шаблон index.html при запросе к корневому пути ('/').
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
