from string import ascii_uppercase, digits
import random

arr = list(ascii_uppercase + digits)


def get_random_symbol(arr):
    symbol = random.choice(arr)
    return symbol


def get_random_username():
    username = []
    print(username)

    while len(username) < 10:
        username.append(get_random_symbol(arr))
        print(username, "в цикле")

    return "".join(username)
