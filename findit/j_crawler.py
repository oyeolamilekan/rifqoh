from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
import re
import requests
import tempfile
from .models import Products
from django.core import files
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

folder = 'jumia/'
def jumia_crawler():
	# jumia_phones()
	# jumia_laptops()
	# jumia_wemen_dresses()
	jumia_tvs()
	# jumia_men_watches()
	# jumia_women_watches()
	# jumia_shirts()
	# jumia_gaming()

def jumia_gaming():
	try:
		for urls in range(1,15):
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			       'Accept-Encoding': 'none',
			       'Accept-Language': 'en-US,en;q=0.8',
			       'Connection': 'keep-alive'}
			html = Request('https://www.jumia.com.ng/playstation4-consoles/?page=%s'%urls,headers=hdr)
			htmll = urlopen(html).read()
			bsObj = BeautifulSoup(htmll,'html.parser')
			namelist = bsObj.findAll('div',{'class':'-gallery'})
			for news in namelist:
				product_link = news.find('a',{'class':'link'})
				if product_link:
					product_link = product_link.attrs['href']
					image = news.find('img',{'class':'image'})
					images = image.attrs['data-src']
					product_named = news.find('h2',{'class':'title'})
					product_price = news.find('span', {'class','price'}).find_all('span')
					product_price = product_price[1]
					product_price = bytes(str(product_price.text),'UTF-8')
					product_price = product_price.decode('ascii','ignore')
					namelst = bytes(str(product_named.text), 'UTF-8')
					namelst = namelst.decode('ascii','ignore').replace('\n','').replace('\t','')
					namelst = str(namelst)
					htl = Request(images,headers=hdr)
					httl = urlopen(htl).read()
					if Products.objects.filter(name=namelst,shop='jumia').exists():
						produc = Products.objects.get(name=namelst,shop='jumia')
						# Checks the price
						if produc.price != product_price:
							print(namelst,product_price,'under')
							produc.old_price = produc.price
							produc.source_url = product_link
							produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
							# Updates the price
							produc.price = product_price
							# Saves the price
							
							produc.save()
					else:
						request = requests.get(images, stream=True)
						if request.status_code != requests.codes.ok:
							continue
						randd_ne = get_random_string(length=10)
						file_name = folder + images.split('/')[-1]
						point_finder = file_name.find('.')
						file_name = file_name[:point_finder] + randd_ne
						lf = tempfile.NamedTemporaryFile()
						for block in request.iter_content(1024*8):
							if not block:
								break
							lf.write(block)
						lf = ContentFile(httl)
						product = Products(name=namelst,price=product_price,source_url=product_link,shop='jumia',genre='gaming')
						product.image.save(file_name[:20],lf)
	except Exception as e:
		subject = 'Crawler Error'
		from_email = settings.EMAIL_HOST_USER
		message = 'The following exception occured %s' % e        
		recipient_list = ['johnsonoye34@gmail.com']
		html_message = '<p>Bros there\'s something went wrong : %s jumia crawler %s</p>'%(e, 'gaming')
		sent_mail = send_mail(
		                subject, 
		                message, 
		                from_email, 
		                recipient_list,  
		                html_message=html_message)
