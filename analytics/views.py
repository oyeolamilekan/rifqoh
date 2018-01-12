import datetime

from django.db.models.aggregates import Count
from django.http import JsonResponse
from django.shortcuts import render

from .models import PageViews, UserNumber, ObjectViewed


# Create your views here.

def HomeView(request):
    return render(request, 'analytics/index.html', {})


def pageView(request):
    data_set = []
    days = []
    page_v = PageViews.objects.extra({'timestamp': "date(timestamp)"}).values('timestamp').annotate(
        date_added_count=Count('id')).order_by('timestamp')[10:]
    for page in page_v:
        data_set.append(page['date_added_count'])
        days.append(datetime.datetime.strptime(str(page['timestamp']), '%Y-%m-%d').strftime('%a'))
    return JsonResponse({'data_set': data_set, 'days': days})


def usergrowth(request):
    data_sett = []
    dayses = []
    user_g = UserNumber.objects.extra({'date_added': "date(date_added)"}).values('date_added').annotate(
        date_added_count=Count('id')).order_by('date_added')
    for user in user_g:
        data_sett.append(user['date_added_count'])
        dayses.append(datetime.datetime.strptime(str(user['date_added']), '%Y-%m-%d').strftime('%a'))
    return JsonResponse({'data_s': data_sett, 'dayses': dayses})


def userClicks(request):
    data_sett = []
    dayses = []
    user_g = ObjectViewed.objects.extra({'timestamp': "date(timestamp)"}).values('timestamp').annotate(
        date_added_count=Count('id')).order_by('timestamp')
    for user in user_g:
        data_sett.append(user['date_added_count'])
        dayses.append(datetime.datetime.strptime(str(user['timestamp']), '%Y-%m-%d').strftime('%a'))
    print(data_sett)
    return JsonResponse({'data_s': data_sett, 'dayses': dayses})
