from django.conf.urls import url

from . import views
app_name = 'analytics'
urlpatterns = [
    url(r'^$', views.HomeView, name='HomeView'),
    url(r'^prod_clicks/$', views.prod_clicks, name='prod_clicks'),
    url(r'^user_acq/$', views.user_acq, name='user_acq'),
    url(r'^pageview/$', views.pageView, name='pageView'),
    url(r'^usergrowth/$', views.usergrowth, name='susergrowth'),
    url(r'^userclicks/$', views.userClicks, name='userClicks'),
]