def jumia_phones():
	try:
		for urls in range(1,25):
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			       'Accept-Encoding': 'none',
			       'Accept-Language': 'en-US,en;q=0.8',
			       'Connection': 'keep-alive'}
			html = Request('http://www.jumia.com.ng/smartphones/?page=%s'%urls,headers=hdr)
			htmll = urlopen(html).read()
			bsObj = BeautifulSoup(htmll,'html.parser')
			namelist = bsObj.findAll('div',{'class':'-gallery'})
			for news in namelist:
				product_link = news.find('a',{'class':'link'})
				if product_link:
					product_link = product_link.attrs['href']
					image = news.find('img',{'class':'image'})
					images = image.attrs['data-src']
					product_named = news.find('h2',{'class':'title'})
					product_price = news.find('span', {'class','price'}).find_all('span')
					product_price = product_price[1]
					product_price = bytes(str(product_price.text),'UTF-8')
					product_price = product_price.decode('ascii','ignore')
					namelst = bytes(str(product_named.text), 'UTF-8')
					namelst = namelst.decode('ascii','ignore').replace('\n','').replace('\t','')
					namelst = str(namelst)
					htl = Request(images,headers=hdr)
					httl = urlopen(htl).read()
					print(namelst,product_price)
					if Products.objects.filter(name=namelst,shop='jumia').exists():
						produc = Products.objects.get(name=namelst,shop='jumia')
						# Checks the price
						if produc.price != product_price:
							produc.old_price = produc.price
							produc.source_url = product_link
							produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
							# Updates the price
							produc.price = product_price
							# Saves the price
							
							produc.save()
					else:
						request = requests.get(images, stream=True)
						if request.status_code != requests.codes.ok:
							continue
						randd_ne = get_random_string(length=10)
						file_name = folder + images.split('/')[-1]
						point_finder = file_name.find('.')
						file_name = file_name[:point_finder] + randd_ne
						lf = tempfile.NamedTemporaryFile()
						for block in request.iter_content(1024*8):
							if not block:
								break
							lf.write(block)
						lf = ContentFile(httl)
						product = Products(name=namelst,price=product_price,source_url=product_link,shop='jumia',genre='phone')
						product.image.save(file_name[:20],lf)

	except Exception as e:
			print(e)
			subject = 'Crawler Error'
			from_email = settings.EMAIL_HOST_USER
			message = 'The following exception occured %s' % e        
			recipient_list = ['johnsonoye34@gmail.com']
			html_message = '<p>Bros there\'s something went wrong : %s jumia crawler %s</p>'%(e, 'phones')
			sent_mail = send_mail(
			                subject, 
			                message, 
			                from_email, 
			                recipient_list,  
			                html_message=html_message)
def jumia_laptops():
	try:
		for urls in range(1,25):
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			       'Accept-Encoding': 'none',
			       'Accept-Language': 'en-US,en;q=0.8',
			       'Connection': 'keep-alive'}
			html = Request('https://www.jumia.com.ng/laptops/?page=%s'%urls,headers=hdr)
			htmll = urlopen(html).read()
			bsObj = BeautifulSoup(htmll,'html.parser')
			namelist = bsObj.findAll('div',{'class':'-gallery'})
			for news in namelist:
				product_link = news.find('a',{'class':'link'})
				if product_link:
					product_link = product_link.attrs['href']
					image = news.find('img',{'class':'image'})
					images = image.attrs['data-src']
					product_named = news.find('h2',{'class':'title'})
					product_price = news.find('span', {'class','price'}).find_all('span')
					product_price = product_price[1]
					product_price = bytes(str(product_price.text),'UTF-8')
					product_price = product_price.decode('ascii','ignore')
					namelst = bytes(str(product_named.text), 'UTF-8')
					namelst = namelst.decode('ascii','ignore').replace('\n','').replace('\t','')
					namelst = str(namelst)
					htl = Request(images,headers=hdr)
					httl = urlopen(htl).read()
					if Products.objects.filter(name=namelst,shop='jumia').exists():
						
						produc = Products.objects.get(name=namelst,shop='jumia')
						# Checks the price
						if produc.price != product_price:
							produc.old_price = produc.price
							produc.source_url = product_link
							produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
							# Updates the price
							produc.price = product_price
							# Saves the price
							
							produc.save()
					else:
						request = requests.get(images, stream=True)
						if request.status_code != requests.codes.ok:
							continue
						randd_ne = get_random_string(length=10)
						file_name = folder +images.split('/')[-1]
						point_finder = file_name.find('.')
						file_name = file_name[:point_finder] + randd_ne
						lf = tempfile.NamedTemporaryFile()
						for block in request.iter_content(1024*8):
							if not block:
								break
							lf.write(block)
						lf = ContentFile(httl)
						product = Products(name=namelst,price=product_price,source_url=product_link,shop='jumia',genre='laptops')
						product.image.save(file_name[:20],lf)

	except Exception as e:
		subject = 'Crawler Error'
		from_email = settings.EMAIL_HOST_USER
		message = 'The following exception occured %s' % e        
		recipient_list = ['johnsonoye34@gmail.com']
		html_message = '<p>Bros there\'s something went wrong : %s jumia crawler %s</p>'%(e, 'laptops')
		sent_mail = send_mail(
		                subject, 
		                message, 
		                from_email, 
		                recipient_list,  
		                html_message=html_message)
