import json

from django.shortcuts import render
from django.http import HttpResponse

from findit.models import Products


# Create your views here.

def home_page(request):
    products_list = Products.objects.order_by('?')[:100]
    product_names = [{'e_img': product_list.image.url, 'c_shop': product_list.shop, 'd_catergory': product_list.genre,
                        'b_price': product_list.price, 'a_name': product_list.name, } for product_list in products_list]
    product = json.dumps(product_names, sort_keys=True, indent=2)
    return render(request,'api/home_page.html',{'products':product})

# The Getting started page
def getting_started(request):
    return render(request,'api/getting_started.html',{})

# Get products by catergory tutorial
def catergory_tuts(request):
  return render(request,'api/get_product_cat.html',{})

# Get products from shop
def shop_tuts(request):
  return render(request,'api/get_product_shop.html',{})



########### API Query views ###########
def rest_product_list(request):
    products_list = Products.objects.order_by('?')[:100]
    product_names = [{'e_img': product_list.image.url, 'c_shop': product_list.shop, 'd_catergory': product_list.genre,
                      'b_price': product_list.price, 'a_name': product_list.name, } for product_list in products_list]
    return HttpResponse(json.dumps(product_names, sort_keys=True, indent=2), content_type='application/json')


def rest_store_detail(request, slug):
    products_list = Products.objects.filter(shop=slug).order_by('?')[:100]
    product_names = [{'e_img': product_list.image.url, 'c_shop': product_list.shop, 'd_catergory': product_list.genre,
                      'b_price': product_list.price, 'a_name': product_list.name, } for product_list in products_list]
    return HttpResponse(json.dumps(product_names, sort_keys=True, indent=4), content_type='application/json')


def rest_product_catergory(request, slug):
    products_list = Products.objects.filter(genre=slug).order_by('?')[:100]
    product_names = [{'e_img': product_list.image.url, 'c_shop': product_list.shop, 'd_catergory': product_list.genre,
                      'b_price': product_list.price, 'a_name': product_list.name, } for product_list in products_list]
    return HttpResponse(json.dumps(product_names, sort_keys=True, indent=4), content_type='application/json')


def rest_store_product_catergory(request, slug, plug):
    products_list = Products.objects.filter(genre=slug, shop=plug).order_by('?')[:100]
    product_names = [{'e_img': product_list.image.url, 'c_shop': product_list.shop, 'd_catergory': product_list.genre,
                      'b_price': product_list.price, 'a_name': product_list.name, } for product_list in products_list]
    return HttpResponse(json.dumps(product_names, sort_keys=True, indent=4), content_type='application/json')
