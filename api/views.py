from django.core import serializers
from django.shortcuts import render
import json

# Create your views here.

def rest_product_list(request):
    products_list = Products.objects.all()[:100]
    product_names = [{"name":product_list.name,
    				'img':product_list.image.url,
    				"shop":product_list.shop,
    				'price':product_list.price,
    				'catergory':product_list.genre} for product_list in products_list]
    return HttpResponse(json.dumps(store_names), content_type='application/json')

def rest_store_detail(request, slug):
	products_list = Products.objects.filter(shop=slug)[:100]
    product_names = [{"name":product_list.name,
    				'img':product_list.image.url,
    				"shop":product_list.shop,
    				'price':product_list.price,
    				'catergory':product_list.genre} for product_list in products_list]
    return HttpResponse(json.dumps(store_names), content_type='application/json')

def rest_product_catergory(request, slug):
	products_list = Products.objects.filter(genre=slug)[:100]
    product_names = [{"name":product_list.name,
    				'img':product_list.image.url,
    				"shop":product_list.shop,
    				'price':product_list.price,
    				'catergory':product_list.genre} for product_list in products_list]
    return HttpResponse(json.dumps(store_names), content_type='application/json')