def jumia_tvs():
	for urls in range(1,50):
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
				'Accept-Encoding': 'none',
				'Accept-Language': 'en-US,en;q=0.8',
				'Connection': 'keep-alive'}
		page_url = 'https://www.jumia.com.ng/televisions/?page=%s'%urls
		html = Request(page_url,headers=hdr)
		htmll = urlopen(html).read()
		bsObj = BeautifulSoup(htmll,'html.parser')
		namelist = bsObj.findAll('div',{'class':'-gallery'})
		for news in namelist:
			product_link = news.find('a',{'class':'link'})
			if product_link:
				product_link = product_link.attrs['href']
				image = news.find('img',{'class':'image'})
				images = image.attrs['data-src']
				product_named = news.find('h2',{'class':'title'})
				product_price = news.find('span', {'class','price'}).find_all('span')
				product_price = product_price[1]
				product_price = bytes(str(product_price.text),'UTF-8')
				product_price = product_price.decode('ascii','ignore')
				namelst = bytes(str(product_named.text), 'UTF-8')
				namelst = namelst.decode('ascii','ignore').replace('\n','').replace('\t','')
				namelst = str(namelst)
				htl = Request(images,headers=hdr)
				httl = urlopen(htl).read()
				print(namelst,product_price)
				if str(product_price) == '3,500':
					print(product_price)
					print(product_link)
					print('yes')
					break
		print(urls)
				# if Products.objects.filter(name=namelst,shop='jumia').exists():
					
				# 	produc = Products.objects.get(name=namelst,shop='jumia')
				# 	# Checks the price
				# 	if produc.price != product_price:
				# 		produc.old_price = produc.price
				# 		produc.source_url = product_link
				# 		produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
				# 		# Updates the price
				# 		produc.price = product_price
				# 		# Saves the price
						
				# 		produc.save()
				# else:
				# 	request = requests.get(images, stream=True)
				# 	if request.status_code != requests.codes.ok:
				# 		continue
				# 	randd_ne = get_random_string(length=10)
				# 	file_name = folder + images.split('/')[-1]
				# 	point_finder = file_name.find('.')
				# 	file_name = file_name[:point_finder] + randd_ne
				# 	lf = tempfile.NamedTemporaryFile()
				# 	for block in request.iter_content(1024*8):
				# 		if not block:
				# 			break
				# 		lf.write(block)
				# 	lf = ContentFile(httl)
				# 	product = Products(name=namelst,price=product_price,source_url=product_link,genre='televisions',shop='jumia')
				# 	product.image.save(file_name[:20],lf)

	
					
def jumia_shirts():
	try:
		for urls in range(1,25):
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			       'Accept-Encoding': 'none',
			       'Accept-Language': 'en-US,en;q=0.8',
			       'Connection': 'keep-alive'}
			page_url = 'https://www.jumia.com.ng/mens-shirts/page=%s'%urls
			html = Request(page_url,headers=hdr)
			htmll = urlopen(html).read()
			bsObj = BeautifulSoup(htmll,'html.parser')
			namelist = bsObj.findAll('div',{'class':'-gallery'})
			for news in namelist:
				product_link = news.find('a',{'class':'link'})
				if product_link:
					product_link = product_link.attrs['href']
					image = news.find('img',{'class':'image'})
					images = image.attrs['data-src']
					product_named = news.find('h2',{'class':'title'})
					product_price = news.find('span', {'class','price'}).find_all('span')
					product_price = product_price[1]
					product_price = bytes(str(product_price.text),'UTF-8')
					product_price = product_price.decode('ascii','ignore')
					namelst = bytes(str(product_named.text), 'UTF-8')
					namelst = namelst.decode('ascii','ignore').replace('\n','').replace('\t','')
					namelst = str(namelst)
					htl = Request(images,headers=hdr)
					httl = urlopen(htl).read()
					if Products.objects.filter(name=namelst,shop='jumia').exists():
						
						produc = Products.objects.get(name=namelst,shop='jumia')
						# Checks the price
						if produc.price != product_price:
							produc.old_price = produc.price
							produc.source_url = product_link
							produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
							# Updates the price
							produc.price = product_price
							# Saves the price
							
							produc.save()
					else:
						request = requests.get(images, stream=True)
						if request.status_code != requests.codes.ok:
							continue
						randd_ne = get_random_string(length=10)
						file_name = folder + images.split('/')[-1]
						point_finder = file_name.find('.')
						file_name = file_name[:point_finder] + randd_ne
						lf = tempfile.NamedTemporaryFile()
						for block in request.iter_content(1024*8):
							if not block:
								break
							lf.write(block)
						lf = ContentFile(httl)
						product = Products(name=namelst,price=product_price,source_url=product_link,genre='shirts',shop='jumia')
						product.image.save(file_name[:20],lf)

	except Exception as e:
		subject = 'Crawler Error'
		from_email = settings.EMAIL_HOST_USER
		message = 'The following exception occured %s' % e        
		recipient_list = ['johnsonoye34@gmail.com']
		html_message = '<p>Bros there\'s something went wrong : %s jumia crawler %s</p>'%(e, 'shirts')
		sent_mail = send_mail(
		                subject, 
		                message, 
		                from_email, 
		                recipient_list,  
		                html_message=html_message)

