from django.urls import path

from . import views
app_name = 'findit'
urlpatterns = [
    # url(r'^$', views.home_page, name='home_page'),
    #url(r'^steore/$',views.rest_store,name='paa'),
    path('', views.real_index, name='real_index'),
    path('test_engine_starter/', views.test_engine_starter, name='test_engine_starter'),
    path('about/', views.about_home, name='about_home'),
    path('suggest/', views.sugget, name='sugget'),
    path('women-dresses/', views.women_index, name='wemen'),
    path('tvs/', views.tv_index, name='tv_index'),
    path('shirts/', views.shirts, name='shirts'),
    path('phones/', views.index, name='index'),  #
    path('minus_club/', views.minus_club, name='minus_club'),
    path('clicks/<slug:words>/', views.number_of_clicks, name='analytics'),
    path('feedback/', views.feedback, name='feedback'),
    path('laptops/', views.laptops, name='laptops'),
    path('worker/', views.despiration, name='worker'),
    path('down/', views.engine_starter, name='engine_starter'),
    path('delete/', views.all_on_it, name='engine_arter'),
    path('twitter_bot/', views.twitter_bot, name='twitter_bot'),
    path('advanced_search/', views.advanced_search, name='advanced_search'),
    path('men_watch/', views.men_watch, name='men_watch'),
    path('women_watch/', views.women_watch, name='women_watch'),
    path('women_bags/', views.wemenbags, name='wemenbags'),
    path('headphones/', views.headphones, name='headphones'),
    path('makeup/', views.makeup, name='makeup'),
    path('deleteu/', views.deleteu, name='deleteu'),
    path('revers/', views.convert_me, name='convert_me'),  # delunn
    path('trending/<slug:word>/', views.real_trend, name='real_trend'),
    path('delunn/', views.delunn, name='delunn'),
    path('convertion/', views.batch_convertor, name='stupid_me'),
    path('user_choice/', views.user_choice, name='user_choice'),  # priceconvert
    path('jumia/', views.priceconvert, name='priceconvert'),
    path('add_log/', views.timeLogs, name='timeLogs'),
    path('tips_loud/', views.tips_loud, name='tips_loud'),
    path('breath/',views.going_global,name='going_global')

]
