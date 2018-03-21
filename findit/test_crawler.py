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
        for urls in range(1, 10):
            html = Request('https://www.jumia.com.ng/womens-dresses/page=%s' % urls, headers=hdr)
            htmll = urlopen(html).read()
            bsObj = BeautifulSoup(htmll, 'html.parser')
            namelist = bsObj.findAll('div', {'data-sku': re.compile(r".*")})
            for news in namelist:
                product_link = news.find('a', {'class': 'link'})
                product_link = product_link.attrs['href']
                image = news.find('img', {'class': 'image'})
                images = image.attrs['data-src']
                product_named = news.find('h2', {'class': 'title'})
                product_price = news.find('span', {'class', 'price'}).find_all('span')
                product_price = product_price[1]
                product_price = bytes(str(product_price.text), 'UTF-8')
                product_price = product_price.decode('ascii', 'ignore')
                namelst = bytes(str(product_named.text), 'UTF-8')
                namelst = namelst.decode('ascii', 'ignore')
                htl = Request(images, headers=hdr)
                httl = urlopen(htl).read()
                namelst = namelst.replace("\n", ' ').replace('\t',' ')
                if Products.objects.filter(name__iexact=namelst,source_url=product_link, shop='jumia').exists():
                    
                    produc = Products.objects.get(name__iexact=namelst,source_url=product_link, shop='jumia')
                    # Checks the price
                    if produc.price != product_price:
                        produc.old_price = produc.price
                        produc.old_price_digit = int(produc.price.replace(',', '').replace('\n', '').replace('.00', ''))
                        # Updates the price
                        produc.price = product_price
                        # Saves the price

                        produc.save()
                else:
                    request = requests.get(images, stream=True)
                    if request.status_code != requests.codes.ok:
                        continue
                    randd_ne = get_random_string(length=10)
                    file_name = images.split('/')[-1]
                    point_finder = file_name.find('.')
                    file_name = 'jumia/' + file_name[:point_finder] + randd_ne
                    lf = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break
                        lf.write(block)
                    lf = ContentFile(httl)
                    product = Products(name=namelst, price=product_price, source_url=product_link,
                                       genre='women-dresses', shop='jumia')
                    product.image.save(file_name[:20], lf)
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