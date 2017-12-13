from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count
from django.shortcuts import render
import datetime
from .models import PageViews,UserNumber
from django.http import JsonResponse,HttpResponse

# Create your views here.

def HomeView(request):
	return render(request,'analytics/index.html',{})

def pageView(request):
	data_set = []
	days = []
	page_v = PageViews.objects.extra({'timestamp':"date(timestamp)"}).values('timestamp').annotate(date_added_count=Count('id'))[14:]
	for page in page_v:
		data_set.append(page['date_added_count'])
		days.append(datetime.datetime.strptime(str(page['timestamp']), '%Y-%m-%d').strftime('%a'))
	return JsonResponse({'data_set':data_set,'days':days})

def usergrowth(request):
	data_sett = []
	dayses = []
	user_g = UserNumber.objects.extra({'date_added':"date(date_added)"}).values('date_added').annotate(date_added_count=Count('id'))
	for user in user_g:
		data_sett.append(user['date_added_count'])
		dayses.append(datetime.datetime.strptime(str(user['date_added']), '%Y-%m-%d').strftime('%a'))
	return JsonResponse({'data_s':data_sett,'dayses':dayses})
