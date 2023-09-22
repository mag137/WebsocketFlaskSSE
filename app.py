from flask import Flask, render_template, Response
import time

app = Flask(__name__)# создание объекта приложения

@app.route('/') # главная страница, маршрут,
def index(): # Этот маршрут возвращает HTML-шаблон index.html при запросе к корневому пути ('/').
    return render_template('index.html')

def generate_time(): # Эта функция будет генерировать текущее время каждую секунду и отправлять его клиенту в формате Server-Sent Events.
    while True:
        current_time = time.strftime('%H:%M:%S')
        yield f"data: {current_time}\n\n"
        time.sleep(1)

@app.route('/stream')
def stream():
    return Response(generate_time(), content_type='text/event-stream')

if __name__ == '__main__':

    app.run(debug=True)
print('Server started...')