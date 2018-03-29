import re
import threading
from .j_crawler import jumia_crawler
from .k_cralwer import konga_crawler
from .y_crawler import yudala
from .aliexpress import alii


def black_rock():
    # Jumia jumia crawler
    jumia_crawler()
    
    # Activates aliexpress crawler
    alii()

    # Activates konga crawler
    konga_crawler()

    # Does the yudala magic
    yudala()

    t = threading.Timer(172800.0, black_rock)
    t.start()


def nairaconv(string):
    price_list = re.findall('\d+\.\d+', string)
    new_price = []
    for price in price_list:
        price = float(price)
        price = price * 360
        price = '{:.2f}'.format(price)
        new_price.append(price)
    if len(new_price) >= 2:
        new_price = tuple(new_price)
        price_field = '%s - %s' % (new_price)
        price_field = ''.join(price_field)
        price_field = price_field.replace('[', '').replace(']', '')
    else:
        price_field = '%s' % (new_price)
        price_field = ''.join(price_field)
        price_field = price_field.replace('[', '').replace(']', '')
    return price_field
