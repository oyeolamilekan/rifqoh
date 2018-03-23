import tempfile
from urllib.request import urlopen, Request

import requests
from bs4 import BeautifulSoup
from django.core import files
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from .models import Products

# https://www.konga.com/playstation-4
def konga_crawler():
    file_storage = 'konga_must_work/'
    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        for urls in range(1, 30):
            html = Request('https://www.konga.com/playstation-4?page=%s' % urls, headers=hdr)
            htmll = urlopen(html).read()
            bsObj = BeautifulSoup(htmll, 'html.parser')
            product_list = bsObj.findAll('div', {'class': 'product-block'})
            for product in product_list:
                product_name = product.find('div', {'class': 'product-name'})
                product_link = 'https://www.konga.com' + product.a.attrs['href']
                images = product.find('img', {'class': 'catalog-product-image'})
                images = images.attrs['src']
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
                namelst = namelst.replace("\n", '').replace('\t','')
                if Products.objects.filter(source_url=product_link, shop='konga').exists():
                    
                    if len(Products.objects.filter(source_url=product_link,shop='konga')) == 2:
                        produc = Products.objects.filter(source_url=product_link,shop='konga')[0]
                        produc.delete()
                    produc = Products.objects.get(source_url=product_link, shop='konga')
                    produc.source_url = product_link
                    produc.save()
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
                    file_name = file_storage + images.split('/')[-1]
                    lf = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break
                        lf.write(block)
                    print(namelst, e_price)
                    product = Products(name=namelst, price=e_price, source_url=product_link,
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
                images = product.find('img', {'class': 'catalog-product-image'})
                images = images.attrs['src']
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
                namelst = namelst.replace("\n", '').replace('\t','')
                if Products.objects.filter(source_url=product_link, shop='konga').exists():
                    if len(Products.objects.filter(source_url=product_link,shop='konga')) == 2:
                        produc = Products.objects.filter(source_url=product_link,shop='konga')[0]
                        produc.delete()
                    produc = Products.objects.get(source_url=product_link, shop='konga')
                    produc.source_url = product_link
                    produc.save()
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
                    file_name = file_storage + images.split('/')[-1]
                    lf = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break
                        lf.write(block)
                    print(namelst, e_price)
                    product = Products(name=namelst, price=e_price, source_url=product_link,
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
                images = product.find('img', {'class': 'catalog-product-image'})
                images = images.attrs['src']
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
                namelst = namelst.replace("\n", '').replace('\t','')
                if Products.objects.filter(source_url=product_link, shop='konga').exists():
                    if len(Products.objects.filter(source_url=product_link,shop='konga')) == 2:
                        produc = Products.objects.filter(source_url=product_link,shop='konga')[0]
                        produc.delete()
                    
                    produc = Products.objects.get(source_url=product_link, shop='konga')
                    produc.source_url = product_link
                    produc.save()
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
                    file_name = file_storage + images.split('/')[-1]
                    lf = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break
                        lf.write(block)
                    print(namelst, e_price)
                    product = Products(name=namelst, price=e_price, source_url=product_link,
                                       genre='televisions', shop='konga')
                    product.image.save(file_name[:20], files.File(lf))

        for urls in range(1, 50):
            
            html = Request('https://www.konga.com/mobile-phones?page=%s' % urls, headers=hdr)
            htmll = urlopen(html).read()
            bsObj = BeautifulSoup(htmll, 'html.parser')
            product_list = bsObj.findAll('div', {'class': 'product-block'})
            for product in product_list:
                product_name = product.find('div', {'class': 'product-name'})
                product_link = 'https://www.konga.com' + product.a.attrs['href']
                images = product.find('img', {'class': 'catalog-product-image'})
                images = images.attrs['src']
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
                namelst = namelst.replace("\n", '').replace('\t','')
                if Products.objects.filter(source_url=product_link, shop='konga').exists():
                    if len(Products.objects.filter(source_url=product_link,shop='konga')) == 2:
                        produc = Products.objects.filter(source_url=product_link,shop='konga')[0]
                        produc.delete()

                    produc = Products.objects.get(source_url=product_link, shop='konga')
                    produc.source_url = product_link
                    produc.save()
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
                    file_name = file_storage + images.split('/')[-1]
                    lf = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break
                        lf.write(block)
                    product = Products(name=namelst, price=e_price, source_url=product_link, shop='konga',genre='phone')
                    product.image.save(file_name[:20], files.File(lf))

        for urls in range(1, 60):
            html = Request('https://www.konga.com/laptops-5230?page=%s' % urls, headers=hdr)
            htmll = urlopen(html).read()
            bsObj = BeautifulSoup(htmll, 'html.parser')
            product_list = bsObj.findAll('div', {'class': 'product-block'})
            for product in product_list:
                product_name = product.find('div', {'class': 'product-name'})
                product_link = 'https://www.konga.com' + product.a.attrs['href']
                images = product.find('img', {'class': 'catalog-product-image'})
                images = images.attrs['src']
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
                namelst = namelst.replace("\n", '').replace('\t','')
                if Products.objects.filter(source_url=product_link, shop='konga').exists():
                    if len(Products.objects.filter(source_url=product_link,shop='konga')) == 2:
                        produc = Products.objects.filter(source_url=product_link,shop='konga')[0]
                        produc.delete()
                    produc = Products.objects.get(source_url=product_link, shop='konga')
                    produc.source_url = product_link
                    produc.save()
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
                    file_name = file_storage + images.split('/')[-1]
                    lf = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break
                        lf.write(block)
                    product = Products(name=namelst, price=e_price,
                                       source_url=product_link, shop='konga', genre='laptops')
                    product.image.save(file_name[:20], files.File(lf))

        html = Request('https://www.konga.com/catalogsearch/result/?category_id=5294&aggregated_brand=Apple', headers=hdr)
        htmll = urlopen(html).read()
        bsObj = BeautifulSoup(htmll, 'html.parser')
        product_list = bsObj.findAll('div', {'class': 'product-block'})
        for product in product_list:
            product_name = product.find('div', {'class': 'product-name'})
            product_link = 'https://www.konga.com' + product.a.attrs['href']
            images = product.find('img', {'class': 'catalog-product-image'})
            images = images.attrs['src']
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
            namelst = namelst.replace("\n", '').replace('\t','')
            if Products.objects.filter(source_url=product_link, shop='konga').exists():
                if len(Products.objects.filter(source_url=product_link,shop='konga')) == 2:
                    produc = Products.objects.filter(source_url=product_link,shop='konga')[0]
                    produc.delete()
                produc = Products.objects.get(source_url=product_link, shop='konga')
                produc.source_url = product_link
                produc.save()
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
                file_name = file_storage + images.split('/')[-1]
                lf = tempfile.NamedTemporaryFile()
                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                print(namelst, e_price)
                product = Products(name=namelst, price=e_price, source_url=product_link, shop='konga')
                product.image.save(file_name[:20], files.File(lf))

        for urls in range(1, 60):
            html = Request('https://www.konga.com/mens-watches?page=%s' % urls, headers=hdr)
            htmll = urlopen(html).read()
            bsObj = BeautifulSoup(htmll, 'html.parser')
            product_list = bsObj.findAll('div', {'class': 'product-block'})
            for product in product_list:
                product_name = product.find('div', {'class': 'product-name'})
                product_link = 'https://www.konga.com' + product.a.attrs['href']
                images = product.find('img', {'class': 'catalog-product-image'})
                images = images.attrs['src']
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
                namelst = namelst.replace("\n", '').replace('\t','')
                if Products.objects.filter(source_url=product_link, shop='konga',
                                           genre='men-watches').exists():
                    if Products.objects.filter(source_url=product_link,shop='konga').count() == 2:
                        produc = Products.objects.filter(source_url=product_link,shop='konga')[0]
                        produc.delete()

                    produc = Products.objects.get(source_url=product_link, shop='konga')
                    produc.source_url = product_link
                    produc.save()
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
                    file_name = file_storage + images.split('/')[-1]
                    lf = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break
                        lf.write(block)
                    product = Products(name=namelst, price=e_price, source_url=product_link, shop='konga',
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
                images = product.find('img', {'class': 'catalog-product-image'})
                images = images.attrs['src']
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
                namelst = namelst.replace("\n", '').replace('\t','')
                if Products.objects.filter(source_url=product_link, shop='konga',
                                           genre='women-watches').exists():
                    if len(Products.objects.filter(source_url=product_link,shop='konga')) == 2:
                        produc = Products.objects.filter(source_url=product_link,shop='konga')[0]
                        produc.delete()
                    produc = Products.objects.get(source_url=product_link, shop='konga')
                    produc.source_url = product_link
                    produc.save()
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
                    file_name = file_storage + images.split('/')[-1]
                    lf = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break
                        lf.write(block)
                    product = Products(name=namelst, price=e_price, source_url=product_link, shop='konga',
                                       genre='women-watches')
                    product.image.save(file_name[:20], files.File(lf))
    
    except Exception as e:
        subject = 'Crawler Error'
        from_email = settings.EMAIL_HOST_USER
        message = 'The following exception occured %s' % e        
        recipient_list = ['johnsonoye34@gmail.com']
        html_message = '<p>Bros there\'s something went wrong : %s konga Crawler : %s - %s</p>'%(e, urls,product_link)
        sent_mail = send_mail(
                        subject, 
                        message, 
                        from_email, 
                        recipient_list,  
                        html_message=html_message)
