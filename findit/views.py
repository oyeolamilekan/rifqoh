from .forms import feedBackForm
from .models import Products, Analytics, UserTheme, Tips, Feedback
from .utils import black_rock, nairaconv
from .search_instance import experimental_search,search_bite
from accounts.models import *
from adplace.models import Ads
from analytics.an_utils import get_client_ip, get_location, get_header_info, is_bot
from analytics.models import PageViews, UserTime, UserNumber
from analytics.signals import object_viewed
from analytics.utils import whichPage, user_count, user_converter, get_location
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# Create your views here.
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
import time
from urllib.parse import quote_plus
from .test_crawler import test_cralwer
from django.utils.text import slugify
from django.conf import settings
from django.core.mail import send_mail
from watson import search as watson

# Intial Stops words for the users
global  share_stringe
global products_list
products_list = Products.objects.all()
share_stringe = quote_plus('Get the best prices from different stores o quickfinda.com.')
def about_home(request):
    return render(request, 'about.html', {})

def batch_convertor(request):
    users = UserNumber.objects.all()
    for user in users:
        user_c_name, user_c_code = get_location(number=user.user_ip)

        user.user_country_name = user_c_name
        user.user_country_code = user_c_code
        user.save()
    return HttpResponse('Part Ways')

def home_page(request):
    share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
    url = request.build_absolute_uri()
    whichPage(request, 'home_page', url)
    user = get_client_ip(request)
    userTheme = ''
    if UserTheme.objects.filter(user=user).exists():
        user_theme = UserTheme.objects.get(user=user)
    user_count(request)
    # ipo = get_client_ip(request)
    # if UserTheme.objects.filter(user=ipo).exists():
    # 	bool_boy = True

    # ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:1]
    # seen_by(request,ad)
    # landlord(request,ad)
    context = {'share_string': share_string, 'url': url, 'page': 'front_page'}
    return render(request, 'search_page.html', context)

# Internalise Products
def going_global(request):
    products = Products.objects.filter(shop='aliexpress')
    for product in products:
        product.country_code = 'US'
        product.save()
    return HttpResponse("Bigest Fan")



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
    # share_string = quote_plus('compare price from different stores at quickfinda.com #popular')
    t1 = time.time()
    url = request.build_absolute_uri()
    #whichPage(request, 'advanced_search', url)
    #user_count(request)
    try:
        brand_name = request.GET.get('brand', None)
        start_price = int(request.GET.get('start_price', None).replace(',', '').replace('\n', '').replace('.00', ''))
        end_price = int(request.GET.get('end_price', None).replace(',', '').replace('\n', '').replace('.00', ''))
        if brand_name and start_price and end_price:
            all_products = Products.objects.filter(Q(name__icontains=brand_name, real_price__gte=int(start_price),
                                                     real_price__lte=int(end_price))).distinct()
        context = {'products': all_products}
    except:
        context = {'twinkle': 'Your query just scatered our database'}
    t2 = time.time()
    add_query('product name: %s, price: %s, end_price: %s' % (request.GET.get('brand', None),
                                                              request.GET.get('start_price', None),
                                                              request.GET.get('end_price', None)),
              'advance_search', all_products[:10], nbool=True, correct=request.GET.get('brand', None), request=request)
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    context['com'] = 'Nothing'
    return render(request, 'results_page.html', context)


