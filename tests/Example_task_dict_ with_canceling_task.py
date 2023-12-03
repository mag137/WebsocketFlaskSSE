import asyncio

async def my_task(text):
    c = 0
    try:
        while True:
            c += 1
            print("My task is running", text, c)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("My task is cancelled", text)
        # Пропустите возбуждение исключения, чтобы избежать KeyboardInterrupt
        pass

async def main():
    tasks = {
        "task1": asyncio.create_task(my_task("task1")),
        "task2": asyncio.create_task(my_task("task2")),
        "task3": asyncio.create_task(my_task("task3"))
    }

    # Для прерывания выполнения конкретной задачи
    task_to_cancel = tasks["task2"]
    task_to_cancel.cancel()

    # Вывести задачи перед ожиданием завершения
    print(asyncio.all_tasks())

    try:
        # Для ожидания завершения всех задач
        await asyncio.gather(*tasks.values(), return_exceptions=True)
    except asyncio.CancelledError:
        # Пропустите возбуждение исключения, чтобы избежать проблемы с KeyboardInterrupt
        pass

    print('Завершение программы')

# Запуск основной асинхронной функции
asyncio.run(main())
