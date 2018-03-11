from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.home_page, name='home_page'),
    #url(r'^steore/$',views.rest_store,name='paa'),
    url(r'^$', views.real_index, name='real_index'),
    url(r'^about/$', views.about_home, name='about_home'),
    url(r'^suggest/$', views.sugget, name='sugget'),
    url(r'^women-dresses/$', views.women_index, name='wemen'),
    url(r'^tvs/$', views.tv_index, name='tv_index'),
    url(r'^shirts/$', views.shirts, name='shirts'),
    url(r'^phones/$', views.index, name='index'),  #
    url(r'^minus_club/$', views.minus_club, name='minus_club'),
    url(r'^analytics/(?P<id>\d+)/$', views.number_of_clicks, name='analytics'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^laptops/$', views.laptops, name='laptops'),
    url(r'^worker/$', views.despiration, name='worker'),
    url(r'^down/$', views.engine_starter, name='engine_starter'),
    url(r'^delete/$', views.all_on_it, name='engine_starter'),
    url(r'^twitter_bot/$', views.twitter_bot, name='twitter_bot'),
    url(r'^advanced_search/$', views.advanced_search, name='advanced_search'),
    url(r'^men_watch/$', views.men_watch, name='men_watch'),
    url(r'^women_watch/$', views.women_watch, name='women_watch'),
    url(r'^women_bags/$', views.wemenbags, name='wemenbags'),
    url(r'^headphones/$', views.headphones, name='headphones'),
    url(r'^makeup/$', views.makeup, name='makeup'),
    url(r'^deleteu/$', views.deleteu, name='deleteu'),
    url(r'^revers/$', views.convert_me, name='convert_me'),  # delunn
    url(r'^trending/(?P<word>[\w-]+)/$', views.real_trend, name='real_trend'),
    url(r'^delunn/$', views.delunn, name='delunn'),
    url(r'^convertion/$', views.batch_convertor, name='stupid_me'),
    url(r'^user_choice/$', views.user_choice, name='user_choice'),  # priceconvert
    url(r'^jumia/$', views.priceconvert, name='priceconvert'),
    url(r'^add_log/$', views.timeLogs, name='timeLogs'),
    url(r'^tips_loud/$', views.tips_loud, name='tips_loud'),
    url(r'^breath/$',views.going_global,name='going_global')

]
