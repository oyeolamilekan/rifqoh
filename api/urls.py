from django.urls import path, include
from rest_framework import routers
from .views import *
app_name = 'api'

router = routers.DefaultRouter()
router.register('products', ProductView, 'products')
router.register('phone', ProductViewPhone, 'phone')
router.register('laptops', ProductViewLaptop, 'laptops')
router.register('gaming', GameProductView, 'gaming')
router.register('phone_t', ProductViewPhones, 'phone')
router.register('laptops_t', ProductViewLaptops, 'laptops')
router.register('gaming_t', ProductViewGaming, 'gaming')
urlpatterns = [
    path('', include(router.urls)),
    path('r_search/',search_query),
    path('r_redirect/<slug>/',number_of_clicks),
    path('q_shop/<slug:slug>/<slug:cat>/',ShopProduct)
]
