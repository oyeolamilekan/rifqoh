from django.shortcuts import render,redirect
from .models import Products,Feedback,Analytics,UserTheme
from actions.utils import subscribe
# Create your views here.
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.db.models import Q
import datetime
from .forms import feedBackForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from .utils import black_rock,nairaconv
import time
from urllib.parse import quote_plus
from django.contrib.auth.models import User
from accounts.models import *
from adengine.models import Ads
from adengine.analytics import seen_by,landlord
from analytics.models import PageViews,UserTime
from analytics.utils import add_query
from analytics.signals import object_viewed
from analytics.utils import whichPage,user_count,user_converter
#from .an_utils import correction
from analytics.an_utils import get_client_ip
import random


def home_page(request):
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	url = request.build_absolute_uri()
	whichPage(request,'home_page',url)
	user = get_client_ip(request)
	user_theme = ''
	if UserTheme.objects.filter(user=user).exists():
		user_theme = UserTheme.objects.get(user=user)
	user_count(request)
	# ipo = get_client_ip(request)
	# if UserTheme.objects.filter(user=ipo).exists():
	# 	bool_boy = True

	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	context = {'share_string':share_string,'url':url,'user_theme':user_theme,'page':'front_page'}
	return render(request,'search_page.html',context)


def user_choice(request):
	user = get_client_ip(request)
	if UserTheme.objects.filter(user=user).exists():
		user_theme = UserTheme.objects.get(user=user)
		if user_theme.theme:
			user_theme.theme = False
			user_theme.save()
		else:
			user_theme.theme = True
			user_theme.save()
	else:
		user_theme = UserTheme.objects.create(user=user,theme=True)
		user_theme.save()
	return HttpResponse('mi')

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

def advanced_search(request):
	#share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	url = request.build_absolute_uri()
	whichPage(request,'advanced_search',url)
	user_count(request)
	try:
		brand_name = request.GET.get('brand',None)
		start_price = int(request.GET.get('start_price',None).replace(',','').replace('\n','').replace('.00',''))
		end_price = int(request.GET.get('end_price',None).replace(',','').replace('\n','').replace('.00',''))
		if brand_name and start_price and end_price:
			all_products = Products.objects.filter(Q(name__icontains=brand_name,real_price__gte=int(start_price),real_price__lte=int(end_price))).distinct()
		context = {'products':all_products}
	except:
		context = {'twinkle':'Your query just scatered our database'}
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	context['com'] = 'Nothing'
	return render(request,'results_page.html',context)

