from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .signals import object_viewed
from .an_utils import get_client_ip
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from accounts.signals import user_logged_in

# Create your models here.

User = settings.AUTH_USER_MODEL

# Query list get 

class QueryList(models.Model):
	title = models.CharField(max_length=200)
	res_list = models.TextField(blank=True,null=True)
	section = models.CharField(max_length=200)
	qury_bool = models.BooleanField(default=True)
	date_added = models.DateTimeField(auto_now_add=True,blank=True,null=True)

	def __str__(self):
		return self.title

class ObjectViewed(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)
	ip_address = models.CharField(max_length=300,blank=True,null=True)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type','object_id')
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s viewed on %s' %(self.content_object,self.timestamp)

	class Meta:
		ordering = ['-timestamp']
		verbose_name = 'Object viewed'
		verbose_name_plural = 'Object viewed plural'

def object_viewed_reciever(sender,instance,request,*args,**kwargs):
	c_type = ContentType.objects.get_for_model(sender)
	new_view_obj = ObjectViewed.objects.create(
			user = request.user,
			ip_address = get_client_ip(request),
			object_id = instance.id,
			content_type = c_type,
		)

object_viewed.connect(object_viewed_reciever)


class UserSession(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)
	ip_address = models.CharField(max_length=200,blank=True,null=True)
	session_key = models.CharField(max_length=100,blank=True,null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	ended = models.BooleanField(default=False)



def user_logged_in_reciever(sender, instance, request, *args, **kwargs):
	user = instance
	ip_address = get_client_ip(request)
	session_key = request.session.session_key
	UserSession.objects.create(
		user=user,
		ip_address=ip_address,
		session_key=session_key
	)
user_logged_in.connect(user_logged_in_reciever)