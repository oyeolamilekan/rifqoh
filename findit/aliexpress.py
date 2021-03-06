import tempfile
import time
from urllib.request import urlopen, Request

import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string

from .models import Products
# https://www.aliexpress.com/category/100003084/hoodies-sweatshirts/2.html?site=glo&g=y&needQuery=n&tag=

def alii():
    folder = 'aliexpress/'
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    for i in range(1,5):
        time.sleep(0.5)
        html = Request(
            'https://www.aliexpress.com/category/200000764/shoulder-bags/{}.html'.format(
                i), headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        # namelist = bsObj.find('div',{'id':'list-items'})
        namelist = bsObj.findAll('div', {'class': 'item'})
        print()
        for news in namelist:
            product_link = news.find('a', {'class': 'product'})
            if product_link:
                product_link = 'http:' + product_link.attrs['href']
                product_named = news.find('a', {'class': 'product'})
                product_price = news.find('span', {'class', 'value'})
                image = news.find('img', {'class': 'picCore'})
                image = 'http:' + image.get('src', image.get('image-src'))
                product_price = bytes(str(product_price.text), 'UTF-8')
                product_price = product_price.decode('ascii', 'ignore')
                namelst = bytes(str(product_named.text), 'UTF-8')
                namelst = namelst.decode('ascii', 'ignore')
                htl = Request(image, headers=hdr)
                httl = urlopen(htl).read()

            if Products.objects.filter(name=namelst, shop='aliexpress').exists():
                produc = Products.objects.get(name=namelst, shop='aliexpress')
                # Checks the price
                if produc.price != product_price:
                    # produc.old_price = produc.price
                    # produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
                    # Updates the price
                    produc.price = product_price
                    # Saves the price
                    produc.save()
            else:
                request = requests.get(image, stream=True)
                if request.status_code != requests.codes.ok:
                    continue
                randd_ne = get_random_string(length=10)
                file_name = image.split('/')[-1]
                point_finder = file_name.find('.')
                file_name = file_name[:point_finder] + randd_ne
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                lf = ContentFile(httl)
                product = Products(name=namelst, price=product_price, source_url=product_link, shop='aliexpress',
                                   genre='women-bags')
                product.image.save(folder + file_name[:10], lf)

    for i in range(1,5):
        # time.sleep(0.5)
        html = Request(
            'https://www.aliexpress.com/category/660103/makeup/{}.html'.format(
                i), headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        # namelist = bsObj.find('div',{'id':'list-items'})
        namelist = bsObj.findAll('div', {'class': 'item'})
        for news in namelist:
            product_link = news.find('a', {'class': 'product'})
            if product_link:
                product_link = 'http:' + product_link.attrs['href']
                product_named = news.find('a', {'class': 'product'})
                product_price = news.find('span', {'class', 'value'})
                image = news.find('img', {'class': 'picCore'})
                image = 'http:' + image.get('src', image.get('image-src'))
                product_price = bytes(str(product_price.text), 'UTF-8')
                product_price = product_price.decode('ascii', 'ignore')
                namelst = bytes(str(product_named.text), 'UTF-8')
                namelst = namelst.decode('ascii', 'ignore')
                htl = Request(image, headers=hdr)
                httl = urlopen(htl).read()

            if Products.objects.filter(name=namelst, shop='aliexpress').exists():
                produc = Products.objects.get(name=namelst, shop='aliexpress')
                # Checks the price
                if produc.price != product_price:
                    # price_format = re.findall(r'(?P<id>\d+)',product_price)
                    # produc.old_price = product_price
                    # produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
                    # Updates the price
                    produc.price = product_price
                    # Saves the price

                    produc.save()
            else:
                request = requests.get(image, stream=True)
                if request.status_code != requests.codes.ok:
                    continue
                randd_ne = get_random_string(length=10)
                file_name = image.split('/')[-1]
                point_finder = file_name.find('.')
                file_name = file_name[:point_finder] + randd_ne
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                lf = ContentFile(httl)
                product = Products(name=namelst, price=product_price, source_url=product_link, shop='aliexpress',
                                   genre='makeup')
                product.image.save(folder + file_name[:10], lf)

    for i in range(5):
        # time.sleep(0.2)
        html = Request(
            'https://www.aliexpress.com/category/63705/earphones-headphones/{}.html'.format(
                i), headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        # namelist = bsObj.find('div',{'id':'list-items'})
        namelist = bsObj.findAll('li', {'class': 'list-item'})
        for news in namelist:
            product_link = news.find('a', {'class': 'picRind'})
            if product_link:
                product_link = news.find('a', {'class': 'picRind'})
                product_link = product_link.attrs['href']
                product_named = news.find('a', {'class': 'product'})
                product_price = news.find('span', {'class', 'value'})
                image = news.find('img', {'class': 'picCore'})
                product_price = bytes(str(product_price.text), 'UTF-8')
                product_price = product_price.decode('ascii', 'ignore')
                namelst = bytes(str(product_named.text), 'UTF-8')
                namelst = namelst.decode('ascii', 'ignore')
                product_link = 'http:' + product_link
                image = 'http:' + image.get('src', image.get('image-src'))
                htl = Request(image, headers=hdr)
                httl = urlopen(htl).read()

            if Products.objects.filter(name=namelst, shop='aliexpress').exists():
                produc = Products.objects.get(name=namelst, shop='aliexpress')
                # Checks the price
                if produc.price != product_price:
                    # produc.old_price = produc.price
                    # produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
                    # Updates the price
                    produc.price = product_price
                    # Saves the price

                    produc.save()
            else:
                request = requests.get(image, stream=True)
                if request.status_code != requests.codes.ok:
                    continue
                randd_ne = get_random_string(length=10)
                file_name = image.split('/')[-1]
                point_finder = file_name.find('.')
                file_name = file_name[:point_finder] + randd_ne
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                lf = ContentFile(httl)
                product = Products(name=namelst, price=product_price, source_url=product_link, shop='aliexpress',
                                   genre='headphones')
                product.image.save(folder + file_name[:10], lf)


    # for i in range():
    #     # time.sleep(0.2)
    #     html = Request('https://www.aliexpress.com/category/100003084/hoodies-sweatshirts/{}.html'.format(
    #             i), headers=hdr)
    #     htmll = urlopen(html).read()
    #     bsObj = BeautifulSoup(htmll, 'html.parser')
    #     # namelist = bsObj.find('div',{'id':'list-items'})
    #     namelist = bsObj.findAll('li', {'class': 'list-item'})
    #     for news in namelist:
    #         product_link = news.find('a', {'class': 'picRind'})
    #         if product_link:
    #             product_link = news.find('a', {'class': 'picRind'})
    #             product_link = product_link.attrs['href']
    #             product_named = news.find('a', {'class': 'product'})
    #             product_price = news.find('span', {'class', 'value'})
    #             image = news.find('img', {'class': 'picCore'})
    #             product_price = bytes(str(product_price.text), 'UTF-8')
    #             product_price = product_price.decode('ascii', 'ignore')
    #             namelst = bytes(str(product_named.text), 'UTF-8')
    #             namelst = namelst.decode('ascii', 'ignore')
    #             product_link = 'http:' + product_link
    #             image = 'http:' + image.get('src', image.get('image-src'))
    #             htl = Request(image, headers=hdr)
    #             httl = urlopen(htl).read()

    #         if Products.objects.filter(name=namelst, shop='aliexpress').exists():
    #             produc = Products.objects.get(name=namelst, shop='aliexpress')
    #             # Checks the price
    #             if produc.price != product_price:
    #                 # produc.old_price = produc.price
    #                 # produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
    #                 # Updates the price
    #                 produc.price = product_price
    #                 # Saves the price

    #                 produc.save()
    #         else:
    #             request = requests.get(image, stream=True)
    #             if request.status_code != requests.codes.ok:
    #                 continue
    #             randd_ne = get_random_string(length=10)
    #             file_name = image.split('/')[-1]
    #             point_finder = file_name.find('.')
    #             file_name = file_name[:point_finder] + randd_ne
    #             lf = tempfile.NamedTemporaryFile()
    #             for block in request.iter_content(1024 * 8):
    #                 if not block:
    #                     break
    #                 lf.write(block)
    #             lf = ContentFile(httl)
    #             product = Products(name=namelst, price=product_price, source_url=product_link, shop='aliexpress',
    #                                genre='hoodies')
    #             product.image.save(file_name[:10], lf)