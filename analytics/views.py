import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import PageViews, UserNumber, ObjectViewed
from accounts.forms import LoginForm


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active and user.is_superuser:
                    login(request, user)
                    next_page = request.POST.get('next')
                    if next_page:
                        return JsonResponse({'redirect':'http://'+request.get_host()+next_page})
                    else:
                        return JsonResponse({'redirect':'http://'+request.get_host()})
                else:
                    print('h')
                    return HttpResponse('Disabled account')
            else:
                print('h')
                return JsonResponse({'error':'true'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Handles the home view to show the graphs
@login_required(login_url='/double/login/')
def HomeView(request):
    print(request.session.session_key)
    return render(request, 'analytics/index.html', {})


# Shows the number of products clicked by the on the graph
@login_required(login_url='/double/login/')
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


# Show the numbers of users acquired on each day and displays on the graph
@login_required(login_url='/double/login/')
def user_acq(request):
    number_q = UserNumber.objects.order_by('-id')
    page_request_var = 'page'
    query = request.GET.get('q')
    if query:
        number_q = UserNumber.objects.filter(user_ip=query)
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

@login_required(login_url='/double/login/')
def pageView(request):
    data_set = []
    days = []
    page_v = PageViews.objects.extra({'timestamp': "date(timestamp)"}).values('timestamp').annotate(
        date_added_count=Count('id')).order_by('timestamp')[10:]
    for page in page_v:
        data_set.append(page['date_added_count'])
        days.append(datetime.datetime.strptime(str(page['timestamp']), '%Y-%m-%d').strftime('%a'))
    return JsonResponse({'data_set': data_set, 'days': days})

@login_required(login_url='/double/login/')
def usergrowth(request):
    data_sett = []
    dayses = []
    user_g = UserNumber.objects.extra({'date_added': "date(date_added)"}).values('date_added').annotate(
        date_added_count=Count('id')).order_by('date_added')[10:]
    for user in user_g:
        data_sett.append(user['date_added_count'])
        dayses.append(datetime.datetime.strptime(str(user['date_added']), '%Y-%m-%d').strftime('%a'))
    return JsonResponse({'data_s': data_sett, 'dayses': dayses})

@login_required(login_url='/double/login/')
def userClicks(request):
    data_sett = []
    dayses = []
    user_g = ObjectViewed.objects.extra({'timestamp': "date(timestamp)"}).values('timestamp').annotate(
        date_added_count=Count('id')).order_by('timestamp')[10:]
    for user in user_g:
        data_sett.append(user['date_added_count'])
        dayses.append(datetime.datetime.strptime(str(user['timestamp']), '%Y-%m-%d').strftime('%a'))
    return JsonResponse({'data_s': data_sett, 'dayses': dayses})
