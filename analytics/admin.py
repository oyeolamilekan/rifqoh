from django.contrib import admin
from .models import QueryList,ObjectViewed,UserSession

# Register your models here.

admin.site.register(QueryList)

admin.site.register(ObjectViewed)

admin.site.register(UserSession)