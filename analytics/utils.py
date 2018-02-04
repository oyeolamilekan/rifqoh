from .an_utils import get_client_ip, is_bot, get_location,get_header_info
from .models import QueryList, PageViews, UserNumber


def add_query(query, sect, listedd, nbool, correct, request):
    user_ip = get_client_ip(request)
    query_up = QueryList.objects.create(title=query, 
                                section=sect, 
                                res_list=listedd, 
                                qury_bool=nbool, 
                                corrected=correct,
                                baser_url=user_ip)
    query_up.save()


def whichPage(request, curr_p, urll):
    if not is_bot(request):
        pagedViewd = PageViews.objects.create(title=curr_p, 
                                ip_address=get_client_ip(request), 
                                url=urll)
        pagedViewd.save()


def user_count(request):
    if not is_bot(request):
        if not UserNumber.objects.filter(user_ip=get_client_ip(request)).exists():
            user_c_name, user_c_code = get_location(request=request)
            user_count = UserNumber.objects.create(
                            user_ip=get_client_ip(request),
                            user_header=get_header_info(request),
                            user_country_name=user_c_name,
                            user_country_code=user_c_code)
            user_count.save()


def user_converter(number):
    if not UserNumber.objects.filter(user_ip=number).exists():
        user_count = UserNumber.objects.create(user_ip=number)
        user_count.save()
