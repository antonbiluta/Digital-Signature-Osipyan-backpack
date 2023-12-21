import json
import random


def generate_knapsack_key(size):
    """ Генерирует случайный рюкзак """
    knapsack = [random.randint(1, 10)]
    for _ in range(1, size):
        knapsack.append(knapsack[-1] + random.randint(1, 10))
    return knapsack

def generate_keys():
    """ Генерация публичного и приватного ключей """
    private_key = generate_knapsack_key(8)  # Примерный размер рюкзака
    # Примерный множитель и модуль для публичного ключа
    multiplier = random.randint(10, 20)
    modulus = sum(private_key) + random.randint(1, 10)
    public_key = [x * multiplier % modulus for x in private_key]
    return public_key, private_key, multiplier, modulus

def generate_keys_json():
    public_key, private_key, multiplier, modulus = generate_keys()
    keys = {'public_key': public_key, 'private_key': private_key, 'multiplier': multiplier, 'modulus': modulus}
    return json.dumps(keys)