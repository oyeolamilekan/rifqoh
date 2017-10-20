from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.store, name='index'),
    url(r'^(?P<word>[\w-]+)/$', views.store_details, name='store_details'),
    url(r'^(?P<word>[\w-]+)/shirts/$', views.store_shirts, name='store_shirts'),
    url(r'^(?P<word>[\w-]+)/phones/$', views.store_phones, name='store_phones'),
    url(r'^(?P<word>[\w-]+)/laptops/$', views.store_laptops, name='store_laptops'),#store_tv_index
    url(r'^(?P<word>[\w-]+)/tvs/$', views.store_tv_index, name='store_tv_index'),#store_women_index
    url(r'^(?P<word>[\w-]+)/womens-cloth/$', views.store_women_index, name='store_women_index'),


]