import hashlib
import logging
import multiprocessing as mp

SETTING = {
    'hash': 'e5c92fb926ffc9976ad06b46cc7eb656158f07b6e41a1666e005c9cd',
    'begin_digits': ["423078", '427401', '427414', '427415', '427421', '427423', '427424','427429', '427434','427435','427437','427443','427447','427448','427457','427458','427464','427465','427471','427473','442198','475794','479583','479586','481778','481781','481782','485463','489798','427601','427901', '466765','467455'],
    'last_digits': '1217',
}

def check_hash(card_number: str) -> bool:
    """ Функция проверки на совпадение хэша
    """
    logging.info("Проверка хеша")
    card_hash = hashlib.sha224(card_number.encode()).hexdigest()
    if SETTING['hash'] == card_hash:
        return True
    return False

def algorithm_luna(number: int) -> bool:
    """функция, которая проверяет номер карты используя алгоритм Луна

    Args:
        number (int): номер

    Returns:
        bool: соответствует/не соответствует
    """
    number = str(number)
 #   if len(number) != 6:
  #      return False
    check = 7
    all_number = [int(i) for i in SETTING['begin_digits']] + [int(i) for i in number] + [int(i) for i in SETTING['last_digits']]
   # all_number = all_number[::-1]
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
    return number if check_sum == check else False