def jumia_wemen_dresses():
	try:
		for urls in range(1,25):
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			       'Accept-Encoding': 'none',
			       'Accept-Language': 'en-US,en;q=0.8',
			       'Connection': 'keep-alive'}
			page_url = 'https://www.jumia.com.ng/womens-dresses/page=%s'%urls
			html = Request(page_url,headers=hdr)
			htmll = urlopen(html).read()
			bsObj = BeautifulSoup(htmll,'html.parser')
			namelist = bsObj.findAll('div',{'class':'-gallery'})
			for news in namelist:
				product_link = news.find('a',{'class':'link'})
				if product_link:
					product_link = product_link.attrs['href']
					image = news.find('img',{'class':'image'})
					images = image.attrs['data-src']
					product_named = news.find('h2',{'class':'title'})
					product_price = news.find('span', {'class','price'}).find_all('span')
					product_price = product_price[1]
					product_price = bytes(str(product_price.text),'UTF-8')
					product_price = product_price.decode('ascii','ignore')
					namelst = bytes(str(product_named.text), 'UTF-8')
					namelst = namelst.decode('ascii','ignore').replace('\n','').replace('\t','')
					namelst = str(namelst)
					htl = Request(images,headers=hdr)
					httl = urlopen(htl).read()
					print(namelst,product_price)
					if Products.objects.filter(name=namelst,shop='jumia').exists():
						
						produc = Products.objects.get(name=namelst,shop='jumia')
						# Checks the price
						if produc.price != product_price:
							produc.old_price = produc.price
							produc.source_url = product_link
							produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
							# Updates the price
							produc.price =product_price
							# Saves the price
							
							produc.save()
					else:
						request = requests.get(images, stream=True)
						if request.status_code != requests.codes.ok:
							continue
						randd_ne = get_random_string(length=10)
						file_name = folder + images.split('/')[-1]
						point_finder = file_name.find('.')
						file_name = file_name[:point_finder] + randd_ne
						lf = tempfile.NamedTemporaryFile()
						for block in request.iter_content(1024*8):
							if not block:
								break
							lf.write(block)
						lf = ContentFile(httl)
						product = Products(name=namelst,price=product_price,source_url=product_link,genre='women-dresses',shop='jumia')
						product.image.save(file_name[:20],lf)

	except Exception as e:
		subject = 'Crawler Error'
		from_email = settings.EMAIL_HOST_USER
		message = 'The following exception occured %s' % e        
		recipient_list = ['johnsonoye34@gmail.com']
		html_message = '<p>Bros there\'s something went wrong : %s jumia crawler %s</p>'%(e, 'womens-dresses')
		sent_mail = send_mail(
		                subject, 
		                message, 
		                from_email, 
		                recipient_list,  
		                html_message=html_message)
