from django.shortcuts import render,redirect
from .models import Products,Feedback
from actions.utils import subscribe
# Create your views here.
from .y_crawler import yudala
from .cralwer import payporte_crawler
from .k_cralwer import konga_crawler
from .j_crawler import jumia_crawler
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.db.models import Q
import datetime
from .forms import feedBackForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from .utils import correction 
import time
from urllib.parse import quote_plus
from django.contrib.auth.models import User
from accounts.models import *
from adengine.models import Ads
from adengine.analytics import seen_by,landlord
def home_page(request):
	share_string = quote_plus('compare price from different stores at pricenpick.com #popular')
	url = request.build_absolute_uri()
	ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:1]
	seen_by(request,ad)
	landlord(request,ad)
	context = {'share_string':share_string,'url':url,'ad':ad}
	return render(request,'search_page.html',context)

def minus_club(request):
	try:
		ad_id = int(request.GET.get('ad_id'))
		ad = Ads.objects.get(id=ad_id)
		ad.views = ad.views - 1
		ad.save()
		bad_ad_view = ad.view_set.last()
		bad_ad_view.delete()
		return HttpResponse('hi')
	except:
		return HttpResponse('*')

def real_index(request):
	ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	seen_by(request,ad)
	landlord(request,ad)
	seen_by(request,prod_ad)
	landlord(request,prod_ad)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	query = request.GET.get('q')
	all_products = Products.objects.order_by('?')
	if query:
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
			'ad':ad,
			'path':'home',
			'prod_ad':prod_ad}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def shirts(request):
	ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	seen_by(request,ad)
	landlord(request,ad)
	seen_by(request,prod_ad)
	landlord(request,prod_ad)
	t1 = time.time()
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='shirts')
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
			'ad':ad,
			'prod_ad':prod_ad}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def index(request):
	ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	seen_by(request,ad)
	landlord(request,ad)
	seen_by(request,prod_ad)
	landlord(request,prod_ad)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='')
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
			'ad':ad,
			'prod_ad':prod_ad}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def laptops(request):
	ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	seen_by(request,ad)
	landlord(request,ad)
	seen_by(request,prod_ad)
	landlord(request,prod_ad)
	t1 = time.time()
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='laptops')
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
			'ad':ad,
			'prod_ad':prod_ad}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def tv_index(request):
	ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	seen_by(request,ad)
	landlord(request,ad)
	seen_by(request,prod_ad)
	landlord(request,prod_ad)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='televisions')
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
			'ad':ad,
			'prod_ad':prod_ad}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def women_index(request):
	ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	seen_by(request,ad)
	landlord(request,ad)
	seen_by(request,prod_ad)
	landlord(request,prod_ad)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='women-dresses')
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
			'ad':ad,
			'prod_ad':prod_ad}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def number_of_clicks(request,id):
	product = Products.objects.get(id=id)
	product.analytics.number_of_clicks = product.analytics.number_of_clicks + 1
	product.analytics.save()
	if product.shop == 'jumia':
		return HttpResponseRedirect('http://c.jumia.io/?a=35588&c=11&p=r&E=kkYNyk2M4sk%3d&ckmrdr='+product.source_url+'&utm_source=cake&utm_medium=affiliation&utm_campaign=35588&utm_term=')
	else:
		return HttpResponseRedirect(product.source_url)

def feedback(request):
	if request.method != 'POST':
		form = feedBackForm()
	else:
		form = feedBackForm(request.POST,request.FILES or None)
		if form.is_valid():
			form.save()
	return HttpResponse('ok')

def despiration(request):
	stuffs = Products.objects.all()
	for i in stuffs:
		i.real_price = int(i.price.replace(',','').replace('\n','').replace('.00',''))
		i.save()
	return HttpResponse('All done boss')

def all_on_it(request):
	loo = Products.objects.all()
	loo.delete()
	return HttpResponse('all done bosees')

def engine_starter(request):
	#konga_crawler()
	#yudala()
	#payporte_crawler()
	#jumia_crawler()
	return HttpResponse('All done bose')


def stupid_me(request):
	loo = Products.objects.filter(shop='payporte').filter(genre='shirts')
	loo.delete()
	return HttpResponse('allo ')

def twitter_bot(request):
	loo = Products.objects.filter(name__icontains='ipad')
	for lo in loo:
		lo.genre = ''
		lo.save()
	return HttpResponse('you are in trouble')

# def stream(request):
# 	all_products = Products.objects.order_by('?').filter(genre__in=[subb.lisert for subb in sub_listo])
# 	product_counter = all_products.count()
# 	click_bait = all_products.order_by('?')
# def sub(request):
# 	new = User.objects.get(username=request.user)
# 	sub_list = Sub.objects.create(user=new,lisert='laptops')
# 	all_products = Products.objects.order_by('?').filter(genre__in=[subb.lisert for subb in sub_listo])
# 	product_counter = all_products.count()
# 	click_bait = all_products.order_by('?')
# 	sub_list.save()
# 	return HttpResponse('jjj')