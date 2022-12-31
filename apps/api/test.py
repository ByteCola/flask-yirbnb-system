import datetime
import random


def gen_order_no():
    base_code = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(100,999))

    print(base_code)
    oreder_list = []
    count = 1
    while True:
        if count > 10:
            break
        count_str = str(count).zfill(8)
        oreder_list.append(base_code + count_str)
        count += 1
    return oreder_list


print(gen_order_no())
