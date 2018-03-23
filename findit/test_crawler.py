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
        for urls in range(1,60):
        # hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        #        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #        'Accept-Encoding': 'none',
        #        'Accept-Language': 'en-US,en;q=0.8',
        #        'Connection': 'keep-alive'}
            html = Request('https://www.konga.com/womens-watches?page=%s'%urls,headers=hdr)
            htmll = urlopen(html).read()
            bsObj = BeautifulSoup(htmll,'html.parser')
            product_list = bsObj.findAll('div',{'class':'product-block'})
            for product in product_list:
                product_name = product.find('div',{'class':'product-name'})
                product_link = 'https://www.konga.com'+product.a.attrs['href']
                images = product.img.attrs['src']
                request = requests.get(images, stream=True)
                if product.find('div',{'class':'special-price'}) != None:
                    # If it does exist it find the price
                    price = product.find('div',{'class':'special-price'})
                else:
                    # If does not exist it finds the original price
                    price = product.find('div',{'class':'original-price'})
                e_price = bytes(str(price.text),'UTF-8')
                e_price = e_price.decode('ascii','ignore')
                namelst = bytes(str(product_name.text), 'UTF-8')
                namelst = namelst.decode('ascii','ignore')
                print(namelst,e_price)
                if Products.objects.filter(name=namelst,shop='konga',genre='women-watches').exists():
                    
                    produc = Products.objects.get(name=namelst,shop='konga',genre='women-watches')
                    # Checks the price
                    if produc.price != e_price:
                        produc.old_price = produc.price
                        produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
                        # Updates the price
                        produc.price = e_price
                        # Saves the price
                        
                        produc.save()
                else:
                    if request.status_code != requests.codes.ok:
                        continue
                    file_name = images.split('/')[-1]
                    lf = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024*8):
                        if not block:
                            break
                        lf.write(block)
                    product = Products(name=namelst,price=e_price,source_url=product_link,shop='konga',genre='women-watches')
                    product.image.save(file_name[:20],files.File(lf))
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