def real_index(request):
    # ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Banner")[:2]
    # prod_ad = Ads.objects.order_by('?').filter(expired='False',ad_type="Products")[:1]
    # print(screen_width)
    # ad = Ads.objects.order_by('?')[:1]
    # seen_by(request,ad)
    # landlord(request,ad)
    # seen_by(request,prod_ad)
    # landlord(request,prod_ad)
    #user_c_name, user_c_code = get_location(request=request)
    # user_count(request)
    share_string = 'Quickfinda - Online Shop & Price Comparison in Nigeria'
    t1 = time.time()
    url = request.build_absolute_uri()
    #whichPage(request, 'discoverB', url)
    confirmed = None
    query = request.GET.get('q')
    # print(query,'hgf')
    all_products = Products.objects.order_by('?')
    if query:
        # all_products = search_bite(request,query)
        all_products = watson.filter(Products, query)

    # if corrected_sentence != orginal_sentence:
    # 	corrected_sentence = ' '.join(corrected_sentence)
    # 	orginal_sentence = ' '.join(orginal_sentence)
    # 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
    com = ''
    page_request_var = 'page'
    # if page_request_var and query:
    #     com = 'Nothing'
    # if user_c_code == 'US':
    #     all_products = all_products.filter(country_code='US').order_by('?')
    paginator = Paginator(all_products, 20)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'query': query,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'trendin': 'home',
               'com': com,
               'page': 'index_page'
               }
    # print(all_products.count())
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.3f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)


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
    whichPage(request, 'shirtsP', url)
    t1 = time.time()
    share_string = 'Shirts - Online Shop & Price Comparison in Nigeria'
    confirmed = None
    all_products = Products.objects.order_by('?').filter(genre='shirts')
    # if corrected_sentence != orginal_sentence:
    # 	corrected_sentence = ' '.join(corrected_sentence)
    # 	orginal_sentence = ' '.join(orginal_sentence)
    # 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
    page_request_var = 'page'
    paginator = Paginator(all_products, 20)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'page': 'shirt_page'
               }
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)


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
    whichPage(request, 'phoneP', url)
    share_string = 'Compare Mobile Phones - Latest Mobile Comparison by Price'
    t1 = time.time()
    confirmed = None
    all_products = Products.objects.order_by('?').filter(genre='phone')
    product_counter = all_products.count()
    # if corrected_sentence != orginal_sentence:
    # 	corrected_sentence = ' '.join(corrected_sentence)
    # 	orginal_sentence = ' '.join(orginal_sentence)
    # 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
    page_request_var = 'page'
    paginator = Paginator(all_products, 20)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'page': 'phone_page'}
    # print(all_products.count())
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)


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
    whichPage(request, 'laptopsP', url)
    t1 = time.time()
    share_string = 'Compare Laptops - Latest Laptops by Price'
    orginal_sentence = []
    corrected_sentence = []
    confirmed = None
    all_products = Products.objects.order_by('?').filter(genre='laptops')
    # if corrected_sentence != orginal_sentence:
    # 	corrected_sentence = ' '.join(corrected_sentence)
    # 	orginal_sentence = ' '.join(orginal_sentence)
    # 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
    page_request_var = 'page'
    paginator = Paginator(all_products, 20)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'page': 'laptop_page'
               }
    # print(all_products.count())
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)


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
    whichPage(request, 'tvP', url)
    share_string = 'Compare TV - Latest TV by Price '
    t1 = time.time()
    confirmed = None
    all_products = Products.objects.order_by('?').filter(genre='televisions')
    product_counter = all_products.count()
    # if corrected_sentence != orginal_sentence:
    # 	corrected_sentence = ' '.join(corrected_sentence)
    # 	orginal_sentence = ' '.join(orginal_sentence)
    # 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
    page_request_var = 'page'
    paginator = Paginator(all_products, 20)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'page': 'tv_page'}
    # print(all_products.count())
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)


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
    whichPage(request, 'tvP', url)
    share_string = share_string = 'Compare Makeups - Latest Makeups by Price & Shop'
    t1 = time.time()
    confirmed = None
    all_products = Products.objects.order_by('?').filter(genre='makeup')
    product_counter = all_products.count()
    # if corrected_sentence != orginal_sentence:
    # 	corrected_sentence = ' '.join(corrected_sentence)
    # 	orginal_sentence = ' '.join(orginal_sentence)
    # 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
    page_request_var = 'page'
    paginator = Paginator(all_products, 20)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'page': 'makeup_page'}
    # print(all_products.count())
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)


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
    whichPage(request, 'tvP', url)
    share_string = 'Compare Headphones - Latest Headphones by Price & Shop'
    t1 = time.time()
    confirmed = None
    all_products = Products.objects.order_by('?').filter(genre='headphones')
    product_counter = all_products.count()
    # if corrected_sentence != orginal_sentence:
    # 	corrected_sentence = ' '.join(corrected_sentence)
    # 	orginal_sentence = ' '.join(orginal_sentence)
    # 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
    page_request_var = 'page'
    paginator = Paginator(all_products, 20)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'page': 'headphone_page'}
    # print(all_products.count())
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)


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
    whichPage(request, 'tvP', url)
    share_string = 'Compare Bags - Latest Bags by Price & Shop'
    t1 = time.time()
    confirmed = None
    all_products = Products.objects.order_by('?').filter(genre='women-bags')
    product_counter = all_products.count()
    # if corrected_sentence != orginal_sentence:
    # 	corrected_sentence = ' '.join(corrected_sentence)
    # 	orginal_sentence = ' '.join(orginal_sentence)
    # 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
    page_request_var = 'page'
    paginator = Paginator(all_products, 20)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'page': 'wemen_bags_page'}
    # print(all_products.count())
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)


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
    whichPage(request, 'wemenP', url)
    share_string = 'Compare Beautiful Dresses - Latest Beautiful Dresses by Price & Shop'
    t1 = time.time()
    confirmed = None
    all_products = Products.objects.order_by('?').filter(genre='women-dresses')
    page_request_var = 'page'
    paginator = Paginator(all_products, 10)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'page': 'women_dress_page'}
    # print(all_products.count())
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)


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
    t1 = time.time()
    whichPage(request, 'wemen_watchP', url)
    share_string = 'Compare Beautiful Women Watches - Latest Beautiful Women Watches by Price & Shop'
    confirmed = None
    all_products = Products.objects.order_by('?').filter(genre='women-watches')
    page_request_var = 'page'
    paginator = Paginator(all_products, 20)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'page': 'women_page'}
    # print(all_products.count())
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)


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
    whichPage(request, 'men_watchP', url)
    share_string = 'Compare Beautiful Men Watches - Latest Beautiful Men Watches by Price & Shop'
    t1 = time.time()
    confirmed = None
    all_products = Products.objects.order_by('?').filter(genre='men-watches')
    page_request_var = 'page'
    paginator = Paginator(all_products, 20)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'page': 'men_watch_page'}
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)

