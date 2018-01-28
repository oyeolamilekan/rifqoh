import datetime

from django.db.models.aggregates import Count
from django.http import JsonResponse
from django.shortcuts import render
from .models import ObjectViewed,UserNumber
from .models import PageViews, UserNumber, ObjectViewed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def HomeView(request):
    return render(request, 'analytics/index.html', {})



def prod_clicks(request):
    number_q = ObjectViewed.objects.order_by('-id')
    page_request_var = 'page'
    paginator = Paginator(number_q, 20)
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
    if request.is_ajax():
        return render(request, 'analytics/number_q_ajax.html', {'queries': queryset})
    context = {'queries': queryset}
    return render(request, 'analytics/number_q.html', context)

def user_acq(request):
    number_q = UserNumber.objects.order_by('-id')
    page_request_var = 'page'
    paginator = Paginator(number_q, 20)
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
    if request.is_ajax():
        return render(request, 'analytics/number_c_ajax.html', {'queries': queryset})
    context = {'queries': queryset}
    return render(request, 'analytics/number_c.html', context)

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
        date_added_count=Count('id')).order_by('date_added')[10:]
    for user in user_g:
        data_sett.append(user['date_added_count'])
        dayses.append(datetime.datetime.strptime(str(user['date_added']), '%Y-%m-%d').strftime('%a'))
    return JsonResponse({'data_s': data_sett, 'dayses': dayses})


def userClicks(request):
    data_sett = []
    dayses = []
    user_g = ObjectViewed.objects.extra({'timestamp': "date(timestamp)"}).values('timestamp').annotate(
        date_added_count=Count('id')).order_by('timestamp')[10:]
    for user in user_g:
        data_sett.append(user['date_added_count'])
        dayses.append(datetime.datetime.strptime(str(user['timestamp']), '%Y-%m-%d').strftime('%a'))
    return JsonResponse({'data_s': data_sett, 'dayses': dayses})