def real_index(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	# seen_by(request,prod_ad)
	# landlord(request,prod_ad)
	user_count(request)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	url = request.build_absolute_uri()
	whichPage(request,'discoverB',url)
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	query = request.GET.get('q')
	#print(query,'hgf')
	all_products = Products.objects.order_by('?')
	if query:
		whichPage(request,'search',request.build_absolute_uri())
		if 'iphone' in str(query.lower()) or 'ipad' in str(query.lower()):
			# # print(query)
			# print(list(query))
			query = query.lower()
			quey = query.split()
			if len(quey) >= 3:
				if 'plus' in quey and len(quey) <= 3:
					q = ' '.join(quey)
					all_products = all_products.filter(
				           Q(name__icontains=q)|
				           Q(name__iexact=q)
						).distinct()
				else:
					for q in quey:
						
						all_products = all_products.filter(
						           Q(name__icontains=q)
						           
						).distinct()
				add_query(query,'search page',all_products[:10],nbool=True,correct=query)
			else:
				query = correction(query)

				print(query)
				query = query.strip()
				all_products = all_products.filter(
				           Q(name__icontains=query)|
				           Q(name__iexact=query)
				).distinct()
				if len(all_products) == 0:
					add_query(query,'search page',all_products[:10],nbool=False,correct=query)
				else:
					add_query(query,'search page',all_products[:10],nbool=True,correct=query)
		else:
			query = query.split()
			new = []
			for q in query:
				q = correction(q)

				print(q)
				new.append(q)
				# Put them all together
				
				all_products = all_products.filter(
				           Q(name__icontains=q)|
				           Q(name__iexact=q)
				).distinct()
			
			query = ' '.join(query)
			made = ' '.join(new)
			if len(all_products) == 0:
				add_query(query,'search page',all_products[:10],nbool=False,correct=made)
			else:
				add_query(query,'search page',all_products[:10],nbool=True,correct=made)
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
	com = ''
	page_request_var = 'page'
	if page_request_var and query:
		com = 'Nothing'
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
			'trendin':'home',
			'com':com,
			'page':'index_page'
			}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.3f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def shirts(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	# seen_by(request,prod_ad)
	# landlord(request,prod_ad)
	user_count(request)
	url = request.build_absolute_uri()
	whichPage(request,'shirtsP',url)
	t1 = time.time()
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='shirts')
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
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
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'page':'shirt_page'
			}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def index(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	# seen_by(request,prod_ad)
	# landlord(request,prod_ad)
	user_count(request)
	url = request.build_absolute_uri()
	whichPage(request,'phoneP',url)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='')
	product_counter = all_products.count()
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
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
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'page':'phone_page'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def laptops(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	# seen_by(request,prod_ad)
	# landlord(request,prod_ad)
	user_count(request)
	url = request.build_absolute_uri()
	whichPage(request,'laptopsP',url)
	t1 = time.time()
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='laptops')
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
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
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'page':'laptop_page'
			}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def tv_index(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	# seen_by(request,prod_ad)
	# landlord(request,prod_ad)
	url = request.build_absolute_uri()
	user_count(request)
	whichPage(request,'tvP',url)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='televisions')
	product_counter = all_products.count()
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
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
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'page':'tv_page'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def makeup(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	# seen_by(request,prod_ad)
	# landlord(request,prod_ad)
	url = request.build_absolute_uri()
	user_count(request)
	whichPage(request,'tvP',url)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='makeup')
	product_counter = all_products.count()
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
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
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'page':'makeup_page'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def headphones(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	# seen_by(request,prod_ad)
	# landlord(request,prod_ad)
	url = request.build_absolute_uri()
	user_count(request)
	whichPage(request,'tvP',url)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='headphones')
	product_counter = all_products.count()
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
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
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'page':'headphone_page'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def wemenbags(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	# seen_by(request,prod_ad)
	# landlord(request,prod_ad)
	url = request.build_absolute_uri()
	user_count(request)
	whichPage(request,'tvP',url)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='women-bags')
	product_counter = all_products.count()
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
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
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'page':'wemen_bags_page'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)



def women_index(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	# seen_by(request,prod_ad)
	# landlord(request,prod_ad)
	user_count(request)
	url = request.build_absolute_uri()
	whichPage(request,'wemenP',url)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='women-dresses')
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
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'page':'women_dress_page'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def women_watch(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	# seen_by(request,prod_ad)
	# landlord(request,prod_ad)
	user_count(request)
	url = request.build_absolute_uri()
	whichPage(request,'wemen_watchP',url)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='women-watches')
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
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'page':'women_page'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)

def men_watch(request):
	# ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
	# prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
	# print(screen_width)
	# ad = Ads.objects.order_by('?')[:1]
	# seen_by(request,ad)
	# landlord(request,ad)
	# seen_by(request,prod_ad)
	# landlord(request,prod_ad)
	user_count(request)
	url = request.build_absolute_uri()
	whichPage(request,'men_watchP',url)
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	all_products = Products.objects.order_by('?').filter(genre='men-watches')
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
			'confirmed':confirmed,
			'all_product':all_products,
			'share_string':share_string,
			'page':'men_watch_page'}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.6f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'results_page.html',context)
	
def number_of_clicks(request,id):
	product = Products.objects.get(id=id)
	object_viewed.send(product.__class__,instance=product,request=request)
	product.num_of_clicks = product.num_of_clicks + 1
	product.save()
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
	return HttpResponse('all done bosees')

def engine_starter(request):
	black_rock()
	return HttpResponse('All done bose')


def stupid_me(request):
	loo = Products.objects.filter(shop='payporte').filter(genre='shirts')
	loo.delete()
	return HttpResponse('allo ')

def twitter_bot(request):
	return HttpResponse('you are in trouble')

