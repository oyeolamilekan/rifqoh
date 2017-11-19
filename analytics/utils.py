from .models import QueryList,PageViews
from .an_utils import get_client_ip


def add_query(query,sect,listedd,nbool):
	query_up = QueryList.objects.create(title=query,section=sect,res_list=listedd,qury_bool=nbool)
	query_up.save()

def whichPage(request,curr_p,urll):
	pagedViewd = PageViews.objects.create(title=curr_p,ip_address=get_client_ip(request),url=urll)
	pagedViewd.save()
