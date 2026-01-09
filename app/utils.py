import random


"""Generate a random short URL string of given length."""
def generate_short_url(length: int = 6) -> str:
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    result = []

    for _ in range(length):
        result.append(random.choice(characters))

    return "".join(result)