def gaming(request):
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
    whichPage(request, 'men_watchP', url)
    share_string = 'Compare Beautiful Men Watches - Latest Beautiful Men Watches by Price & Shop'
    t1 = time.time()
    confirmed = None
    all_products = Products.objects.filter(genre='gaming').order_by('?')
    page_request_var = 'page'
    paginator = Paginator(all_products, 20)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'share_stringe':share_stringe,
               'page': 'gaming'}
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.6f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'results_page.html', context)


def number_of_clicks(request, words):
    if Products.objects.filter(slug=words).exists():
        product = Products.objects.get(slug=words)
        if not is_bot(request):
            object_viewed.send(product.__class__, instance=product, request=request)
            product.num_of_clicks = product.num_of_clicks + 1
            product.save()
        if product.shop == 'jumia':
            return HttpResponseRedirect(
                'http://c.jumia.io/?a=35588&c=11&p=r&E=kkYNyk2M4sk%3d&ckmrdr=' + product.source_url + '&utm_source=cake&utm_medium=affiliation&utm_campaign=35588&utm_term=')
        else:
            return HttpResponseRedirect(product.source_url)
    else:
        return HttpResponse('Not Found on this beautiful server')


def feedback(request):
    if request.method != 'POST':
        form = feedBackForm()
    else:
        # csrfmiddlewaretoken
        print(request.POST['csrfmiddlewaretoken'])
        form = feedBackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.url_locator= request.POST['user_url']
            feedback.current_location = request.POST['user_c_name']
            feedback.feelings = int(request.POST['reactionScore'])
            feedback.save()
    return HttpResponse('ok')


def despiration(request):
    stuffs = Products.objects.filter(shop='aliexpress')
    stuffs.delete()
    return HttpResponse('All done boss')


def all_on_it(request):
    return HttpResponse('i will find you and kill you')

def test_engine_starter(request):
    return HttpResponse('post woel')

def engine_starter(request):
    black_rock()
    return HttpResponse('All done bose')


def stupid_me(request):
    # Products.objects.all().delete()
    return HttpResponse('You have successfully deleted all the db')


def twitter_bot(request):
    return HttpResponse('you are in trouble')


def sugget(request):
    query = request.GET.get('search',None)
    # adder = []
    if query:
        query = query.split()
        num = len(query)
        for q in range(num):
            product_list = products_list.filter(name__icontains=query[q])
        adder = [{'name' : su.name.replace('\t','').replace('\n','')} for su in product_list]
    else:
        adder=[]
    return JsonResponse({'query': adder})


