from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.HomeView, name='HomeView'),
    url(r'^pageview/$', views.pageView, name='pageView'),
    url(r'^usergrowth/$', views.usergrowth, name='susergrowth'),
    url(r'^userclicks/$', views.userClicks, name='userClicks'),
]
