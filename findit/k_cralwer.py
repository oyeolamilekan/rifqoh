import tempfile
from urllib.request import urlopen, Request

import requests
from bs4 import BeautifulSoup
from django.core import files

from .models import Products

# https://www.konga.com/playstation-4
def konga_crawler():
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
    for urls in range(1, 30):
        html = Request('https://www.konga.com/playstation-4?page=%s' % urls, headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        product_list = bsObj.findAll('div', {'class': 'product-block'})
        for product in product_list:
            product_name = product.find('div', {'class': 'product-name'})
            product_link = 'https://www.konga.com' + product.a.attrs['href']
            images = product.img.attrs['src']
            request = requests.get(images, stream=True)
            if product.find('div', {'class': 'special-price'}) != None:
                # If it does exist it find the price
                price = product.find('div', {'class': 'special-price'})
            else:
                # If does not exist it finds the original price
                price = product.find('div', {'class': 'original-price'})
            e_price = bytes(str(price.text), 'UTF-8')
            e_price = e_price.decode('ascii', 'ignore')
            namelst = bytes(str(product_name.text), 'UTF-8')
            namelst = namelst.decode('ascii', 'ignore')
            if Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga').exists():
                product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga").count()

                if product_count >= 2:
                    product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga")[1]
                    product_count.delete()

                produc = Products.objects.get(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga')
                # Checks the price
                if produc.price != e_price:
                    produc.old_price = produc.price
                    produc.old_price_digit = int(produc.price.replace(',', '').replace('\n', '').replace('.00', ''))
                    # Updates the price
                    produc.price = e_price
                    # Saves the price

                    produc.save()
            else:
                if request.status_code != requests.codes.ok:
                    continue
                file_name = 'konga/' + images.split('/')[-1]
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                print(namelst, e_price)
                product = Products(name=namelst.replace("\n", ' ').replace('\t',' '), price=e_price, source_url=product_link,
                                   genre='televisions', shop='konga')
                product.image.save(file_name[:20], files.File(lf))

    for urls in range(1, 60):
        
        html = Request('https://www.konga.com/mens-shirts?page=%s' % urls, headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        product_list = bsObj.findAll('div', {'class': 'product-block'})
        for product in product_list:
            product_name = product.find('div', {'class': 'product-name'})
            product_link = 'https://www.konga.com' + product.a.attrs['href']
            images = product.img.attrs['src']
            request = requests.get(images, stream=True)
            if product.find('div', {'class': 'special-price'}) != None:
                # If it does exist it find the price
                price = product.find('div', {'class': 'special-price'})
            else:
                # If does not exist it finds the original price
                price = product.find('div', {'class': 'original-price'})
            e_price = bytes(str(price.text), 'UTF-8')
            e_price = e_price.decode('ascii', 'ignore')
            namelst = bytes(str(product_name.text), 'UTF-8')
            namelst = namelst.decode('ascii', 'ignore')
            if Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga').exists():
                product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga").count()

                if product_count >= 2:
                    product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga")[1]
                    product_count.delete()

                produc = Products.objects.get(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga')
                # Checks the price
                if produc.price != e_price:
                    produc.old_price = produc.price
                    produc.old_price_digit = int(produc.price.replace(',', '').replace('\n', '').replace('.00', ''))
                    # Updates the price
                    produc.price = e_price
                    # Saves the price

                    produc.save()
            else:
                if request.status_code != requests.codes.ok:
                    continue
                file_name = 'konga/' + images.split('/')[-1]
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                print(namelst, e_price)
                product = Products(name=namelst.replace("\n", ' ').replace('\t',' '), price=e_price, source_url=product_link,
                                   genre='shirts', shop='konga')
                product.image.save(file_name[:20], files.File(lf))

    for urls in range(1, 60):
        html = Request('https://www.konga.com/televisions?page=%s' % urls, headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        product_list = bsObj.findAll('div', {'class': 'product-block'})
        for product in product_list:
            product_name = product.find('div', {'class': 'product-name'})
            product_link = 'https://www.konga.com' + product.a.attrs['href']
            images = product.img.attrs['src']
            request = requests.get(images, stream=True)
            if product.find('div', {'class': 'special-price'}) != None:
                # If it does exist it find the price
                price = product.find('div', {'class': 'special-price'})
            else:
                # If does not exist it finds the original price
                price = product.find('div', {'class': 'original-price'})
            e_price = bytes(str(price.text), 'UTF-8')
            e_price = e_price.decode('ascii', 'ignore')
            namelst = bytes(str(product_name.text), 'UTF-8')
            namelst = namelst.decode('ascii', 'ignore')
            if Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga').exists():
                product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga").count()

                if product_count >= 2:
                    product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga")[1]
                    product_count.delete()

                produc = Products.objects.get(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga')
                # Checks the price
                if produc.price != e_price:
                    produc.old_price = produc.price
                    produc.old_price_digit = int(produc.price.replace(',', '').replace('\n', '').replace('.00', ''))
                    # Updates the price
                    produc.price = e_price
                    # Saves the price

                    produc.save()
            else:
                if request.status_code != requests.codes.ok:
                    continue
                file_name = 'konga/' + images.split('/')[-1]
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                print(namelst, e_price)
                product = Products(name=namelst.replace("\n", ' ').replace('\t',' '), price=e_price, source_url=product_link,
                                   genre='televisions', shop='konga')
                product.image.save(file_name[:20], files.File(lf))

    for urls in range(1, 60):
        
        html = Request('https://www.konga.com/mobile-phones?page=%s' % urls, headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        product_list = bsObj.findAll('div', {'class': 'product-block'})
        for product in product_list:
            product_name = product.find('div', {'class': 'product-name'})
            product_link = 'https://www.konga.com' + product.a.attrs['href']
            images = product.img.attrs['src']
            request = requests.get(images, stream=True)
            if product.find('div', {'class': 'special-price'}) != None:
                # If it does exist it find the price
                price = product.find('div', {'class': 'special-price'})
            else:
                # If does not exist it finds the original price
                price = product.find('div', {'class': 'original-price'})
            e_price = bytes(str(price.text), 'UTF-8')
            e_price = e_price.decode('ascii', 'ignore')
            namelst = bytes(str(product_name.text), 'UTF-8')
            namelst = namelst.decode('ascii', 'ignore')
            if Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga').exists():
                product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga").count()

                if product_count >= 2:
                    product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga")[1]
                    product_count.delete()

                produc = Products.objects.get(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga')
                # Checks the price
                if produc.price != e_price:
                    produc.old_price = produc.price
                    produc.old_price_digit = int(produc.price.replace(',', '').replace('\n', '').replace('.00', ''))
                    # Updates the price
                    produc.price = e_price
                    # Saves the price

                    produc.save()
            else:
                if request.status_code != requests.codes.ok:
                    continue
                file_name = 'konga/' + images.split('/')[-1]
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                product = Products(name=namelst.replace("\n", ' ').replace('\t',' '), price=e_price, source_url=product_link, shop='konga',genre='phone')
                product.image.save(file_name[:20], files.File(lf))

    for urls in range(1, 60):
        html = Request('https://www.konga.com/laptops-5230?page=%s' % urls, headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        product_list = bsObj.findAll('div', {'class': 'product-block'})
        for product in product_list:
            product_name = product.find('div', {'class': 'product-name'})
            product_link = 'https://www.konga.com' + product.a.attrs['href']
            images = product.img.attrs['src']
            request = requests.get(images, stream=True)
            if product.find('div', {'class': 'special-price'}) != None:
                # If it does exist it find the price
                price = product.find('div', {'class': 'special-price'})
            else:
                # If does not exist it finds the original price
                price = product.find('div', {'class': 'original-price'})
            e_price = bytes(str(price.text), 'UTF-8')
            e_price = e_price.decode('ascii', 'ignore')
            namelst = bytes(str(product_name.text), 'UTF-8')
            namelst = namelst.decode('ascii', 'ignore')
            if Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga').exists():
                product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga").count()

                if product_count >= 2:
                    product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga")[1]
                    product_count.delete()
                produc = Products.objects.get(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga')
                # Checks the price
                if produc.price != e_price:
                    produc.old_price = produc.price
                    produc.old_price_digit = int(produc.price.replace(',', '').replace('\n', '').replace('.00', ''))
                    # Updates the price
                    produc.price = e_price
                    # Saves the price

                    produc.save()
            else:
                if request.status_code != requests.codes.ok:
                    continue
                file_name = 'konga/' + images.split('/')[-1]
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                product = Products(name=namelst.replace("\n", ' ').replace('\t',' '), price=e_price,
                                   source_url=product_link, shop='konga', genre='laptops')
                product.image.save(file_name[:20], files.File(lf))

    html = Request('https://www.konga.com/catalogsearch/result/?category_id=5294&aggregated_brand=Apple', headers=hdr)
    htmll = urlopen(html).read()
    bsObj = BeautifulSoup(htmll, 'html.parser')
    product_list = bsObj.findAll('div', {'class': 'product-block'})
    for product in product_list:
        product_name = product.find('div', {'class': 'product-name'})
        product_link = 'https://www.konga.com' + product.a.attrs['href']
        images = product.img.attrs['src']
        request = requests.get(images, stream=True)
        if product.find('div', {'class': 'special-price'}) != None:
            # If it does exist it find the price
            price = product.find('div', {'class': 'special-price'})
        else:
            # If does not exist it finds the original price
            price = product.find('div', {'class': 'original-price'})
        e_price = bytes(str(price.text), 'UTF-8')
        e_price = e_price.decode('ascii', 'ignore')
        namelst = bytes(str(product_name.text), 'UTF-8')
        namelst = namelst.decode('ascii', 'ignore')
        if Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga').exists():
            product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga").count()

            if product_count >= 2:
                product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga")[1]
                product_count.delete()
            produc = Products.objects.get(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga')
            # Checks the price
            if produc.price != e_price:
                produc.old_price = produc.price
                produc.old_price_digit = int(produc.price.replace(',', '').replace('\n', '').replace('.00', ''))
                # Updates the price
                produc.price = e_price
                # Saves the price

                produc.save()
        else:
            if request.status_code != requests.codes.ok:
                continue
            file_name = 'konga/' + images.split('/')[-1]
            lf = tempfile.NamedTemporaryFile()
            for block in request.iter_content(1024 * 8):
                if not block:
                    break
                lf.write(block)
            print(namelst, e_price)
            product = Products(name=namelst.replace("\n", ' ').replace('\t',' '), price=e_price, source_url=product_link, shop='konga')
            product.image.save(file_name[:20], files.File(lf))

    for urls in range(1, 60):
        html = Request('https://www.konga.com/mens-watches?page=%s' % urls, headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        product_list = bsObj.findAll('div', {'class': 'product-block'})
        for product in product_list:
            product_name = product.find('div', {'class': 'product-name'})
            product_link = 'https://www.konga.com' + product.a.attrs['href']
            images = product.img.attrs['src']
            request = requests.get(images, stream=True)
            if product.find('div', {'class': 'special-price'}) != None:
                # If it does exist it find the price
                price = product.find('div', {'class': 'special-price'})
            else:
                # If does not exist it finds the original price
                price = product.find('div', {'class': 'original-price'})
            e_price = bytes(str(price.text), 'UTF-8')
            e_price = e_price.decode('ascii', 'ignore')
            namelst = bytes(str(product_name.text), 'UTF-8')
            namelst = namelst.decode('ascii', 'ignore')
            print(namelst, e_price)
            if Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga',
                                       genre='men-watches').exists():
                product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga").count()

                if product_count >= 2:
                    product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga")[1]
                    product_count.delete()

                produc = Products.objects.get(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga', genre='men-watches')
                # Checks the price
                if produc.price != e_price:
                    produc.old_price = produc.price
                    produc.old_price_digit = int(produc.price.replace(',', '').replace('\n', '').replace('.00', ''))
                    # Updates the price
                    produc.price = e_price
                    # Saves the price

                    produc.save()
            else:
                if request.status_code != requests.codes.ok:
                    continue
                file_name = 'konga/' + images.split('/')[-1]
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                product = Products(name=namelst.replace("\n", ' ').replace('\t',' '), price=e_price, source_url=product_link, shop='konga',
                                   genre='men-watches')
                product.image.save(file_name[:20], files.File(lf))

    for urls in range(1, 60):
        html = Request('https://www.konga.com/womens-watches?page=%s' % urls, headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        product_list = bsObj.findAll('div', {'class': 'product-block'})
        for product in product_list:
            product_name = product.find('div', {'class': 'product-name'})
            product_link = 'https://www.konga.com' + product.a.attrs['href']
            images = product.img.attrs['src']
            request = requests.get(images, stream=True)
            if product.find('div', {'class': 'special-price'}) != None:
                # If it does exist it find the price
                price = product.find('div', {'class': 'special-price'})
            else:
                # If does not exist it finds the original price
                price = product.find('div', {'class': 'original-price'})
            e_price = bytes(str(price.text), 'UTF-8')
            e_price = e_price.decode('ascii', 'ignore')
            namelst = bytes(str(product_name.text), 'UTF-8')
            namelst = namelst.decode('ascii', 'ignore')
            print(namelst, e_price)
            if Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga',
                                       genre='women-watches').exists():
                product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga").count()

                if product_count >= 2:
                    product_count = Products.objects.filter(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop="konga")[1]
                    product_count.delete()

                produc = Products.objects.get(name__iexact=namelst.replace("\n", ' ').replace('\t',' '), shop='konga',
                                              genre='women-watches')
                # Checks the price
                if produc.price != e_price:
                    produc.old_price = produc.price
                    produc.old_price_digit = int(produc.price.replace(',', '').replace('\n', '').replace('.00', ''))
                    # Updates the price
                    produc.price = e_price
                    # Saves the price

                    produc.save()
            else:
                if request.status_code != requests.codes.ok:
                    continue
                file_name = 'konga/' + images.split('/')[-1]
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                product = Products(name=namelst.replace("\n", ' ').replace('\t',' '), price=e_price, source_url=product_link, shop='konga',
                                   genre='women-watches')
                product.image.save(file_name[:20], files.File(lf))