def deleteu(request):
    products = Products.objects.filter(name__icontains='Playstation')
    for product in products:
        product.genre = 'gaming'
        product.save()
    return HttpResponse('all done')


def convert_me(request):
    products = Products.objects.all().exclude(shop='aliexpress')
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


def polp(request):
    products = Products.objects.filter(shop='aliexpress')
    for product in products:
        price = nairaconv(product.price)
        product.price = '$ US $19.60'
        product.save()
    return HttpResponse('bfgg')


def timeLogs(request):
    user = get_client_ip(request)
    time = request.GET.get('timespent', None)
    page = request.GET.get('page', None)
    url = request.GET.get('url', None)
    time = str(time)
    print(time)
    user_time = UserTime.objects.create(user_o=user, time_spent=time, page=page, current_page=url)
    user_time.save()
    return HttpResponse('hii')


############################################################################
#####################		Trending Layout			########################

def real_trend(request, word):
    share_string = 'Compare Trending Products - Latest Trending Products by Price & Shop'
    t1 = time.time()
    url = request.build_absolute_uri()
    whichPage(request, 'Trending', url)
    orginal_sentence = []
    corrected_sentence = []
    confirmed = None
    query = request.GET.get('q')
    if word != 'index':
        all_products = Products.objects.order_by('-num_of_clicks').filter(genre=word)
    else:
        all_products = Products.objects.order_by('-num_of_clicks')
    if query:
        whichPage(request, 'search Trending', request.build_absolute_uri())
        if 'iphone' in str(query.lower()) or 'ipad' in str(query.lower()):
            # # print(query)
            # print(list(query))
            query = query.lower()
            quey = query.split()
            if len(quey) >= 3:
                if 'plus' in quey and len(quey) <= 3:
                    q = ' '.join(quey)
                    all_products = all_products.filter(
                        Q(name__icontains=q) |
                        Q(name__iexact=q)
                    ).distinct()
                else:
                    for q in quey:
                        all_products = all_products.filter(
                            Q(name__icontains=q)

                        ).distinct()
                add_query(query, 'search page', all_products[:10], nbool=True)
            else:
                # query = correction(query)
                query = query.strip()
                all_products = all_products.filter(
                    Q(name__icontains=query) |
                    Q(name__iexact=query)
                ).distinct()
                if len(all_products) == 0:
                    add_query(query, 'search page', all_products[:10], nbool=False)
                else:
                    add_query(query, 'search page', all_products[:10], nbool=True)
        else:
            query = query.split()
            for q in query:
                all_products = all_products.filter(
                    Q(name__icontains=q) |
                    Q(name__iexact=q)
                ).distinct()
            query = ' '.join(query)
            if len(all_products) == 0:
                add_query(query, 'search page', all_products[:10], nbool=False)
            else:
                add_query(query, 'search page', all_products[:10], nbool=True)
    # if corrected_sentence != orginal_sentence:
    # 	corrected_sentence = ' '.join(corrected_sentence)
    # 	orginal_sentence = ' '.join(orginal_sentence)
    # 	confirmed = 'Showing result of {0} instead of {1}'.format(corrected_sentence,orginal_sentence)
    page_request_var = 'page'
    paginator = Paginator(all_products, 40)
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
        return render(request, 'results_ajax.html', {'products': queryset})
    context = {'products': queryset,
               'query': query,
               'confirmed': confirmed,
               'all_product': all_products,
               'share_string': share_string,
               'page': 'trending_' + word

               }
    # print(all_products.count())
    t2 = time.time()
    query_time = t2 - t1
    query_time = '{:.3f}'.format(query_time)
    context['query_time'] = query_time
    return render(request, 'result_trend_page.html', context)


def delunn(request):
    for product in Products.objects.all():
        product.slug = slugify('%s-%s-%s'%(product.name,product.id,product.shop))
        product.save()
    return HttpResponse('Sacrifices')

def tips_loud(request):
    tips = Tips.objects.order_by('?')[0]
    if tips.image_1:
        return JsonResponse({'text': tips.body, 'img': tips.image.url, 'img_1': tips.image_1.url})
    elif tips.image:
        return JsonResponse({'text': tips.body, 'img': tips.image.url})
    else:
        return JsonResponse({'text': tips.body})

def error_404(request):
    return render(request,'error_500.html', {})
 
def error_500(request):
    return render(request,'error_500.html', {})

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
