from django.contrib import admin
from .models import QueryList,ObjectViewed,UserSession,PageViews,UserNumber,UserTime

# Register your models here.

admin.site.register(QueryList)

admin.site.register(ObjectViewed)

admin.site.register(UserSession)

admin.site.register(PageViews)

admin.site.register(UserNumber)

admin.site.register(UserTime)