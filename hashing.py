import hashlib
import logging
from setting import SETTING

def check_hash(card_center: int, card_begin: int) -> int:
    """ Функция проверки на совпадение хэша
    """

    logging.info("Проверка хеша")
    card_number = str(card_begin) + str(card_center) + SETTING['last_digits']
    card_hash = hashlib.sha224(card_number.encode()).hexdigest()
    if SETTING['hash'] == card_hash:
        return card_number
    return False


def algorithm_luna(number: str) -> bool:
    """функция, которая проверяет номер карты используя алгоритм Луна
    """
    check = 7
    all_number = list(map(int, number))
    all_number = all_number[::-1]
    for i, num in enumerate(all_number):
        if i % 2 == 0:
            tmp = num*2
            if tmp > 9:
                tmp -= 9
            all_number[i] = tmp
    total_sum = sum(all_number)
    rem = total_sum % 10
    if rem != 0:
        check_sum = 10 - rem
    else:
        check_sum = 0
    return True if check_sum == check else False