def sugget(request):
	pixeld = []
	sugget_input = request.GET.get('search',None)
	sucide = Products.objects.filter(name__icontains=sugget_input)[:10]
	for su in sucide:
		new_product = su.name.split()
		new_product = ' '.join(new_product)
		pixeld.append(new_product[:25])
	return JsonResponse({'query':pixeld})

def deleteu(request):
	return HttpResponse('all done')

def convert_me(request):
	products = Products.objects.all()
	for product in products:
		analytics = Analytics.objects.get(id=product.id)
		product.num_of_clicks = product.num_of_clicks + analytics.number_of_clicks
		product.save()
	return HttpResponse('All done Boss Again')

def user_convertion(request):
	users = PageViews.objects.all()
	for user in users:
		user_converter(user.ip_address)

	return HttpResponse('hello world')

def priceconvert(request):
	products = Products.objects.filter(shop='aliexpress')
	for product in products:
		price = nairaconv(product.price)
		product.converted_price = price
		product.save()

	return HttpResponse('hello world')

def priceconvert(request):
	products = Products.objects.filter(shop='aliexpress')
	for product in products:
		price = nairaconv(product.price)
		product.converted_price = price.replace("'",'')
		product.save()
	return HttpResponse('hello world')

def polp(request):
	products = Products.objects.filter(shop='aliexpress')
	for product in products:
		price = nairaconv(product.price)
		product.price = '$ US $19.60'
		product.save()
	return HttpResponse('bfgg')

def timeLogs(request):
	user = get_client_ip(request)
	time = request.GET.get('timespent',None)
	page = request.GET.get('page',None)
	#print(abs(int(time)),user,page)
	time = str(abs(int(time)))
	user_time = UserTime.objects.create(user_o=user,time_spent=time,page=page)
	user_time.save()
	return HttpResponse('hii')
############################################################################
#####################		Trending Layout			########################

def real_trend(request,word):
	share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
	t1 = time.time()
	url = request.build_absolute_uri()
	whichPage(request,'Trending',url)
	orginal_sentence = []
	corrected_sentence = []
	confirmed = None
	query = request.GET.get('q')
	if word != 'index':
		all_products = Products.objects.order_by('-num_of_clicks').filter(genre=word)
	else:
		all_products = Products.objects.order_by('-num_of_clicks')
	if query:
		whichPage(request,'search Trending',request.build_absolute_uri())
		if 'iphone' in str(query.lower()) or 'ipad' in str(query.lower()):
			# # print(query)
			# print(list(query))
			query = query.lower()
			quey = query.split()
			if len(quey) >= 3:
				if 'plus' in quey and len(quey) <= 3:
					q = ' '.join(quey)
					all_products = all_products.filter(
				           Q(name__icontains=q)|
				           Q(name__iexact=q)
						).distinct()
				else:
					for q in quey:
						
						all_products = all_products.filter(
						           Q(name__icontains=q)
						           
						).distinct()
				add_query(query,'search page',all_products[:10],nbool=True)
			else:
				#query = correction(query)
				query = query.strip()
				all_products = all_products.filter(
				           Q(name__icontains=query)|
				           Q(name__iexact=query)
				).distinct()
				if len(all_products) == 0:
					add_query(query,'search page',all_products[:10],nbool=False)
				else:
					add_query(query,'search page',all_products[:10],nbool=True)
		else:
			query = query.split()
			for q in query:
				all_products = all_products.filter(
				           Q(name__icontains=q)|
				           Q(name__iexact=q)
				).distinct()
			query = ' '.join(query)
			if len(all_products) == 0:
				add_query(query,'search page',all_products[:10],nbool=False)
			else:
				add_query(query,'search page',all_products[:10],nbool=True)
		# if corrected_sentence != orginal_sentence:
		# 	corrected_sentence = ' '.join(corrected_sentence)
		# 	orginal_sentence = ' '.join(orginal_sentence)
		# 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
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
			'page':'trending_'+word

			}
	#print(all_products.count())
	t2 = time.time()
	query_time = t2 - t1
	query_time = '{:.3f}'.format(query_time)
	context['query_time']=query_time
	return render(request,'result_trend_page.html',context)

def delunn(request):
	prod = Products.objects.filter(name__icontains='Apple',genre='women-dresses')
	prod.delete()
	return HttpResponse('Sacrifices')

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