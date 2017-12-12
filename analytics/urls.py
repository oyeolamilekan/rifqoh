from django.conf.urls import url, handler404, handler500
from . import views

urlpatterns = [
	url(r'^$', views.HomeView, name='HomeView'),
	url(r'^pageview/$', views.pageView, name='pageView'),
	url(r'^usergrowth/$', views.usergrowth, name='susergrowth'),
]