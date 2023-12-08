import random

def generate_random_value(min_value=0.1, max_value=0.3):
    random_value = round(random.uniform(min_value, max_value), 3)
    return random_value


# Пример использования
random_result = generate_random_value()
print(random_result)