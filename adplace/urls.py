from django.urls import path
from . import views

app_name = 'adengine'
urlpatterns = [
	path('',views.home_page,name='home_page'),
	path('index/',views.index,name='index'),
	path('<int:ads>/', views.click_by, name='ads'),
	path('dashboard/', views.dash, name='dash'),
	path('data_set/', views.loaded, name='data_set'),
	path('pay_val/', views.payment_val, name='payment_val'),
	path('ads_upload/', views.upload_ads, name='upload_ads'),
	path('edit_ads/<int:id>/', views.edit_ads, name='edit_ads'),
	path('reactivation/<int:id>/', views.reactivate_payment_val, name='reactivate_payment_val'),
]