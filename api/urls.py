from django.conf.urls import url

from . import views
app_name = 'api'
urlpatterns = [
    url(r'^$',views.home_page, name='home'),
    url(r'^getting_started/$',views.getting_started, name='getting_started'),
    url(r'^product_by_cat/$',views.catergory_tuts, name='catergory_tuts'),
    url(r'^product_by_shop/$',views.shop_tuts, name='shop_tuts'),
    url(r'^product_list/$', views.rest_product_list, name='product_list'),
    url(r'^store_product_list/(?P<slug>[\w-]+)/$',
        views.rest_store_detail, name='rest_store_detail'),
    url(r'^product_catergory/(?P<slug>[\w-]+)/$',
        views.rest_product_catergory, name='rest_product_catergory'),
    url(r'^store_product_catergory/(?P<slug>[\w-]+)/(?P<plug>[\w-]+)/$',
        views.rest_store_product_catergory, name='rest_store_product_catergory'),
]
