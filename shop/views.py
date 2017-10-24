from django.shortcuts import render
from django.http import HttpResponse
from findit.models import *
from adengine.models import Ads
from adengine.analytics import seen_by,landlord
from urllib.parse import quote_plus
import time
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def store(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# seen_by(request,ad)
	# landlord(request,ad)
	return render(request,'shop/index.html',{})

def store_details(request,word):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# seen_by(request,ad)
	# landlord(request,ad)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(shop=word)
	product_counter = all_products.count()
	query = request.GET.get('q')
	if query:
		all_products = Products.objects.all().filter(shop=word)
		if 'iphone' in str(query.lower()) or 'ipad' in str(query.lower()):
			quey = query.split()
			if len(quey) >= 3:
				for q in quey:
					all_products = all_products.filter(
			           Q(name__icontains=q)|
			           Q(name__iexact=q)
					).distinct()
			else:	
				query = query.strip()
				all_products = all_products.filter(
				           Q(name__icontains=query)|
				           Q(name__iexact=query)
				).distinct()
		else:
			query = query.split()
			for q in query:
				all_products = all_products.filter(
				           Q(name__icontains=q)|
				           Q(name__iexact=q)
				).distinct()
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
		query = ' '.join(query)
	page_request_var = 'page'
	paginator = Paginator(all_products,40)
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range return an empty page
			return HttpResponse('')
	if request.is_ajax():
		return render(request,'results_ajax.html',{'products':queryset})
	context = {'products':queryset,
			'query':query,
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			
			'shop':word,
			'mack':'mack'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'shop/results_page.html',context)

def store_shirts(request,word):
	# ad = Ads.objects.order_by('?').filter(expired='False')[:2]
	# seen_by(request,ad)
	# landlord(request,ad)
	t1 = time.time()
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='shirts',shop=word)
	query = request.GET.get('q')
	if query:
		all_products = Products.objects.all()
		if 'iphone' in str(query.lower()) or 'ipad' in str(query.lower()):
			quey = query.split()
			if len(quey) >= 3:
				for q in quey:
					all_products = all_products.filter(
			           Q(name__icontains=q)|
			           Q(name__iexact=q)
					).distinct()
			else:	
				query = query.strip()
				all_products = all_products.filter(
				           Q(name__icontains=query)|
				           Q(name__iexact=query)
				).distinct()
		else:
			query = query.split()
			for q in query:
				all_products = all_products.filter(
				           Q(name__icontains=q)|
				           Q(name__iexact=q)
				).distinct()
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
		query = ' '.join(query)
	page_request_var = 'page'
	paginator = Paginator(all_products,40)
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range return an empty page
			return HttpResponse('')
	if request.is_ajax():
		return render(request,'results_ajax.html',{'products':queryset})
	context = {'products':queryset,
			'query':query,
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'shop':word,
			'mack':'mack'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'shop/results_page.html',context)

def store_phones(request,word):
	# ad = Ads.objects.order_by('?').filter(expired='False')[:2]
	# seen_by(request,ad)
	# landlord(request,ad)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='',shop=word)
	product_counter = all_products.count()
	query = request.GET.get('q')
	if query:
		all_products = Products.objects.all()
		if 'iphone' in str(query.lower()) or 'ipad' in str(query.lower()):
			quey = query.split()
			if len(quey) >= 3:
				for q in quey:
					all_products = all_products.filter(
			           Q(name__icontains=q)|
			           Q(name__iexact=q)
					).distinct()
			else:	
				query = query.strip()
				all_products = all_products.filter(
				           Q(name__icontains=query)|
				           Q(name__iexact=query)
				).distinct()
		else:
			query = query.split()
			for q in query:
				all_products = all_products.filter(
				           Q(name__icontains=q)|
				           Q(name__iexact=q)
				).distinct()
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
		query = ' '.join(query)
	page_request_var = 'page'
	paginator = Paginator(all_products,40)
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range return an empty page
			return HttpResponse('')
	if request.is_ajax():
		return render(request,'results_ajax.html',{'products':queryset})
	context = {'products':queryset,
			'query':query,
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'shop':word,
			'mack':'mack'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'shop/results_page.html',context)