def jumia_men_watches():
	try:
		for urls in range(1,25):
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			       'Accept-Encoding': 'none',
			       'Accept-Language': 'en-US,en;q=0.8',
			       'Connection': 'keep-alive'}
			page_url = 'https://www.jumia.com.ng/mens-watches/?page=%s'%urls
			html = Request(page_url,headers=hdr)
			htmll = urlopen(html).read()
			bsObj = BeautifulSoup(htmll,'html.parser')
			namelist = bsObj.findAll('div',{'class':'-gallery'})
			for news in namelist:
				product_link = news.find('a',{'class':'link'})
				if product_link:
					product_link = product_link.attrs['href']
					image = news.find('img',{'class':'image'})
					images = image.attrs['data-src']
					product_named = news.find('h2',{'class':'title'})
					product_price = news.find('span', {'class','price'}).find_all('span')
					product_price = product_price[1]
					product_price = bytes(str(product_price.text),'UTF-8')
					product_price = product_price.decode('ascii','ignore')
					namelst = bytes(str(product_named.text), 'UTF-8')
					namelst = namelst.decode('ascii','ignore').replace('\n','').replace('\t','')
					namelst = str(namelst)
					htl = Request(images,headers=hdr)
					httl = urlopen(htl).read()
					print(namelst,product_price)
					if Products.objects.filter(name=namelst,shop='jumia',genre='men-watches').exists():
						
						produc = Products.objects.get(name=namelst,shop='jumia',genre='men-watches')
						# Checks the price
						if produc.price != product_price:
							produc.old_price = produc.price
							produc.source_url = product_link
							produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
							# Updates the price
							produc.price =product_price
							# Saves the price
							
							produc.save()
					else:
						request = requests.get(images, stream=True)
						if request.status_code != requests.codes.ok:
							continue
						randd_ne = get_random_string(length=10)
						file_name = folder + images.split('/')[-1]
						point_finder = file_name.find('.')
						file_name = file_name[:point_finder] + randd_ne
						lf = tempfile.NamedTemporaryFile()
						for block in request.iter_content(1024*8):
							if not block:
								break
							lf.write(block)
						lf = ContentFile(httl)
						product = Products(name=namelst,price=product_price,source_url=product_link,genre='men-watches',shop='jumia')
						product.image.save(file_name[:20],lf)

	except Exception as e:
		subject = 'Crawler Error'
		from_email = settings.EMAIL_HOST_USER
		message = 'The following exception occured %s' % e        
		recipient_list = ['johnsonoye34@gmail.com']
		html_message = '<p>Bros there\'s something went wrong : %s jumia crawler %s</p>'%(e, 'men_watches')
		sent_mail = send_mail(
		                subject, 
		                message, 
		                from_email, 
		                recipient_list,  
		                html_message=html_message)

def jumia_women_watches():
	try:
		for urls in range(1,25):
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			       'Accept-Encoding': 'none',
			       'Accept-Language': 'en-US,en;q=0.8',
			       'Connection': 'keep-alive'}
			page_url = 'https://www.jumia.com.ng/womens-watches/?page=%s'%urls
			html = Request(page_url,headers=hdr)
			htmll = urlopen(html).read()
			bsObj = BeautifulSoup(htmll,'html.parser')
			namelist = bsObj.findAll('div',{'class':'-gallery'})
			for news in namelist:
				product_link = news.find('a',{'class':'link'})
				if product_link:
					product_link = product_link.attrs['href']
					image = news.find('img',{'class':'image'})
					images = image.attrs['data-src']
					product_named = news.find('h2',{'class':'title'})
					product_price = news.find('span', {'class','price'}).find_all('span')
					product_price = product_price[1]
					product_price = bytes(str(product_price.text),'UTF-8')
					product_price = product_price.decode('ascii','ignore')
					namelst = bytes(str(product_named.text), 'UTF-8')
					namelst = namelst.decode('ascii','ignore').replace('\n','').replace('\t','')
					namelst = str(namelst)
					htl = Request(images,headers=hdr)
					httl = urlopen(htl).read()
					print(namelst,product_price)
					if Products.objects.filter(name=namelst,shop='jumia',genre='women-watches').exists():
						
						produc = Products.objects.get(name=namelst,shop='jumia',genre='women-watches')
						# Checks the price
						if produc.price != product_price:
							produc.old_price = produc.price
							produc.source_url = product_link
							produc.old_price_digit = int(produc.price.replace(',','').replace('\n','').replace('.00',''))
							# Updates the price
							produc.price =product_price
							# Saves the price
							
							produc.save()
					else:
						request = requests.get(images, stream=True)
						if request.status_code != requests.codes.ok:
							continue
						randd_ne = get_random_string(length=10)
						file_name = folder + images.split('/')[-1]
						point_finder = file_name.find('.')
						file_name = file_name[:point_finder] + randd_ne
						lf = tempfile.NamedTemporaryFile()
						for block in request.iter_content(1024*8):
							if not block:
								break
							lf.write(block)
						lf = ContentFile(httl)
						product = Products(name=namelst,price=product_price,source_url=product_link,genre='women-watches',shop='jumia')
						product.image.save(file_name[:20],lf)

	except Exception as e:
		subject = 'Crawler Error'
		from_email = settings.EMAIL_HOST_USER
		message = 'The following exception occured %s' % e        
		recipient_list = ['johnsonoye34@gmail.com']
		html_message = '<p>Bros there\'s something went wrong : %s jumia crawler %s</p>'%(e, 'women-watches')
		sent_mail = send_mail(
		                subject, 
		                message, 
		                from_email, 
		                recipient_list,  
		                html_message=html_message)