import tempfile
from urllib.request import urlopen, Request

import requests
from bs4 import BeautifulSoup
from django.core import files

from .models import Products


def yudala():
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    for urls in range(1, 8):
        html = Request('http://www.yudala.com/phones-and-tablets?p=%s' % urls, headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        bsObj = bsObj.find('ol', {'class': 'product-items'})
        namelist = bsObj.findAll('li', {'class': 'product-item'})
        for news in namelist:
            product_link = news.find('a', {'class': 'product-item-link'})
            # product_link = product_link.attrs['href']
            image = news.find('img', {'class': 'product-image-photo'})
            images = image.attrs['src']
            product_named = product_link.text
            price = news.find('div', {'class': 'price-box'})
            product_price = news.find('span', {'class', 'price'})
            product_price = bytes(str(product_price.text), 'UTF-8')
            product_price = product_price.decode('ascii', 'ignore')
            namelst = bytes(str(product_named), 'UTF-8')
            namelst = namelst.decode('ascii', 'ignore')[:299]
            request = requests.get(images, stream=True)
            print(product_named)
            if Products.objects.filter(name__iexact=namelst, shop='yudala').exists():
                product_count = Products.objects.filter(name__iexact=namelst, shop="yudala").count()

                if product_count >= 2:
                    product_count = Products.objects.filter(name__iexact=namelst, shop="yudala")[1]
                    product_count.delete()

                produc = Products.objects.get(name__iexact=namelst, shop='yudala')
                # Checks the price
                if produc.price != product_price:
                    # produc.old_price = produc.price
                    # produc.old_price_digit = int(produc.price.replace(',', '').replace('\n', '').replace('.00', ''))
                    # Updates the price
                    produc.price = product_price
                    # Saves the price

                    produc.save()
            else:
                if request.status_code != requests.codes.ok:
                    continue
                file_name = 'yudala/' + images.split('/')[-1]
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                product = Products(name=namelst, price=product_price, source_url=product_link.attrs['href'],
                                   shop='yudala', genre='phone')
                product.image.save(file_name[:20], files.File(lf))

    urls_tuple = 'https://www.yudala.com/laptops'
    html = Request(urls_tuple, headers=hdr)
    htmll = urlopen(html).read()
    bsObj = BeautifulSoup(htmll, 'html.parser')
    bsObj = bsObj.find('ol', {'class': 'product-items'})
    namelist = bsObj.findAll('li', {'class': 'product-item'})
    for news in namelist:
        product_link = news.find('a', {'class': 'product-item-link'})
        image = news.find('img', {'class': 'product-image-photo'})
        images = image.attrs['src']
        product_named = product_link.text
        price = news.find('div', {'class': 'price-box'})
        product_price = news.find('span', {'class', 'price'})
        product_price = bytes(str(product_price.text), 'UTF-8')
        product_price = product_price.decode('ascii', 'ignore')
        namelst = bytes(str(product_named), 'UTF-8')
        namelst = namelst.decode('ascii', 'ignore')[:299]
        request = requests.get(images, stream=True)
        if Products.objects.filter(name__iexact=namelst, shop='yudala').exists():
            product_count = Products.objects.filter(name__iexact=namelst, shop="yudala").count()

            if product_count >= 2:
                product_count = Products.objects.filter(name__iexact=namelst, shop="yudala")[1]
                product_count.delete()

            produc = Products.objects.get(name__iexact=namelst, shop='yudala')
            # Checks the price
            if produc.price != product_price:
                # produc.old_price = produc.price
                # produc.old_price_digit = int(produc.price.replace(',', '').replace('\n', '').replace('.00', ''))
                # Updates the price
                produc.price = product_price
                # Saves the price

                produc.save()
        else:
            if request.status_code != requests.codes.ok:
                continue
            file_name = 'yudala/' + images.split('/')[-1]
            lf = tempfile.NamedTemporaryFile()
            for block in request.iter_content(1024 * 8):
                if not block:
                    break
                lf.write(block)
            product = Products(name=namelst, price=product_price, source_url=product_link.attrs['href'], shop='yudala',
                               genre='laptops')
            product.image.save(file_name[:20], files.File(lf))