def store_laptops(request,word):
	# ad = Ads.objects.order_by('?').filter(expired='False')[:2]
	# seen_by(request,ad)
	# print('jii')
	# landlord(request,ad)
	t1 = time.time()
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='laptops',shop=word)
	query = request.GET.get('q')
	if query:
		all_products = Products.objects.all()
		if 'iphone' in str(query.lower()) or 'ipad' in str(query.lower()):
			quey = query.split()
			if len(quey) >= 3:
				for q in quey:
					all_products = all_products.filter(
			           Q(name__icontains=q)|
			           Q(name__iexact=q)
					).distinct()
			else:	
				query = query.strip()
				all_products = all_products.filter(
				           Q(name__icontains=query)|
				           Q(name__iexact=query)
				).distinct()
		else:
			query = query.split()
			for q in query:
				all_products = all_products.filter(
				           Q(name__icontains=q)|
				           Q(name__iexact=q)
				           
				).distinct()
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
		query = ' '.join(query)
	page_request_var = 'page'
	paginator = Paginator(all_products,40)
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range return an empty page
			return HttpResponse('')
	if request.is_ajax():
		return render(request,'results_ajax.html',{'products':queryset})
	context = {'products':queryset,
			'query':query,
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'shop':word,
			'mack':'mack'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'shop/results_page.html',context)

def store_tv_index(request,word):
	ad = Ads.objects.order_by('?').filter(expired='False')[:2]
	seen_by(request,ad)
	landlord(request,ad)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='televisions',shop=word)
	product_counter = all_products.count()
	query = request.GET.get('q')
	if query:
		all_products = Products.objects.all()
		if 'iphone' in str(query.lower()) or 'ipad' in str(query.lower()):
			quey = query.split()
			if len(quey) >= 3:
				for q in quey:
					all_products = all_products.filter(
			           Q(name__icontains=q)|
			           Q(name__iexact=q)
					).distinct()
			else:	
				query = query.strip()
				all_products = all_products.filter(
				           Q(name__icontains=query)|
				           Q(name__iexact=query)
				).distinct()
		else:
			query = query.split()
			for q in query:
				all_products = all_products.filter(
				           Q(name__icontains=q)|
				           Q(name__iexact=q)
				).distinct()
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
		query = ' '.join(query)
	page_request_var = 'page'
	paginator = Paginator(all_products,40)
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range return an empty page
			return HttpResponse('')
	if request.is_ajax():
		return render(request,'results_ajax.html',{'products':queryset})
	context = {'products':queryset,
			'query':query,
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'shop':word,
			'mack':'mack'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'shop/results_page.html',context)

def store_women_index(request,word):
	ad = Ads.objects.order_by('?').filter(expired='False')[:2]
	seen_by(request,ad)
	landlord(request,ad)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='women-dresses',shop=word)
	product_counter = all_products.count()
	query = request.GET.get('q')
	if query:
		all_products = Products.objects.all()
		if 'iphone' in str(query.lower()) or 'ipad' in str(query.lower()):
			quey = query.split()
			if len(quey) >= 3:
				for q in quey:
					all_products = all_products.filter(
			           Q(name__icontains=q)|
			           Q(name__iexact=q)
					).distinct()
			else:	
				query = query.strip()
				all_products = all_products.filter(
				           Q(name__icontains=query)|
				           Q(name__iexact=query)
				).distinct()
		else:
			query = query.split()
			for q in query:
				all_products = all_products.filter(
				           Q(name__icontains=q)|
				           Q(name__iexact=q)
				).distinct()
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
		query = ' '.join(query)
	page_request_var = 'page'
	paginator = Paginator(all_products,40)
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range return an empty page
			return HttpResponse('')
	if request.is_ajax():
		return render(request,'results_ajax.html',{'products':queryset})
	context = {'products':queryset,
			'query':query,
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'shop':word,
			'mack':'mack'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'shop/results_page.html',context)