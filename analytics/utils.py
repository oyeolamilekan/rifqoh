from .models import QueryList,PageViews,UserNumber
from .an_utils import get_client_ip


def add_query(query,sect,listedd,nbool,correct,request):
	user_ip = get_client_ip(request)
	query_up = QueryList.objects.create(title=query,section=sect,res_list=listedd,qury_bool=nbool,corrected=correct,baser_url=user_ip)
	query_up.save()

def whichPage(request,curr_p,urll):
	pagedViewd = PageViews.objects.create(title=curr_p,ip_address=get_client_ip(request),url=urll)
	pagedViewd.save()

def user_count(request):
	if UserNumber.objects.filter(user_ip=get_client_ip(request)).exists():
		pass
	else:
		user_count = UserNumber.objects.create(user_ip=get_client_ip(request))
		user_count.save()

def user_converter(number):
	if UserNumber.objects.filter(user_ip=number).exists():
		pass
	else:
		user_count = UserNumber.objects.create(user_ip=number)
		user_count.save()