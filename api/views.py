from rest_framework import viewsets, pagination, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from findit.models import Products
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .serializers import ProductSerializer
from watson import search as watson
from algoliasearch_django import raw_search

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProductView(viewsets.ModelViewSet):
    queryset = Products.objects.order_by('-num_of_clicks')
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

class ProductViewLaptops(viewsets.ModelViewSet):
    queryset = Products.objects.filter(genre='laptops').order_by('-num_of_clicks')
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

class ProductViewPhones(viewsets.ModelViewSet):
    queryset = Products.objects.filter(genre='phone').order_by('-num_of_clicks')
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

class ProductViewGaming(viewsets.ModelViewSet):
    queryset = Products.objects.filter(genre='gaming').order_by('-num_of_clicks')
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

class GameProductView(viewsets.ModelViewSet):
    queryset = Products.objects.filter(genre='gaming').order_by('?')
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

class ProductViewPhone(viewsets.ModelViewSet):
    queryset = Products.objects.filter(genre='phone').order_by('?')
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    
class ProductViewLaptop(viewsets.ModelViewSet):
    queryset = Products.objects.filter(genre='laptops').order_by('?')
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

@api_view(['GET'])
def ShopProduct(request,slug,cat):
    ##  Allows me to filter dynamically
    ##  it's filters both catergory 
    ##  and the shop so its a 2 in 1
    ##  Through the shops without
    ##  Having to write multiple code
    if cat == 'all':
        products = Products.objects.filter(shop=slug)
    else:
        products = Products.objects.filter(shop=slug,genre=cat)
    paginator = pagination.PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(products,request=request)
    serializer = ProductSerializer(result_page,many=True)
    return paginator.get_paginated_response(serializer.data)

def search_query(request):
    try:
        queryset = Products.objects.all()
        query = request.GET.get('q')
        if query:
            params = { "hitsPerPage": 15 }
            queryset = raw_search(Products, query, params)
        return JsonResponse({'results':queryset['hits']})
    except:
        return HttpResponse('nothing')

    
def number_of_clicks(request, slug):
    if Products.objects.filter(slug=slug).exists():
        product = Products.objects.get(slug=slug)
        print()
        # if not is_bot(request):
        #     object_viewed.send(product.__class__, instance=product, request=request)
        product.num_of_clicks = product.num_of_clicks + 1
        product.save()
        if product.shop == 'jumia':
            return redirect(
                'http://c.jumia.io/?a=35588&c=11&p=r&E=kkYNyk2M4sk%3d&ckmrdr=' + product.source_url + '&utm_source=cake&utm_medium=affiliation&utm_campaign=35588&utm_term=')
        else:
            return redirect(product.source_url)
    else:
        return HttpResponse('Not Found on this beautiful server')