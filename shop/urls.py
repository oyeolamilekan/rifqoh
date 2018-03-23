from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
    path('', views.store, name='index'),
    path('shop_index/', views.home_p, name='shop_index'),
    path('shop_register/', views.register, name='shop_reg'),
    path('dashboard/',views.dashboard,name='dashh'),
    path('<slug:word>/', views.store_details, name='store_details'),
    path('<slug:word>/shirts/', views.store_shirts, name='store_shirts'),
    path('<slug:word>/phones/', views.store_phones, name='store_phones'),
    path('<slug:word>/laptops/', views.store_laptops, name='store_laptops'),#store_tv_index
    path('<slug:word>/tvs/', views.store_tv_index, name='store_tv_index'),#store_women_index
    path('<slug:word>/womens-cloth/', views.store_women_index, name='store_women_index'),
    path('<slug:word>/headphones/', views.store_heaphones, name='store_heaphones'),#store_tv_index
    path('<slug:word>/women_bags/', views.store_women_bags, name='store_women_bags'),#store_women_index
    path('<slug:word>/store_makeup/', views.store_makeup, name='store_makeup'),
]