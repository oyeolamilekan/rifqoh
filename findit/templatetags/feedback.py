from django import template
from ..forms import feedBackForm
from analytics.utils import get_location
register = template.Library()

@register.inclusion_tag('_form.html')
def report_form(url,request):
	#user_c_name, user_c_code = get_location(request=request)
	user_c_name = 'nigeria'
	form = feedBackForm()
	return {'form':form,'url':url,'user_c_name':user_c_name}