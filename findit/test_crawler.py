import tempfile
from urllib.request import urlopen, Request
import re
import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from .models import Products

def test_cralwer():

    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        for urls in range(1, 3):
            html = Request('https://www.konga.com/playstation-4?page=%s' % urls, headers=hdr)
            htmll = urlopen(html).read()
            bsObj = BeautifulSoup(htmll, 'html.parser')
            product_list = bsObj.findAll('div', {'data-sku': re.compile(r".*")})
            print(product_list)
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
    except Exception as e:
        subject = 'Crawler Error'
        from_email = settings.EMAIL_HOST_USER
        message = 'The following exception occured %s' % e        
        recipient_list = ['johnsonoye34@gmail.com']
        html_message = '<p>Bros there\'s something went wrong : %s </p>'%(e)
        sent_mail = send_mail(
                        subject, 
                        message, 
                        from_email, 
                        recipient_list,  
                        html_message=html_message)