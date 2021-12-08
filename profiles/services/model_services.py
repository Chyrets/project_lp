import random
import string


def rand_slug() -> str:
    """Создание случайной строки для поля slug"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))