from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import post_save

from accounts.signals import user_logged_in
from .an_utils import get_client_ip
from .signals import object_viewed

# Create your models here.

User = settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, 'FORCE_INACTIVE_USER_ENDSESSION', False)

class ProductList(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

# Handles the number of page views
class PageViews(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '%s viewed on %s' % (self.title, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Page Views'
        verbose_name_plural = 'Page Views'


# Handles the number of user acquired
class UserNumber(models.Model):
    user_ip = models.CharField(max_length=200, blank=True, null=True)
    user_header = models.TextField(max_length=200,blank=True,null=True)
    user_session = models.CharField(max_length=200,blank=True,null=True)
    user_country_name = models.CharField(max_length=200, blank=True, null=True)
    user_country_code = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{} added on {}'.format(self.user_ip, self.date_added)

    class Meta:
        ordering = ['-date_added']
        verbose_name = 'User Number'
        verbose_name_plural = 'User Number'


# class UserDirection(models.Model):
# 	user = models.ForeignKey(UserNumber,blank=True,null=True)
# 	direction = models.CharField(max_length=200,blank=True,null=True)
# 	time_spent = models.CharField(max_length=200,blank=True,null=True)
# 	date_added = models.DateTimeField(auto_now_add=True,blank=True,null=True)

# 	def __str__(self):
# 		return user

# handles the queries being send by the user
class QueryList(models.Model):
    title = models.CharField(max_length=200)
    res_list = models.TextField(blank=True, null=True)
    section = models.CharField(max_length=200)
    baser_url = models.CharField(max_length=200, blank=True, null=True)
    qury_bool = models.BooleanField(default=True)
    corrected = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{} searched on {}'.format(self.title, self.date_added)

    class Meta:
        ordering = ['-date_added']
        verbose_name = 'Query List'
        verbose_name_plural = 'Query List'


# Handles the objects seen by the user
class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True,on_delete=True)
    ip_address = models.CharField(max_length=300, blank=True, null=True)
    content_type = models.ForeignKey(ContentType,on_delete=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s viewed on %s' % (self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Object viewed'


def object_viewed_reciever(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    new_view_obj = ObjectViewed.objects.create(
        ip_address=get_client_ip(request),
        object_id=instance.id,
        content_type=c_type,
    )


object_viewed.connect(object_viewed_reciever)


# Handles the time period the user spends on the site
class UserTime(models.Model):
    user_o = models.CharField(max_length=200, blank=True, null=True)
    time_spent = models.CharField(max_length=200, blank=True, null=True)
    current_page = models.CharField(max_length=200, blank=True, null=True)
    page = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{} spent {} seconds on {} timecreated {}'.format(self.user_o, self.time_spent, self.page,
                                                                 self.timestamp)

    class Meta:
        ordering = ['-id']
        verbose_name = 'User Time'
        verbose_name_plural = 'User Time'


# Handles each user session on the site
# class UserSession(models.Model):
#     user = models.ForeignKey(User, blank=True, null=True,on_delete=True)
#     ip_address = models.CharField(max_length=200, blank=True, null=True)
#     session_key = models.CharField(max_length=100, blank=True, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     active = models.BooleanField(default=True)
#     ended = models.BooleanField(default=False)

#     def end_session(self):
#         session_key = self.session_key
#         ended = self.ended
#         try:
#             Session.objects.get(pk=session_key).delete()
#             self.active = False
#             self.ended = True
#             self.save()
#         except:
#             pass
#         return self.ended


# def post_save_session_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
#         for i in qs:
#             i.end_session()

#     if not instance.active and not instance.ended:
#         instance.end_session()


# if FORCE_SESSION_TO_ONE:
#     post_save.connect(post_save_session_receiver, sender=UserSession)


# def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
#     if not created:
#         if instance.is_active == False:
#             qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)


# if FORCE_INACTIVE_USER_ENDSESSION:
#     post_save.connect(post_save_user_changed_receiver, sender=User)


# def user_logged_in_reciever(sender, instance, request, *args, **kwargs):
#     user = instance
#     ip_address = get_client_ip(request)
#     session_key = request.session.session_key
#     UserSession.objects.create(
#         user=user,
#         ip_address=ip_address,
#         session_key=session_key
#     )


# user_logged_in.connect(user_logged_in_reciever)
