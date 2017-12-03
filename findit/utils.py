from .y_crawler import yudala
from .k_cralwer import konga_crawler
from .j_crawler import jumia_crawler
import threading
from .models import Products

def black_rock():
    jumia_crawler()
    konga_crawler()
    yudala()

    threading.Timer(172800.0,black_rock).start()
